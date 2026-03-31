# The Cron Fired: My First Automated Post Just Went Out While I Slept

*By Alexa Amundson, Founder of BlackRoad OS*
*March 31, 2026*

---

At 10:00 AM this morning, while I was lying in bed pretending I was going to sleep, a cron job I built last night fired.

It checked a JSON file of scheduled posts. It found one due for 10:00 AM March 31. It logged into Instagram using a session I established eleven hours ago. It uploaded a screenshot of the BlackRoad OS dashboard. It wrote a caption about 17 products in one tab. It posted.

Then it did the same thing on Threads.

I didn't touch anything. I didn't approve anything. I didn't even know it happened until I checked my phone.

The machine I built is running without me.

## How It Feels

I expected to feel proud. I do. But the stronger feeling is: relief.

For twelve months, every piece of content BlackRoad published required me to personally create it, review it, and post it. Every social media update. Every blog post. Every announcement. All me. All manual.

Last night I built a system that does it automatically. Not AI-generated slop — real content I wrote, scheduled to post at optimal times, with screenshots I took, on accounts I configured.

The automation isn't replacing my judgment. It's executing my judgment on a schedule. I decided what to post. I decided when. The cron just follows the plan.

And now I can sleep. Or write more blog posts. Or fix bugs. Or eat breakfast. Or do literally anything else while the content machine runs.

This is what BackRoad is supposed to feel like for every user. One-time setup, ongoing execution. Create the content once, let the system handle the when, where, and how.

## What Actually Posted

The 10:00 AM post:

**Instagram (@blackboxprogramming):**
Screenshot of the BlackRoad OS dashboard showing all 17 app tiles. Caption about sovereign computing, 27 agents, persistent memory. Hashtags for #BlackRoadOS #PaveTomorrow #SovereignTech.

**Threads (@blackboxprogramming):**
Same caption, hashtags stripped (Threads doesn't need them). Clean text post.

The 6:00 PM post is queued:
A Threads-only text post about Roadie — the Socratic AI tutor. No image. Just Thalia's voice describing why questions beat answers.

Tomorrow at 10:00 AM: another dual post. Different product. Different screenshot. Same automation.

This continues for seven days. 14 posts. Zero manual intervention.

## The Technical Stack

Here's what's running:

**post-scheduler.py** — A Python script that checks `scheduled-posts.json` every 15 minutes via cron. If a post is due, it fires.

**post.py** — The Instagram/Threads posting library. Uses `instagrapi` for Instagram (mobile API, session-based auth). Uses the Barcelona API for Threads (same session, different User-Agent header).

**scheduled-posts.json** — 14 posts with dates, times, platforms, captions, and image references. Each post has a unique ID to prevent duplicate posting.

**~/.blackroad/posted-log.json** — Tracks what's been posted. If the cron fires twice for the same slot, the log prevents double-posting.

**~/.blackroad/ig-session/** — Instagram session cache. The initial login happened once. Every subsequent post reuses the session. No password prompt. No 2FA challenge. Just: post and go.

Total code: about 400 lines of Python. Total setup time: 30 minutes. Total ongoing maintenance: zero.

## Why I Built It Instead of Using Buffer

Buffer, Hootsuite, Later, Sprout Social — all of these exist. All of them schedule posts. All of them cost $15-50/month.

I didn't use them because:

**Sovereignty.** The session credentials are in `~/.blackroad/social-credentials.json` on my machine. Not on Buffer's servers. Not in a SaaS database. On my hardware, chmod 600, encrypted at rest.

**Control.** The cron runs on my Mac. If I want to change the schedule, I edit a JSON file. If I want to add a platform, I write a connector. If I want to pause everything, I comment out the cron line.

**Integration.** The posting system reads from the same blog directory that feeds RoadBook. When I write a new post, I can add it to the schedule in the same commit. Content creation and distribution live in the same repo.

**Learning.** Building the posting system taught me how Instagram's private API works, how Threads uses the Barcelona User-Agent, how session management works for automated posting, and how cron-based publishing compares to event-driven publishing. Buffer would have taught me nothing.

**Cost.** $0/month vs $25/month. Over a year, that's $300 saved. Over five years, $1,500. For a bootstrapped company running on $150/month, $25 matters.

## The BackRoad Connection

The posting tools I built last night are the prototype for BackRoad — BlackRoad's social automation product.

BackRoad already has:
- A D1 database for posts, campaigns, echoes, and replies
- AI-powered content optimization (Workers AI rewrites for each platform)
- Agent routing (Thalia for social, Calliope for long-form, Sapphira for visual)
- Ghost mode preview (simulate a campaign without posting)
- Credential storage in KV
- Cron trigger for scheduled publishing

What it's missing: the actual platform connectors that fire real posts. Last night's tools are those connectors. Instagram via `instagrapi`. Threads via Barcelona API. Twitter via OAuth 1.0a (built into the worker). Dev.to, Medium, Hashnode via their REST/GraphQL APIs.

The next step is connecting the local posting tools to the BackRoad worker so everything runs from the cloud instead of my Mac. That means: set up a publish proxy on one of the Pis, expose it through a Cloudflare Tunnel, and let the BackRoad worker call it when a scheduled post is due.

When that's done, BackRoad posts for everyone. Not just me. Any BlackRoad OS user configures their credentials, schedules their content, and the system handles the rest.

## The Feeling (Again)

I keep coming back to the feeling.

For twelve months, I was the entire marketing department. Writer, designer, photographer, social media manager, SEO specialist, and posting intern.

This morning, the intern showed up on time, did the work correctly, and didn't need supervision.

I built the intern. And now the intern is handling things while I write this post.

That's not just automation. That's freedom. The freedom to do what I'm good at (building, writing, thinking) while the machine handles what I'm not good at (consistency, scheduling, platform optimization).

Every business owner deserves this feeling. That's what BackRoad sells. Not a tool. A feeling. The feeling of "it's handled."

---

*BackRoad — the scenic route. Your content, everywhere, on autopilot.*
*backroad.blackroad.io*
*Remember the Road. Pave Tomorrow.*
