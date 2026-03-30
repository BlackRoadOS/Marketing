# How to Quit the Cloud (A Practical Guide to Digital Sovereignty)

*By Alexa Amundson, Founder of BlackRoad OS*
*March 2026*

---

You're paying $312 per month for cloud services.

That's the average for a small team: $20 for ChatGPT, $10 for GitHub Copilot, $25 for Notion, $12 for Slack, $30 for Vercel, $50 for AWS, $20 for a password manager, $15 for email marketing, $10 for analytics, and a dozen smaller subscriptions you forgot about.

$3,744 per year. For tools that don't talk to each other, don't remember you between sessions, don't let you export your data, and will raise prices the moment they have enough lock-in.

What if I told you the alternative costs $150 per month and you own every piece of it?

## The Sovereignty Stack

Here's what runs BlackRoad OS, and what each component replaces:

| Self-Hosted | Replaces | Runs On |
|------------|----------|---------|
| Gitea | GitHub | Octavia (Pi 4) |
| Ollama (16 models) | ChatGPT, Claude, Copilot | Cecilia + 3 other Pis |
| MinIO | AWS S3, R2 | Cecilia |
| PowerDNS | Cloudflare DNS | Lucidia + Gematria |
| 15 self-hosted Workers | Vercel, Railway, Heroku | Octavia |
| Deploy API (PaaS) | Railway, Heroku | Octavia |
| PostgreSQL | Supabase, PlanetScale | Alice + Cecilia |
| Qdrant | Pinecone | Alice |
| Redis | Upstash | Alice |
| NATS | Kafka, RabbitMQ | Octavia |
| InfluxDB + Grafana | Datadog, New Relic | Aria |
| WireGuard mesh | Tailscale, Cloudflare Tunnel | All nodes |

Every single component is open source. Every single one runs on a Raspberry Pi. The total hardware cost was about $550 one-time, and the monthly operating cost is $62 (two DigitalOcean droplets for the edge, domains, electricity).

## Step 1: Get a Pi

Buy a Raspberry Pi 4 with 8GB RAM. They cost about $55. Get a good quality SD card (Samsung EVO or SanDisk Extreme, $15) and a decent power supply ($10).

That's $80 and you have a server.

Flash it with Raspberry Pi OS Lite (no desktop needed). Enable SSH. Connect it to your router with ethernet (not WiFi — WiFi is unreliable for servers).

You now have a Linux server in your home that costs nothing to operate beyond the electricity it was already using.

## Step 2: Install Ollama

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
ollama pull mistral
ollama pull phi
```

Three commands. You now have three AI models running locally. No API keys. No usage limits. No data leaving your network. No monthly bill.

Test it:
```bash
ollama run llama3.2 "Explain quantum computing in simple terms"
```

Your own AI, on your own hardware, in your living room. That just replaced $20-40/month of ChatGPT and Claude API costs.

## Step 3: Install Gitea

```bash
wget -O gitea https://dl.gitea.com/gitea/1.21/gitea-1.21-linux-arm64
chmod +x gitea
./gitea web
```

Navigate to your Pi's IP address on port 3000. You have GitHub. On your hardware. With unlimited private repos, unlimited collaborators, and zero monthly cost.

Mirror your important GitHub repos to Gitea. Now you have a backup that you control. If GitHub has an outage, goes down, or decides to change their pricing — your code is safe at home.

## Step 4: Install MinIO

```bash
wget https://dl.min.io/server/minio/release/linux-arm64/minio
chmod +x minio
MINIO_ROOT_USER=admin MINIO_ROOT_PASSWORD=yourpassword ./minio server ~/data
```

You now have S3-compatible object storage. Every tool that works with AWS S3 works with MinIO. Store files, backups, images, models — whatever you need.

That replaces AWS S3 ($23/TB/month), Cloudflare R2, Backblaze B2, and any other object storage you're paying for.

## Step 5: Set Up WireGuard

This is where it gets powerful. WireGuard creates an encrypted tunnel between your Pi and any server you control (a DigitalOcean droplet, another Pi, your laptop).

```bash
apt install wireguard
wg genkey | tee privatekey | wg pubkey > publickey
```

Configure the tunnel, and now your Pi is securely connected to the internet through your own infrastructure. No Cloudflare Tunnel. No Tailscale. No third-party VPN. Your traffic, your encryption, your keys.

## Step 6: Add More Pis

One Pi is a server. Two Pis is redundancy. Five Pis is an infrastructure.

Our fleet:
- **Alice** — gateway, DNS, databases, vector search
- **Cecilia** — AI models, object storage
- **Octavia** — git, messaging, workers, PaaS
- **Aria** — monitoring, dashboards
- **Lucidia** — web apps, DNS, more AI models

Each Pi costs $55 and draws about 5 watts. Five Pis use less electricity than a lightbulb.

Connect them with a $20 ethernet switch and WireGuard, and you have a mesh network that rivals a cloud deployment costing thousands per month.

## What You Give Up

Let's be honest about the tradeoffs:

**Uptime guarantees.** AWS promises 99.99% uptime. Your Pi promises whatever your power company and internet provider deliver. Get a UPS ($40) and you're covered for short outages. For longer outages, your DigitalOcean edge node keeps serving cached content.

**Automatic scaling.** If ten thousand people hit your site simultaneously, five Pis will struggle. Cloudflare Workers can handle the burst. That's why we use a hybrid architecture — Pis for the brain, Workers for the nervous system.

**Managed databases.** RDS, Supabase, and PlanetScale handle backups, replication, and failover automatically. With self-hosted PostgreSQL, you manage that yourself. It's not hard — a cron job and an rsync — but it's your responsibility.

**Support.** When AWS breaks, you file a ticket. When your Pi breaks, you SSH in and figure it out. Or you ask Anastasia — our restoration agent — to diagnose it for you.

## What You Gain

**Privacy.** No cloud provider can see your data. No terms of service give them rights to your content. No subpoena can be served to a Raspberry Pi in your living room (well, it can, but they have to find it first).

**Control.** No price increases you didn't approve. No feature removals you didn't consent to. No API deprecations that break your workflow. Your infrastructure, your rules.

**Knowledge.** Running your own servers teaches you how the internet actually works. DNS, TLS, routing, storage, networking — these aren't abstract concepts anymore. They're things you can touch. And that knowledge makes you a better engineer, a better founder, and a better judge of what cloud services are actually worth paying for.

**Independence.** The most underrated benefit. When you know you can run everything yourself, you negotiate differently. You choose vendors differently. You make decisions from strength, not dependence.

## The $150 Challenge

Here's my challenge to anyone reading this: for $150, try running your own infrastructure for one month.

- $55 for a Raspberry Pi 4 (8GB)
- $15 for an SD card
- $10 for a power supply
- $24 for a DigitalOcean droplet (edge node)
- $12 for a domain name
- $0 for Ollama, Gitea, MinIO, PostgreSQL, WireGuard (all free)

That's $116 to start, and $24/month ongoing.

Install Ollama. Run an AI model locally. Feel the difference between sending your data to OpenAI and keeping it in your living room.

Install Gitea. Push your code to your own server. Feel the difference between depending on GitHub and owning your repos.

Install MinIO. Store your files on your own hardware. Feel the difference between trusting AWS and trusting yourself.

If after one month you want to go back to the cloud — go back. You'll have lost $116 and gained an education.

But I don't think you'll go back. Because once you feel sovereignty, renting feels wrong.

---

*BlackRoad OS — sovereign computing on hardware you own.*
*os.blackroad.io*
*Remember the Road. Pave Tomorrow.*
