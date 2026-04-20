# compute-commons

> An open specification for provider-agnostic AI inference compute accounting.

**Status**: RFC Draft · Est. 2026.04  
**Author**: [@pzy19-prog](https://github.com/pzy19-prog)  
**Related**: [pzy-v5](https://github.com/pzy19-prog/pzy-v5) — reference implementation

---

## The Problem

You pay for AI compute in tokens, API calls, GPU-hours — each provider uses different units, different pricing models, different billing granularities. There is no common unit of account.

This makes it impossible to:
- Compare costs across providers on equal footing
- Build portable budgeting systems that survive provider switches
- Reason about compute as a fungible, measurable resource

---

## The Proposal

Define a **Compute Unit (CU)** — a provider-agnostic atomic unit of AI inference work — and a protocol for how providers declare, exchange, and account for compute in these units.

Like currency exchange: providers declare their exchange rate to CU, and consumers reason in CU regardless of which provider they use.

---

## RFCs

| # | Title | Status |
|---|-------|--------|
| [RFC-0001](rfcs/RFC-0001-compute-unit.md) | Compute Unit Definition | Draft |
| RFC-0002 | Provider Declaration Format | Planned |
| RFC-0003 | Cross-provider Routing Protocol | Planned |

---

## Relationship to Existing Protocols

compute-commons is **not** a payments protocol.

| Protocol | Layer | What it solves |
|----------|-------|----------------|
| ACP (OpenAI+Stripe) | Commerce | Agent checkout & merchant integration |
| AP2 (Google) | Authorization | Agent payment mandates & trust |
| x402 | Transport | HTTP-native micropayments |
| **compute-commons** | **Metering** | **How much compute was used** |

ACP/AP2/x402 solve "how agents pay." compute-commons solves "what they're paying for." These are complementary layers.

---

## Reference Implementation

PZY V5 uses this protocol internally via its LiteLLM proxy layer.  
Cost tracking: `cost_records` table with provider-normalized CU fields.  
Budget enforcement: `system_config.budget.daily_cost_usd` runtime-configurable.

---

## Discussion

Open an Issue to discuss the RFCs.  
The CU definition in RFC-0001 is the most important thing to get right — feedback welcome.

---

## License

Specification text: MIT  
*(Additionally available under CC BY 4.0 — the spec is meant to be adopted, not hoarded.)*
