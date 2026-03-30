#!/usr/bin/env python3
"""
BackRoad Publish Proxy — Runs on Alice (Pi)
Wraps instagrapi for Instagram + Barcelona API for Threads.
Called by the BackRoad Cloudflare Worker.

Usage:
    python3 publish-proxy.py              # Start on port 9090
    python3 publish-proxy.py --port 9090  # Custom port

Deploy:
    nohup python3 ~/Marketing/tools/publish-proxy.py &
    # Or as systemd service
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
import time
import os
import sys
from pathlib import Path

PORT = int(sys.argv[sys.argv.index('--port') + 1] if '--port' in sys.argv else 9090)
PROXY_SECRET = os.environ.get('PUBLISH_PROXY_SECRET', 'blackroad-publish-2026')
SESSION_DIR = Path.home() / '.blackroad' / 'ig-session'
SESSION_DIR.mkdir(parents=True, exist_ok=True)

# Cache Instagram clients by username
ig_clients = {}


def get_ig_client(username, password):
    """Get or create an Instagram client with session caching."""
    from instagrapi import Client

    if username in ig_clients:
        return ig_clients[username]

    cl = Client()
    cl.delay_range = [2, 5]
    session_file = SESSION_DIR / f'{username}.json'

    if session_file.exists():
        try:
            cl.load_settings(session_file)
            cl.login(username, password)
            ig_clients[username] = cl
            return cl
        except Exception:
            pass

    cl.login(username, password)
    cl.dump_settings(session_file)
    os.chmod(session_file, 0o600)
    ig_clients[username] = cl
    return cl


def publish_instagram(username, password, caption, image_path=None):
    """Post to Instagram. Returns dict with success, url."""
    cl = get_ig_client(username, password)

    if image_path and Path(image_path).exists():
        result = cl.photo_upload(Path(image_path), caption)
    else:
        # Text-only: use a default BlackRoad image
        default_img = Path.home() / 'Marketing' / 'assets' / 'screenshots' / 'local' / 'blackroad-io.png'
        if default_img.exists():
            result = cl.photo_upload(default_img, caption)
        else:
            return {'success': False, 'error': 'No image provided and no default image found'}

    code = result.model_dump().get('code', '') if hasattr(result, 'model_dump') else result.dict().get('code', '')
    return {'success': True, 'url': f'https://www.instagram.com/p/{code}/'}


def publish_threads(username, password, caption):
    """Post to Threads via Barcelona API. Returns dict with success, url."""
    import requests

    cl = get_ig_client(username, password)

    s = requests.Session()
    for name, value in cl.private.cookies.items():
        s.cookies.set(name, value)

    s.headers.update({
        'User-Agent': 'Barcelona 346.1.0.36.119 Android (33/13; 420dpi; 1080x2400; samsung; SM-S908B; b0q; qcom; en_US; 617463801)',
        'Authorization': cl.authorization,
        'X-IG-App-ID': '238260118697367',
        'X-IG-Device-ID': cl.phone_id,
        'X-IG-Android-ID': cl.android_device_id,
        'X-Bloks-Version-Id': cl.bloks_versioning_id,
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    })

    data = {
        'publish_mode': 'text_post',
        'text_post_app_info': json.dumps({'reply_control': 0}),
        'timezone_offset': '-21600',
        'source_type': '4',
        'caption': caption,
        '_uid': str(cl.user_id),
        '_uuid': cl.uuid,
        'device_id': cl.android_device_id,
        'upload_id': str(int(time.time() * 1000)),
    }
    body = json.dumps(data)
    resp = s.post(
        'https://i.instagram.com/api/v1/media/configure_text_only_post/',
        data={'signed_body': f'SIGNATURE.{body}'},
    )
    result = resp.json()
    code = result.get('media', {}).get('code', '')
    if code:
        return {'success': True, 'url': f'https://www.threads.net/@{username}/post/{code}/'}
    return {'success': False, 'error': str(result.get('message', 'unknown error'))}


class ProxyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/health':
            self.respond(200, {'status': 'ok', 'service': 'backroad-publish-proxy', 'platforms': ['instagram', 'threads']})
        else:
            self.respond(404, {'error': 'not found'})

    def do_POST(self):
        # Auth check
        secret = self.headers.get('X-Publish-Secret', '')
        if secret != PROXY_SECRET:
            self.respond(401, {'error': 'unauthorized'})
            return

        content_length = int(self.headers.get('Content-Length', 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}

        if self.path == '/publish/instagram':
            username = body.get('username')
            password = body.get('password')
            caption = body.get('caption', '')
            image_path = body.get('image_path')
            if not username or not password:
                self.respond(400, {'error': 'username and password required'})
                return
            try:
                result = publish_instagram(username, password, caption, image_path)
                self.respond(200, result)
            except Exception as e:
                self.respond(500, {'success': False, 'error': str(e)})

        elif self.path == '/publish/threads':
            username = body.get('username')
            password = body.get('password')
            caption = body.get('caption', '')
            if not username or not password:
                self.respond(400, {'error': 'username and password required'})
                return
            try:
                result = publish_threads(username, password, caption)
                self.respond(200, result)
            except Exception as e:
                self.respond(500, {'success': False, 'error': str(e)})

        else:
            self.respond(404, {'error': 'unknown endpoint'})

    def respond(self, status, data):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def log_message(self, format, *args):
        print(f'[proxy] {args[0]}')


if __name__ == '__main__':
    print(f'BackRoad Publish Proxy starting on port {PORT}...')
    server = HTTPServer(('0.0.0.0', PORT), ProxyHandler)
    print(f'Listening on http://0.0.0.0:{PORT}')
    print(f'Endpoints: /health, /publish/instagram, /publish/threads')
    server.serve_forever()
