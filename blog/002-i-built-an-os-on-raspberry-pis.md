# I Built a Sovereign Operating System on Five Raspberry Pis

*By Alexa Amundson, Founder of BlackRoad OS*
*March 2026*

---

The total infrastructure cost of BlackRoad OS — a browser-based operating system with 17 products, 27 AI agents, persistent memory, blockchain verification, and a token economy — is $150 per month.

That's not a typo. That's five Raspberry Pis, two DigitalOcean droplets, and a Cloudflare account.

Here's how, and more importantly, why.

## The Hardware

My living room has a stack of five Raspberry Pis connected by ethernet cables and an encrypted WireGuard mesh network:

- **Alice** (Pi 4, 192.168.4.49) — Gateway, Pi-hole DNS, PostgreSQL, Qdrant vector DB, Redis, nginx routing 37 sites
- **Cecilia** (Pi 4, 192.168.4.105) — Ollama running 16 local AI models, MinIO object storage, PostgreSQL, InfluxDB
- **Octavia** (Pi 4, 192.168.4.101) — Gitea (our primary git host), NATS messaging, Docker, 15 self-hosted workers
- **Aria** (Pi 4, 192.168.4.98) — Portainer, Headscale VPN, InfluxDB, Grafana, Ollama
- **Lucidia** (Pi 4, 192.168.4.38) — 334 web apps, nginx, PowerDNS, GitHub Actions runners, Ollama

Two of them have Hailo-8 AI accelerators — 26 TOPS each, 52 TOPS total. That's enough to run real-time AI inference locally without ever calling an external API.

Two DigitalOcean droplets in NYC provide the edge:
- **Gematria** — Caddy TLS termination for 151 domains, Ollama, PowerDNS
- **Anastasia** — Backup and recovery node

Internet hits Gematria, travels through WireGuard to the Pi fleet, and comes back. The whole path is encrypted.

## Why Raspberry Pis

The question I get asked most: "Why not just use AWS?"

Because then it wouldn't be mine.

When you run on AWS, Amazon can see your traffic, your data, your patterns. They can raise prices. They can change terms of service. They can shut you down. You are a tenant in their building and they hold the keys.

When you run on a Raspberry Pi in your living room, you hold the keys. Literally — the SD card is in your hand. If Cloudflare disappeared tomorrow, I'd point DNS at my own PowerDNS servers and keep serving. If GitHub went down, Gitea on Octavia has every repo. If OpenAI cut me off, Ollama on Cecilia has 16 models ready to go.

That's not paranoia. That's engineering for independence.

## The Architecture

BlackRoad OS uses what we call the "circuit and lightbulb" architecture:

- **Lightbulbs** = Cloudflare Workers serving the static HTML for each product
- **Circuits** = Cloudflare Workers handling the API backends, connected to D1 databases

The static sites are lightweight — pure HTML/CSS/JS, no build step, no framework. The API workers handle data, authentication, and business logic against D1 (SQLite at the edge).

For AI inference, requests route through the WireGuard mesh to whichever Pi has the right model loaded. Cecilia handles most Ollama requests. The Hailo-8 accelerators handle vision and real-time inference.

For anything that needs scale beyond what five Pis can handle, Cloudflare Workers pick up the overflow. But the Pis are the brain. Workers are the nervous system.

## The Numbers

| Component | Cost |
|-----------|------|
| 5x Raspberry Pi 4 (one-time) | ~$250 total |
| 2x Hailo-8 accelerators (one-time) | ~$200 total |
| SD cards, cables, ethernet switch (one-time) | ~$100 |
| 2x DigitalOcean droplets | $24/month |
| Cloudflare Pro | $25/month |
| Domain registrations (20 domains) | ~$100/year (~$8/month) |
| Electricity | ~$5/month |
| Internet | Already paying for it |
| **Monthly total** | **~$62/month** |

I round up to $150 to account for occasional costs like SD card replacements and the Stripe subscription.

For that $150, I run:
- 17 products with 150 API endpoints
- 27 AI agents with persistent memory
- 466 Cloudflare Workers
- 35 D1 databases
- 59 KV namespaces
- 13 R2 storage buckets
- 239 git repositories on self-hosted Gitea
- Full blockchain verification layer
- Token economy

A comparable setup on AWS — with managed databases, Lambda functions, S3 storage, AI inference, and the networking to connect it all — would cost $5,000-15,000 per month. I know because I priced it.

## What I Learned

**1. Constraints are features.** A Raspberry Pi has 8GB of RAM. That means you can't be lazy. You can't spin up a Kubernetes cluster for a TODO app. You have to think about every byte, every process, every connection. The result is software that's lean, fast, and efficient — because it had to be.

**2. Sovereignty is a state of mind.** Once you realize you can run everything yourself, you stop accepting dependencies you don't need. Slack is great, but do I need it? Or can I build sovereign chat on my own infrastructure? (I built it.) GitHub is great, but do I need it? Or can I run Gitea? (I run Gitea.)

**3. The physical is grounding.** There's something irreplaceable about being able to see your infrastructure. I can watch the LED on Alice blink when a request comes in. I can feel Cecilia get warm when Ollama is running inference. The cloud is abstract. A Raspberry Pi is real. And when you're building something that matters to you, real matters.

**4. Nobody cares how you built it. They care that it works.** Users don't see the Pis. They see a desktop in their browser. They see an AI tutor that remembers them. They see a social automation tool that posts on their behalf. The infrastructure is invisible — and that's the point. Sovereign doesn't mean primitive. It means independent.

## The Road Ahead

The Pis aren't a temporary solution. They're the permanent foundation. As BlackRoad grows, we'll add more Pis, more Hailo accelerators, more nodes to the mesh. The architecture scales horizontally — add a Pi, add capacity.

When we hit the limits of what Pis can do — and that day will come — we'll add dedicated servers. But they'll be our servers. In our rack. On our network. Connected by our mesh.

The sovereignty is non-negotiable. The road was built on hardware we own, and it will always run on hardware we own.

$150 a month. Seventeen products. Twenty-seven agents. One living room.

If that sounds impossible, it's because you've been told infrastructure has to be expensive. It doesn't. It just has to be yours.

---

*BlackRoad OS — sovereign computing on hardware you own.*
*os.blackroad.io*
*Remember the Road. Pave Tomorrow.*
