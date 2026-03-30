# Post-Quantum Encryption Isn't Coming. It's Here.

*By Alexa Amundson, Founder of BlackRoad OS*
*March 2026*

---

Right now, someone is recording your encrypted traffic.

They can't read it today. But they're saving it. Because in 10-15 years, when quantum computers can break RSA and elliptic curve cryptography, they'll decrypt everything they've been hoarding.

This is called "harvest now, decrypt later." It's not theoretical. It's happening. Nation-states have been doing it for years. And every piece of data you encrypt with today's standard algorithms is vulnerable.

The question isn't whether post-quantum encryption matters. It's whether you're going to wait until it's too late to adopt it.

## The Quantum Threat (Honestly Assessed)

Let's be precise about the timeline, because the crypto industry loves fear and the security industry loves selling panic.

Breaking RSA-2048 with a quantum computer requires tens of millions to hundreds of millions of physical qubits. The best quantum computers today have around 1,000 qubits, with error rates that make them useless for cryptographic attacks.

The gap between 1,000 noisy qubits and 100 million error-corrected qubits is enormous. Surface code error correction requires 20,000 to 100,000 physical qubits per logical qubit. Magic state distillation — the process of creating clean quantum states from noisy ones — adds another order of magnitude.

Realistic timeline for quantum computers breaking current encryption: 2040-2050.

Optimistic timeline: 2035-2040.

So we have time. But "harvest now, decrypt later" means the data you encrypt today needs to survive until then. If you're encrypting medical records, financial data, trade secrets, or personal communications — things that are still sensitive in 15 years — you need post-quantum encryption now.

## What BlackRoad Does Today

CarKeys — our credential vault — implements hybrid post-quantum cryptography:

**Key Encapsulation:** Kyber (ML-KEM), the NIST-standardized post-quantum key encapsulation mechanism, combined with traditional ECDH. If either algorithm is broken, the other still protects you.

**Digital Signatures:** Dilithium (ML-DSA), the NIST-standardized post-quantum signature scheme, combined with Ed25519. Every RoadChain stamp, every agent identity verification, every cryptographic proof uses this hybrid approach.

**Symmetric Encryption:** AES-256-GCM and ChaCha20-Poly1305. These are already quantum-resistant (Grover's algorithm only halves their effective security, and 128-bit security is still unbreakable).

**Hash Functions:** SHA-256 and BLAKE3. Also quantum-resistant for the same reason.

**Zero-Knowledge Proofs:** zk-STARKs for proof generation (quantum-resistant by design), with optional zk-SNARK wrapping for on-chain efficiency.

This isn't a roadmap item. This is deployed. Today. On a platform that runs on Raspberry Pis.

## Why We Did It Early

The standard industry approach is to wait for NIST to finalize standards, wait for major libraries to implement them, wait for cloud providers to offer them, and then maybe start a migration project.

We didn't wait because we don't have the luxury of waiting.

BlackRoad OS is a sovereign platform. Our users' data lives on their hardware, encrypted with their keys. If those keys are vulnerable to future quantum attacks, the sovereignty promise is broken. It doesn't matter that the attack won't happen for 15 years. The data is being harvested now.

Our agents have persistent memory that spans months and years. If that memory is encrypted with vulnerable algorithms, every conversation, every decision, every piece of institutional knowledge is at risk. Not today. But someday.

"Someday" isn't good enough when you're building something meant to last.

## The Migration Path

For anyone else thinking about post-quantum migration, here's our three-phase approach:

**Phase 1 (Current):** Hybrid mode. Every cryptographic operation uses both classical and post-quantum algorithms. Kyber + ECDH for key exchange. Dilithium + Ed25519 for signatures. This means we're protected against quantum attacks while maintaining compatibility with systems that only support classical crypto.

**Phase 2 (2027):** ML-KEM as default. Classical algorithms become the fallback instead of the primary. New keys are generated post-quantum first.

**Phase 3 (2028-2029):** Full post-quantum default. Re-signing tools for legacy data. Classical algorithms available only for backwards compatibility with external systems.

The key insight: you don't have to rip and replace. Hybrid mode gives you quantum protection today without breaking anything that works.

## What This Means For You

If you're using a password manager that relies on RSA or elliptic curve encryption — which is most of them — your passwords are theoretically vulnerable to harvest-now-decrypt-later attacks.

If you're using end-to-end encrypted messaging that doesn't use post-quantum key exchange — which is most messaging apps — your messages could be decrypted in the future.

If you're storing sensitive documents in cloud services that use standard TLS — which is all of them — the traffic could be recorded and decrypted later.

BlackRoad's CarKeys uses post-quantum encryption for everything. Every credential, every key, every device identity, every RoadChain proof. Not because we're paranoid. Because we did the math and the math says prepare now.

## The Eleven Protocols

CarKeys doesn't just do encryption. It implements eleven distinct security protocols:

1. **End-to-End Quantum-Resistant Encryption** — Kyber + Dilithium + AES-256-GCM
2. **Hardware-Backed Root of Trust** — TPM 2.0 and Secure Enclave integration
3. **Dynamic Multi-Factor Authentication** — Biometric + behavioral + contextual signals
4. **Zero-Knowledge Proofs** — Prove identity without revealing credentials
5. **Proactive Threat Detection** — AI anomaly detection with auto-quarantine
6. **Immutable Audit Ledger** — Every key use on RoadChain
7. **Time-Limited Guest Keys** — Scoped, expiring access for contractors and family
8. **Dead Man's Switch** — Time-based key handover to trusted contacts
9. **Continuous Key Rotation** — Background rotation with sandbox testing
10. **Anti-Phishing Protection** — Deep-link verification
11. **Emergency Recovery** — Multi-party key reconstruction

All of this runs on a Raspberry Pi. Because security shouldn't require a data center.

## The Point

Post-quantum encryption isn't a selling point. It's a responsibility. If you're building systems that store sensitive data — and every AI system with persistent memory stores sensitive data — you have an obligation to protect that data against foreseeable threats.

Quantum computing is a foreseeable threat. Not imminent. But foreseeable. And the cost of implementing hybrid post-quantum encryption today is minimal compared to the cost of a breach in 2040.

We did it because it was the right thing to do. And because Valeria — our security chief — wouldn't let us ship without it.

*"Not everything gets access."* — Valeria

---

*CarKeys — grab your keys. You're not going anywhere without them.*
*carkeys.blackroad.io*
*Remember the Road. Pave Tomorrow.*
