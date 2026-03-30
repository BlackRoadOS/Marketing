#!/usr/bin/env python3
"""
BlackRoad OS — Social Media Posting Tool
Posts to Instagram, X/Twitter, Facebook from the command line.
Credentials stored in ~/.blackroad/social-credentials.json (chmod 600).

Usage:
    python3 post.py instagram --caption "Your caption" --image /path/to/image.jpg
    python3 post.py instagram --caption "Caption" --carousel /path/to/img1.jpg /path/to/img2.jpg
    python3 post.py instagram --caption "Caption" --story /path/to/image.jpg
    python3 post.py instagram --caption "Caption" --reel /path/to/video.mp4
    python3 post.py twitter --text "Your tweet"
    python3 post.py twitter --thread "Tweet 1" "Tweet 2" "Tweet 3"
    python3 post.py setup instagram    # Interactive credential setup
    python3 post.py setup twitter      # Interactive credential setup
    python3 post.py status             # Check which platforms are configured
"""

import argparse
import json
import os
import sys
from pathlib import Path

CRED_DIR = Path.home() / ".blackroad"
CRED_FILE = CRED_DIR / "social-credentials.json"
SESSION_DIR = CRED_DIR / "ig-session"


def load_credentials():
    if not CRED_FILE.exists():
        return {}
    with open(CRED_FILE) as f:
        return json.load(f)


def save_credentials(creds):
    CRED_DIR.mkdir(parents=True, exist_ok=True)
    with open(CRED_FILE, "w") as f:
        json.dump(creds, f, indent=2)
    os.chmod(CRED_FILE, 0o600)


def setup_instagram():
    """Store Instagram credentials and test login."""
    from instagrapi import Client

    creds = load_credentials()
    username = input("Instagram username: ").strip()
    password = input("Instagram password: ").strip()

    print(f"Logging in as {username}...")
    cl = Client()
    SESSION_DIR.mkdir(parents=True, exist_ok=True)
    session_file = SESSION_DIR / f"{username}.json"

    try:
        cl.login(username, password)
        cl.dump_settings(session_file)
        os.chmod(session_file, 0o600)
        creds["instagram"] = {
            "username": username,
            "password": password,
            "session_file": str(session_file),
        }
        save_credentials(creds)
        print(f"Logged in as {username}. Session saved.")
        print(f"Account: {cl.account_info().dict().get('full_name', username)}")
        print("Instagram is ready to post.")
    except Exception as e:
        print(f"Login failed: {e}")
        print("If 2FA is enabled, you may see a challenge. Check your email/SMS.")
        # Handle 2FA challenge
        if "challenge" in str(e).lower() or "two_factor" in str(e).lower():
            code = input("Enter the 2FA/challenge code: ").strip()
            try:
                cl.challenge_code_handler = lambda *a, **k: code
                cl.login(username, password, verification_code=code)
                cl.dump_settings(session_file)
                os.chmod(session_file, 0o600)
                creds["instagram"] = {
                    "username": username,
                    "password": password,
                    "session_file": str(session_file),
                }
                save_credentials(creds)
                print("2FA verified. Instagram is ready to post.")
            except Exception as e2:
                print(f"2FA login also failed: {e2}")
                sys.exit(1)
        else:
            sys.exit(1)


def setup_twitter():
    """Store Twitter/X API credentials."""
    creds = load_credentials()
    print("You need X/Twitter API v2 credentials (developer.twitter.com).")
    print("Free tier allows 1,500 tweets/month.")
    api_key = input("API Key (Consumer Key): ").strip()
    api_secret = input("API Secret (Consumer Secret): ").strip()
    access_token = input("Access Token: ").strip()
    access_secret = input("Access Token Secret: ").strip()

    creds["twitter"] = {
        "api_key": api_key,
        "api_secret": api_secret,
        "access_token": access_token,
        "access_secret": access_secret,
    }
    save_credentials(creds)
    print("Twitter/X credentials saved. Testing...")

    try:
        import tweepy
        auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_secret)
        api = tweepy.API(auth)
        user = api.verify_credentials()
        print(f"Authenticated as @{user.screen_name}. Twitter is ready to post.")
    except Exception as e:
        print(f"Verification failed: {e}")
        print("Credentials saved anyway — they may still work for posting.")


def get_ig_client():
    """Get authenticated Instagram client, reusing session."""
    from instagrapi import Client

    creds = load_credentials()
    ig = creds.get("instagram")
    if not ig:
        print("Instagram not configured. Run: python3 post.py setup instagram")
        sys.exit(1)

    cl = Client()
    session_file = Path(ig.get("session_file", ""))

    # Try loading existing session first (avoids rate limits)
    if session_file.exists():
        try:
            cl.load_settings(session_file)
            cl.login(ig["username"], ig["password"])
            cl.get_timeline_feed()  # Test the session
            return cl
        except Exception:
            pass  # Session expired, do fresh login

    # Fresh login
    try:
        cl.login(ig["username"], ig["password"])
        if session_file.parent.exists():
            cl.dump_settings(session_file)
        return cl
    except Exception as e:
        print(f"Instagram login failed: {e}")
        sys.exit(1)


def post_instagram(args):
    """Post to Instagram."""
    cl = get_ig_client()
    caption = args.caption or ""

    if args.story:
        path = Path(args.story)
        if path.suffix.lower() in (".mp4", ".mov"):
            result = cl.video_upload_to_story(path, caption)
        else:
            result = cl.photo_upload_to_story(path, caption)
        print(f"Story posted: {result.dict().get('pk', 'success')}")

    elif args.reel:
        path = Path(args.reel)
        result = cl.clip_upload(path, caption)
        print(f"Reel posted: https://www.instagram.com/reel/{result.dict().get('code', '')}/")

    elif args.carousel:
        paths = [Path(p) for p in args.carousel]
        result = cl.album_upload(paths, caption)
        print(f"Carousel posted: https://www.instagram.com/p/{result.dict().get('code', '')}/")

    elif args.image:
        path = Path(args.image)
        result = cl.photo_upload(path, caption)
        print(f"Photo posted: https://www.instagram.com/p/{result.dict().get('code', '')}/")

    else:
        print("Specify --image, --carousel, --story, or --reel")
        sys.exit(1)


def post_twitter(args):
    """Post to Twitter/X."""
    import tweepy

    creds = load_credentials()
    tw = creds.get("twitter")
    if not tw:
        print("Twitter not configured. Run: python3 post.py setup twitter")
        sys.exit(1)

    client = tweepy.Client(
        consumer_key=tw["api_key"],
        consumer_secret=tw["api_secret"],
        access_token=tw["access_token"],
        access_token_secret=tw["access_secret"],
    )

    if args.thread:
        # Post thread: first tweet, then replies
        tweets = args.thread
        prev_id = None
        for i, text in enumerate(tweets):
            result = client.create_tweet(
                text=text,
                in_reply_to_tweet_id=prev_id,
            )
            tweet_id = result.data["id"]
            prev_id = tweet_id
            print(f"Tweet {i + 1}/{len(tweets)}: https://twitter.com/i/web/status/{tweet_id}")
        print(f"Thread posted ({len(tweets)} tweets)")

    elif args.text:
        result = client.create_tweet(text=args.text)
        tweet_id = result.data["id"]
        print(f"Posted: https://twitter.com/i/web/status/{tweet_id}")

    else:
        print("Specify --text or --thread")
        sys.exit(1)


def show_status():
    """Show which platforms are configured."""
    creds = load_credentials()
    platforms = {
        "instagram": "username",
        "twitter": "api_key",
    }
    print("BlackRoad Social Posting Tool — Status\n")
    for platform, key_field in platforms.items():
        conf = creds.get(platform, {})
        if conf.get(key_field):
            detail = conf.get("username", "configured")
            print(f"  {platform:12s}  READY  ({detail})")
        else:
            print(f"  {platform:12s}  NOT CONFIGURED")
    print(f"\n  Credentials: {CRED_FILE}")
    print(f"  IG Session:  {SESSION_DIR}/")


def main():
    parser = argparse.ArgumentParser(description="BlackRoad OS Social Posting Tool")
    subparsers = parser.add_subparsers(dest="command")

    # Setup
    setup_parser = subparsers.add_parser("setup", help="Configure a platform")
    setup_parser.add_argument("platform", choices=["instagram", "twitter"])

    # Status
    subparsers.add_parser("status", help="Show configured platforms")

    # Instagram
    ig_parser = subparsers.add_parser("instagram", aliases=["ig"], help="Post to Instagram")
    ig_parser.add_argument("--caption", "-c", help="Post caption")
    ig_parser.add_argument("--image", "-i", help="Image file path")
    ig_parser.add_argument("--carousel", nargs="+", help="Multiple images for carousel")
    ig_parser.add_argument("--story", help="Image/video for story")
    ig_parser.add_argument("--reel", help="Video for reel")

    # Twitter
    tw_parser = subparsers.add_parser("twitter", aliases=["tw", "x"], help="Post to X/Twitter")
    tw_parser.add_argument("--text", "-t", help="Tweet text")
    tw_parser.add_argument("--thread", nargs="+", help="Multiple tweets as a thread")

    args = parser.parse_args()

    if args.command == "setup":
        if args.platform == "instagram":
            setup_instagram()
        elif args.platform == "twitter":
            setup_twitter()
    elif args.command == "status":
        show_status()
    elif args.command in ("instagram", "ig"):
        post_instagram(args)
    elif args.command in ("twitter", "tw", "x"):
        post_twitter(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
