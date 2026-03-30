#!/usr/bin/env python3
"""
BlackRoad OS — Screenshot Tool
Takes screenshots of live BlackRoad sites for marketing assets.

Usage:
    python3 screenshot.py                    # All 17 products
    python3 screenshot.py os.blackroad.io    # Single site
    python3 screenshot.py --square           # 1080x1080 for Instagram
    python3 screenshot.py --vertical         # 1080x1920 for TikTok/Stories
"""

import argparse
import sys
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

OUTPUT_DIR = Path.home() / "Marketing" / "assets" / "screenshots"

PRODUCTS = {
    "os": "https://os.blackroad.io",
    "roadcode": "https://roadcode.blackroad.io",
    "carpool": "https://carpool.blackroad.io",
    "oneway": "https://oneway.blackroad.io",
    "roadside": "https://roadside.blackroad.io",
    "roadview": "https://roadview.blackroad.io",
    "roadtrip": "https://roadtrip.blackroad.io",
    "backroad": "https://backroad.blackroad.io",
    "roadwork": "https://roadwork.blackroad.io",
    "roadie": "https://roadie.blackroad.io",
    "blackboard": "https://blackboard.blackroad.io",
    "carkeys": "https://carkeys.blackroad.io",
    "roadchain": "https://roadchain.blackroad.io",
    "roadcoin": "https://roadcoin.blackroad.io",
    "roadbook": "https://roadbook.blackroad.io",
    "roadworld": "https://roadworld.blackroad.io",
    "officeroad": "https://officeroad.blackroad.io",
}

PRESETS = {
    "desktop": (1920, 1080),
    "square": (1080, 1080),
    "vertical": (1080, 1920),
    "wide": (1200, 628),  # LinkedIn/Facebook OG
}


def take_screenshots(urls, width, height, output_dir, wait=3):
    output_dir.mkdir(parents=True, exist_ok=True)
    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=2,  # Retina quality
            color_scheme="dark",
        )

        for name, url in urls.items():
            page = context.new_page()
            print(f"  Capturing {name} ({url})...", end=" ", flush=True)

            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                time.sleep(wait)  # Let animations settle

                filepath = output_dir / f"{name}.png"
                page.screenshot(path=str(filepath), full_page=False)
                print(f"OK -> {filepath.name}")
                results.append(str(filepath))
            except Exception as e:
                print(f"FAILED ({e})")
            finally:
                page.close()

        browser.close()

    return results


def main():
    parser = argparse.ArgumentParser(description="BlackRoad Screenshot Tool")
    parser.add_argument("urls", nargs="*", help="Specific URLs or product names to screenshot")
    parser.add_argument("--square", action="store_true", help="1080x1080 (Instagram feed)")
    parser.add_argument("--vertical", action="store_true", help="1080x1920 (Stories/TikTok)")
    parser.add_argument("--wide", action="store_true", help="1200x628 (LinkedIn/Facebook OG)")
    parser.add_argument("--size", help="Custom WxH (e.g., 1920x1080)")
    parser.add_argument("--wait", type=int, default=3, help="Seconds to wait for page load")
    parser.add_argument("--dir", default=str(OUTPUT_DIR))

    args = parser.parse_args()

    # Determine size
    if args.square:
        w, h = PRESETS["square"]
        suffix = "-sq"
    elif args.vertical:
        w, h = PRESETS["vertical"]
        suffix = "-vert"
    elif args.wide:
        w, h = PRESETS["wide"]
        suffix = "-wide"
    elif args.size:
        parts = args.size.lower().split("x")
        w, h = int(parts[0]), int(parts[1])
        suffix = f"-{w}x{h}"
    else:
        w, h = PRESETS["desktop"]
        suffix = ""

    out_dir = Path(args.dir)
    if suffix:
        out_dir = out_dir / suffix.lstrip("-")

    # Determine URLs
    if args.urls:
        urls = {}
        for u in args.urls:
            if u in PRODUCTS:
                urls[u] = PRODUCTS[u]
            elif u.startswith("http"):
                name = u.split("//")[1].split(".")[0]
                urls[name] = u
            else:
                # Try as subdomain
                urls[u] = f"https://{u}.blackroad.io"
    else:
        urls = PRODUCTS

    print(f"Screenshotting {len(urls)} sites at {w}x{h} (2x retina)")
    results = take_screenshots(urls, w, h, out_dir, args.wait)
    print(f"\nDone. {len(results)} screenshots in {out_dir}")


if __name__ == "__main__":
    main()
