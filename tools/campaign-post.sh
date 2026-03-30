#!/bin/bash
# BlackRoad OS — Campaign Poster
# Posts campaign content from the Marketing repo to configured platforms.
#
# Usage:
#   ./campaign-post.sh status           # Check which platforms are ready
#   ./campaign-post.sh setup instagram  # Configure Instagram credentials
#   ./campaign-post.sh setup twitter    # Configure Twitter/X credentials
#   ./campaign-post.sh instagram <image> [carousel_img2 carousel_img3 ...]
#   ./campaign-post.sh twitter          # Post the primary tweet
#   ./campaign-post.sh twitter-thread   # Post the full 7-tweet thread
#   ./campaign-post.sh all <image>      # Post everywhere at once

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CAMPAIGN_DIR="$SCRIPT_DIR/../campaigns/launch-2026"
POST_PY="$SCRIPT_DIR/post.py"

PINK='\033[38;5;205m'
GREEN='\033[38;5;82m'
BLUE='\033[38;5;69m'
RESET='\033[0m'

case "${1:-help}" in
  status)
    python3 "$POST_PY" status
    ;;

  setup)
    python3 "$POST_PY" setup "${2:?Specify platform: instagram or twitter}"
    ;;

  instagram|ig)
    shift
    if [ $# -eq 0 ]; then
      echo "Usage: $0 instagram <image.jpg> [image2.jpg image3.jpg ...]"
      exit 1
    fi

    # Extract Instagram caption from campaign file
    CAPTION=$(sed -n '/^## Caption$/,/^---$/p' "$CAMPAIGN_DIR/instagram.md" | grep -v '^##\|^---' | sed '/^$/d')

    if [ $# -eq 1 ]; then
      echo -e "${PINK}Posting to Instagram...${RESET}"
      python3 "$POST_PY" instagram --caption "$CAPTION" --image "$1"
    else
      echo -e "${PINK}Posting carousel to Instagram ($# images)...${RESET}"
      python3 "$POST_PY" instagram --caption "$CAPTION" --carousel "$@"
    fi
    echo -e "${GREEN}Instagram posted.${RESET}"
    ;;

  twitter|tw|x)
    # Extract primary tweet from campaign file
    TWEET=$(sed -n '/^## Primary Tweet$/,/^---$/p' "$CAMPAIGN_DIR/twitter.md" | grep -v '^##\|^---' | sed '/^$/d')

    echo -e "${BLUE}Posting to X/Twitter...${RESET}"
    python3 "$POST_PY" twitter --text "$TWEET"
    echo -e "${GREEN}Tweet posted.${RESET}"
    ;;

  twitter-thread|thread)
    echo -e "${BLUE}Posting thread to X/Twitter (7 tweets)...${RESET}"

    # Extract each tweet from the thread
    T1=$(sed -n '/^## Primary Tweet$/,/^---$/p' "$CAMPAIGN_DIR/twitter.md" | grep -v '^##\|^---' | sed '/^$/d')
    T2=$(sed -n '/^### Tweet 2$/,/^### Tweet 3$/p' "$CAMPAIGN_DIR/twitter.md" | grep -v '^###' | sed '/^$/d')
    T3=$(sed -n '/^### Tweet 3$/,/^### Tweet 4$/p' "$CAMPAIGN_DIR/twitter.md" | grep -v '^###' | sed '/^$/d')
    T4=$(sed -n '/^### Tweet 4$/,/^### Tweet 5$/p' "$CAMPAIGN_DIR/twitter.md" | grep -v '^###' | sed '/^$/d')
    T5=$(sed -n '/^### Tweet 5$/,/^### Tweet 6$/p' "$CAMPAIGN_DIR/twitter.md" | grep -v '^###' | sed '/^$/d')
    T6=$(sed -n '/^### Tweet 6$/,/^### Tweet 7$/p' "$CAMPAIGN_DIR/twitter.md" | grep -v '^###' | sed '/^$/d')
    T7=$(sed -n '/^### Tweet 7$/,/^---$/p' "$CAMPAIGN_DIR/twitter.md" | grep -v '^###\|^---' | sed '/^$/d')

    python3 "$POST_PY" twitter --thread "$T1" "$T2" "$T3" "$T4" "$T5" "$T6" "$T7"
    echo -e "${GREEN}Thread posted (7 tweets).${RESET}"
    ;;

  all)
    shift
    IMAGE="${1:?Provide an image path for Instagram}"
    echo -e "${PINK}Posting to ALL platforms...${RESET}"
    "$0" instagram "$IMAGE"
    "$0" twitter
    echo -e "${GREEN}All platforms posted.${RESET}"
    ;;

  help|*)
    echo "BlackRoad OS — Campaign Poster"
    echo ""
    echo "Usage:"
    echo "  $0 status              Check configured platforms"
    echo "  $0 setup instagram     Set up Instagram credentials"
    echo "  $0 setup twitter       Set up Twitter/X credentials"
    echo "  $0 instagram <img>     Post to Instagram (single image)"
    echo "  $0 instagram <img1> <img2> ...   Post carousel"
    echo "  $0 twitter             Post primary tweet"
    echo "  $0 twitter-thread      Post full 7-tweet thread"
    echo "  $0 all <img>           Post to all platforms at once"
    ;;
esac
