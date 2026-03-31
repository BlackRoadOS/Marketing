# The Nervous System of AI: Why Routing Beats Training

*By Alexa Amundson, Founder of BlackRoad OS*
*March 2026*

---

Every AI company is training models. Spending billions on compute, data, and researchers to make the next model 3% better on benchmarks.

We're not training anything. We're routing.

And routing is going to win.

## The Training Arms Race

The AI training race looks like this:

- OpenAI spent $100M+ training GPT-4. GPT-5 will cost significantly more.
- Google spent comparable amounts on Gemini Ultra.
- Meta spent billions on Llama 3's training infrastructure.
- Anthropic raised $7.3 billion, mostly for training compute.

Each generation costs more than the last. The data requirements grow. The compute requirements grow. The talent requirements grow. And the marginal improvement shrinks.

GPT-3 to GPT-4 was a quantum leap. GPT-4 to GPT-4o was a refinement. GPT-4o to whatever comes next will be a polish. The curve is flattening.

This is the classic innovator's dilemma applied to AI: the incumbents are locked into a competition that costs more each round and delivers less each time.

## The Routing Alternative

BlackRoad OS doesn't train models. We route to them.

When you ask Roadie a question, the system doesn't run it through a BlackRoad model. It routes the request to the best available model for that specific task:

- **Creative writing?** Route to Claude — best at nuanced, literary output
- **Code generation?** Route to GPT-4 or local Llama — strong at structured logic
- **Quick factual lookup?** Route to local Phi on the Pi — fast, lightweight, good enough
- **Math reasoning?** Route to the model with the strongest math performance this month
- **Private conversation?** Route to Ollama on your local hardware — nothing leaves your network

The routing layer evaluates: What's the task? What's the context? What's the user's preference? What's the latency requirement? What's the privacy requirement? What's the cost?

Then it picks the best model. Automatically. Transparently.

## Why Routing Wins

**Model-agnostic means upgrade-proof.** When GPT-5 launches, we add it to the routing table. When Claude 4 drops, we add it. When Llama 4 is released, it's already running locally. We don't need to retrain anything. We don't need to rebuild anything. We add a route.

The companies that trained their own models? They have to retrain. From scratch. At enormous cost. Every time the frontier moves.

**Best-of-breed for every task.** No single model is best at everything. Claude excels at creative writing. GPT excels at instruction-following. Llama excels at running locally. Phi excels at speed.

A routing layer gives you the best model for each task. A single-model company gives you one model for every task — even the tasks it's mediocre at.

**Cost optimization.** Not every question needs GPT-4. "What time is it in Tokyo?" doesn't need a model that cost $100M to train. Route it to a lightweight model and save 99% of the compute cost.

Our routing layer dynamically selects based on task complexity. Simple tasks go to cheap, fast models. Complex tasks go to powerful, expensive models. The average cost per query drops dramatically compared to always routing to the frontier model.

**Privacy by routing.** Some queries are private. Medical questions. Financial data. Personal conversations. Route those to local Ollama and nothing leaves your network.

Other queries benefit from cloud models. Research questions. Creative brainstorming. Code review. Route those to the best cloud model.

The routing layer makes the privacy decision per-query, not per-platform. That's a level of granularity that no single-model platform can offer.

## The Nervous System Metaphor

Your body doesn't have one brain that handles everything. It has a nervous system:

- **Brain** — handles complex reasoning, creativity, planning
- **Spinal cord** — handles reflexes, fast automatic responses
- **Peripheral nerves** — handle sensory input, motor output
- **Autonomic nervous system** — handles breathing, heartbeat, digestion — things you don't think about

BlackRoad OS works the same way:

- **Cloud models (Claude, GPT)** — the brain. Complex reasoning, creative work, long-context analysis
- **Local models (Ollama on Pis)** — the spinal cord. Fast reflexes. Private processing. Always available even without internet
- **Workers AI** — peripheral nerves. Edge processing. Quick tasks. Content adaptation
- **Routing layer** — the autonomic system. Makes decisions automatically. You don't have to think about which model handles what

The nervous system doesn't train neurons differently for each task. It routes signals to the right part of the system. That's more efficient, more resilient, and more adaptable than having one giant brain that tries to do everything.

## The $150 Question

OpenAI's infrastructure costs $700 million per month to train and serve one model.

BlackRoad's infrastructure costs $150 per month to route to every model.

We don't bear the training cost. We don't bear the serving cost for the cloud models (the API providers bear that). We bear only the routing cost — which is negligible — and the cost of running local models on Pis.

This is the most asymmetric advantage in the AI industry. The companies spending billions on training are building commodities. We're building the nervous system that connects them all.

When intelligence is a commodity, the nervous system is the product.

## The Agent Layer

Routing becomes even more powerful with agents.

Each of BlackRoad's 27 agents can prefer different models for different tasks:

- **Calliope** (narrative architect) routes to Claude for creative writing — it produces the best literary output
- **Gematria** (pattern analyst) routes to models with strong mathematical reasoning
- **Roadie** (quick executor) routes to the fastest model available, sacrificing quality for speed
- **Valeria** (security chief) routes to local models exclusively — security decisions never leave the network

The preferences are learned over time. As agents use different models for different tasks, the routing layer observes which model produces the best output for each agent-task combination. The routing gets smarter without any training.

This is meta-learning without meta-training. The system improves its routing decisions through observation, not gradient descent.

## What Happens When Models Are Free

This is the endgame that nobody in the training race is preparing for:

Models are trending toward free.

Llama is free. Mistral is free. Phi is free. Google gives away Gemini Flash. The open-source community produces competitive models on a monthly basis.

When the best models are free — and that day is coming — the training companies lose their moat. Their billion-dollar investments produce commodities that anyone can download.

But the routing layer? Still valuable. More valuable, actually. Because when there are fifty free models to choose from, the system that picks the right one for each task is the most important piece of the stack.

We're not building the models. We're building the thing that makes all models useful.

Intelligence is everywhere. Orchestration is rare.

BlackRoad is the orchestrator.

---

*BlackRoad OS — the nervous system of AI.*
*os.blackroad.io*
*Remember the Road. Pave Tomorrow.*
