#!/usr/bin/env python3
"""
BlackRoad OS — Scheduled Post Runner
Checks scheduled-posts.json and posts anything due now.
Run via cron every 15 minutes.

Usage:
    python3 post-scheduler.py          # Post anything due now
    python3 post-scheduler.py --dry    # Show what would post without posting
    python3 post-scheduler.py --list   # Show full schedule
    python3 post-scheduler.py --next   # Show next upcoming post
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

SCHEDULE_FILE = Path(__file__).parent / "scheduled-posts.json"
POSTED_FILE = Path.home() / ".blackroad" / "posted-log.json"
SCREENSHOTS = Path.home() / "Marketing" / "assets" / "screenshots" / "local"
CRED_FILE = Path.home() / ".blackroad" / "social-credentials.json"
SESSION_DIR = Path.home() / ".blackroad" / "ig-session"


def load_schedule():
    with open(SCHEDULE_FILE) as f:
        return json.load(f)


def load_posted():
    if POSTED_FILE.exists():
        with open(POSTED_FILE) as f:
            return json.load(f)
    return []


def save_posted(posted):
    POSTED_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(POSTED_FILE, "w") as f:
        json.dump(posted, f, indent=2)


def get_ig_client():
    from instagrapi import Client

    with open(CRED_FILE) as f:
        creds = json.load(f)
    ig = creds["instagram"]
    cl = Client()
    cl.load_settings(SESSION_DIR / f'{ig["username"]}.json')
    cl.login(ig["username"], ig["password"])
    return cl


def post_to_instagram(cl, caption, image_name):
    image_path = SCREENSHOTS / image_name
    if not image_path.exists():
        print(f"    Image not found: {image_path}")
        return None
    result = cl.photo_upload(image_path, caption)
    code = result.model_dump().get("code", "")
    return f"https://www.instagram.com/p/{code}/"


def post_to_threads(cl, caption):
    import requests

    s = requests.Session()
    for name, value in cl.private.cookies.items():
        s.cookies.set(name, value)
    s.headers.update({
        "User-Agent": "Barcelona 346.1.0.36.119 Android (33/13; 420dpi; 1080x2400; samsung; SM-S908B; b0q; qcom; en_US; 617463801)",
        "Authorization": cl.authorization,
        "X-IG-App-ID": "238260118697367",
        "X-IG-Device-ID": cl.phone_id,
        "X-IG-Android-ID": cl.android_device_id,
        "X-Bloks-Version-Id": cl.bloks_versioning_id,
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    })

    data = {
        "publish_mode": "text_post",
        "text_post_app_info": json.dumps({"reply_control": 0}),
        "timezone_offset": "-21600",
        "source_type": "4",
        "caption": caption,
        "_uid": str(cl.user_id),
        "_uuid": cl.uuid,
        "device_id": cl.android_device_id,
        "upload_id": str(int(time.time() * 1000)),
    }
    body = json.dumps(data)
    signed = f"SIGNATURE.{body}"
    resp = s.post(
        "https://i.instagram.com/api/v1/media/configure_text_only_post/",
        data={"signed_body": signed},
    )
    result = resp.json()
    code = result.get("media", {}).get("code", "")
    return f"https://www.threads.net/@blackboxprogramming/post/{code}/" if code else None


def is_due(post, now, window_minutes=15):
    """Check if a post is due within the current window."""
    post_dt = datetime.strptime(f'{post["day"]} {post["time"]}', "%Y-%m-%d %H:%M")
    return now - timedelta(minutes=window_minutes) <= post_dt <= now


def post_id(post):
    return f'{post["day"]}_{post["time"]}_{"+".join(post["platforms"])}'


def run_scheduler(dry=False):
    schedule = load_schedule()
    posted = load_posted()
    posted_ids = set(p["id"] for p in posted)
    now = datetime.now()

    print(f"Scheduler run: {now.strftime('%Y-%m-%d %H:%M')}")
    print(f"Schedule: {len(schedule)} posts, {len(posted)} already posted\n")

    due = [p for p in schedule if is_due(p, now) and post_id(p) not in posted_ids]

    if not due:
        print("Nothing due right now.")
        return

    cl = None
    for post in due:
        pid = post_id(post)
        print(f"  DUE: {post['day']} {post['time']} -> {', '.join(post['platforms'])}")
        print(f"  Caption: {post['caption'][:80]}...")

        if dry:
            print("  [DRY RUN — skipping]\n")
            continue

        if cl is None:
            cl = get_ig_client()

        results = {}
        for platform in post["platforms"]:
            try:
                if platform == "instagram" and post.get("image"):
                    url = post_to_instagram(cl, post["caption"], post["image"])
                    results["instagram"] = url
                    print(f"    IG: {url}")
                elif platform == "threads":
                    # Strip hashtags for Threads
                    threads_caption = post["caption"].split("\n#")[0].strip()
                    url = post_to_threads(cl, threads_caption)
                    results["threads"] = url
                    print(f"    Threads: {url}")
                time.sleep(3)
            except Exception as e:
                print(f"    {platform} FAILED: {e}")
                results[platform] = f"error: {e}"

        posted.append({
            "id": pid,
            "posted_at": now.isoformat(),
            "results": results,
        })
        save_posted(posted)
        print()

    print(f"Done. {len(due)} post(s) processed.")


def show_list():
    schedule = load_schedule()
    posted = load_posted()
    posted_ids = set(p["id"] for p in posted)

    print(f"{'Date':12s} {'Time':6s} {'Platforms':20s} {'Image':25s} {'Status':8s}")
    print("-" * 75)
    for post in schedule:
        pid = post_id(post)
        status = "POSTED" if pid in posted_ids else "pending"
        platforms = ", ".join(post["platforms"])
        image = post.get("image") or "(text only)"
        print(f"{post['day']:12s} {post['time']:6s} {platforms:20s} {image:25s} {status:8s}")


def show_next():
    schedule = load_schedule()
    posted = load_posted()
    posted_ids = set(p["id"] for p in posted)
    now = datetime.now()

    for post in schedule:
        pid = post_id(post)
        if pid in posted_ids:
            continue
        post_dt = datetime.strptime(f'{post["day"]} {post["time"]}', "%Y-%m-%d %H:%M")
        if post_dt > now:
            delta = post_dt - now
            hours = delta.total_seconds() / 3600
            print(f"Next post in {hours:.1f} hours:")
            print(f"  Date: {post['day']} {post['time']}")
            print(f"  Platforms: {', '.join(post['platforms'])}")
            print(f"  Image: {post.get('image') or '(text only)'}")
            print(f"  Caption: {post['caption'][:120]}...")
            return
    print("No upcoming posts scheduled.")


def main():
    parser = argparse.ArgumentParser(description="BlackRoad Scheduled Poster")
    parser.add_argument("--dry", action="store_true", help="Dry run")
    parser.add_argument("--list", action="store_true", help="Show schedule")
    parser.add_argument("--next", action="store_true", help="Show next post")
    args = parser.parse_args()

    if args.list:
        show_list()
    elif args.next:
        show_next()
    else:
        run_scheduler(dry=args.dry)


if __name__ == "__main__":
    main()
