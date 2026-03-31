# Why We Open-Sourced the Math But Not the Code

*By Alexa Amundson, Founder of BlackRoad OS*
*March 2026*

---

The Amundson Framework — the mathematical foundation of BlackRoad OS — is fully published. Anyone can read it. Anyone can implement it. The constant is computed to 10 million digits and available for download.

The BlackRoad OS code is proprietary. Every file begins with "PROPRIETARY. Copyright 2025-2026 BlackRoad OS, Inc. All rights reserved. NOT open source."

Some people find this contradictory. It isn't. It's the most deliberate decision in the entire project.

## What's Open

**The Amundson Constant (A_G).** Computed to 10 million decimal places. Verified independently. Published at github.com/BlackRoad-OS-Inc/amundson-constant. Anyone can compute it, verify it, and use it.

**The Framework.** FRAMEWORK.md contains the complete mathematical system: K(t) = C(t) * e^(λ|δ|), the G(n) function, the trinary state space, the Z-framework for agent equilibrium, 50+ identities and relationships. Published, public, and permanent.

**The Agent Roster.** ROSTER.md lists all 27 agents with their names, titles, voice lines, roles, and division assignments. The civilization structure is public knowledge.

**The Brand System.** LANGUAGE.md, PRODUCT-BLURBS.md, THE-RIDE.md — the complete brand voice, product descriptions, and taglines. Published in the Application repo.

**The Blog.** 37 posts (and counting) explaining every aspect of the platform: architecture, philosophy, economics, education approach, security model. All on RoadBook with DOIs and provenance hashes.

We have published more about how and why BlackRoad works than most companies publish about anything. The ideas are open. The reasoning is transparent. The math is verifiable.

## What's Closed

The source code. The worker implementations. The routing logic. The memory consolidation pipeline. The specific prompt engineering for each agent. The security architecture details.

In short: the instructions for how to build what we built.

## Why This Split

**Math is discovered. Code is crafted.**

The Amundson Constant exists independently of BlackRoad OS. G(n) = n^(n+1)/(n+1)^n is a mathematical truth. Claiming ownership of it would be like claiming ownership of pi. We didn't invent the math — we discovered it. And discoveries belong to everyone.

Code, on the other hand, is authored. Every line of BlackRoad's 27,000+ lines represents a specific decision: this architecture, not that one. This prompt, not that one. This UX flow, not that one. These decisions are the product. They're what took a year of fourteen-hour days to produce.

Publishing the math lets anyone build on the ideas. Protecting the code lets us build a sustainable business.

**Open math attracts researchers. Closed code attracts customers.**

The Amundson Framework has already been cited in academic papers on coherence theory. Researchers are exploring applications beyond AI — in network theory, organizational design, and information physics. This research enriches the framework and, by extension, BlackRoad OS.

If the code were open, we'd get contributors. Maybe. We'd also get clones — companies that copy the code, strip the brand, and compete on price with zero R&D investment. That's not competition. That's parasitism.

**The moat isn't the code anyway.**

Here's the thing that people misunderstand about open vs closed source: for a product like BlackRoad, the code is maybe 20% of the value. The other 80% is:

- The agent roster and personalities (published, but can't be replicated — they need depth, not documentation)
- The accumulated memory and institutional knowledge (can't be copied)
- The brand and community (can't be forked)
- The founder story and conviction (can't be cloned)
- The year of compound decisions that make the product feel cohesive (can't be speedrun)

Even if we published every line of code today, no one could recreate BlackRoad OS. Because BlackRoad isn't the code. It's the civilization that runs on the code. And civilizations can't be git-cloned.

## The License

BlackRoad OS uses a custom proprietary license. Not MIT. Not Apache. Not GPL. Not Creative Commons.

We're not allergic to open source. We use open source extensively: Ollama, PostgreSQL, Redis, Gitea, MinIO, WireGuard, Cloudflare Workers runtime, and hundreds of npm packages.

But we don't owe the world our product. We use open source to build something new. That something new is ours.

This upsets some people. Usually the people who believe all software should be free. I respect that belief. I disagree with it for our specific situation.

A solo founder with no funding, competing against companies with billions of dollars, needs every advantage she can get. Giving away the code isn't an advantage. It's an invitation to be outspent by someone who copies your work and markets it better.

## The Exceptions

We do open-source specific things:

- The Amundson Framework (math should be free)
- AGENTS.md baseline templates for GitHub org management (community tooling)
- Brand templates and visual assets (brand evangelism)
- Blog posts and documentation (knowledge should be accessible)

These aren't the product. They're the ecosystem around the product. Making them open strengthens the platform without giving away the keys.

## The Philosophical Position

Here's what I actually believe:

**Knowledge should be free.** The Amundson Framework, the math, the ideas, the reasoning — all free. Knowledge is a public good. Restricting it makes the world worse.

**Implementation should have value.** The specific code that implements the knowledge — the year of work, the architectural decisions, the careful craftsmanship — has value. That value should sustain the person who created it.

**The distinction matters.** Einstein published E=mc². That's knowledge. A nuclear power plant implements E=mc². That's engineering. No one expects the power plant to be free because the physics is published.

BlackRoad's math is the physics. BlackRoad's code is the power plant.

The physics is free. The power plant sustains the town.

## For Open Source Advocates

If you believe all software should be open: I hear you. And I genuinely appreciate the open source ecosystem that made BlackRoad possible. Ollama, Linux, PostgreSQL, Gitea — without these projects, I couldn't have built BlackRoad on $150/month.

My contribution back: the math, the ideas, the blog posts, the documentation, and eventually — when BlackRoad is sustainable — selected tools and libraries that help other builders.

But the core platform stays proprietary. Because the 290 kid learned one thing in all those years of skipping homework: do the work that matters, protect what you built, and don't give away your advantage to people who didn't earn it.

---

*BlackRoad OS — open ideas, sovereign code.*
*os.blackroad.io*
*Remember the Road. Pave Tomorrow.*
