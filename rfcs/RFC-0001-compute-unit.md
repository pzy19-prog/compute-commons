# RFC-0001: Compute Unit (CU) Definition

**Status**: Draft  
**Created**: 2026-04  
**Author**: pzy19-prog  
**Repository**: compute-commons  
**Discussion**: [Issues](https://github.com/pzy19-prog/compute-commons/issues)

---

## Abstract

This RFC defines the **Compute Unit (CU)** — a provider-agnostic atomic unit for measuring AI inference work. It specifies how providers declare their CU exchange rates and how consumers normalize costs across providers for budgeting and comparison.

---

## Motivation

Current AI inference billing is fragmented:

- OpenAI bills per token (input/output separately, with cache tiers)
- Anthropic bills per token with cache read/write distinctions
- Alibaba DashScope bills per thousand tokens with model-tier pricing
- GPU cloud providers bill per GPU-hour
- Some providers bill per API call

A consumer running workloads across multiple providers cannot answer a simple question: *"how much compute did I use today?"* — without provider-specific accounting logic embedded in their codebase.

This problem compounds in multi-agent systems where a single user task may invoke 5–20 LLM calls across different model tiers and providers. The lack of a common unit makes budgeting, optimization, and provider comparison structurally difficult.

The Compute Unit is a minimal abstraction that solves this without requiring providers to change their pricing models.

---

## Specification

### 1. Compute Unit (CU) Definition

A **Compute Unit** is defined as:

> The compute equivalent of processing 1,000 input tokens and generating 100 output tokens using a reference model (GPT-3.5-turbo-equivalent capability tier) as of 2024-01-01.

**Design decisions:**

- The definition is intentionally **fixed in time**. CU is a stable accounting unit, not a tracker of hardware efficiency improvements.
- The 10:1 input/output ratio reflects typical production workload patterns.
- The reference date anchors the definition independent of future model repricing.

**Reference CU cost**: $0.002 USD (as of definition date)

### 2. Provider Exchange Rate Declaration

Providers (or proxy layers like LiteLLM) declare a `cu_rate` in their model configuration:

```json
{
  "model": "gpt-4o",
  "provider": "openai",
  "cu_rate": {
    "per_1k_input_tokens": 0.5,
    "per_1k_output_tokens": 2.0,
    "per_1k_cache_read_tokens": 0.05,
    "effective_date": "2024-01-01",
    "version": "1"
  }
}
```

`cu_rate` values are **CU per unit of provider billing**, not USD. This decouples the standard from USD price fluctuations.

### 3. Consumer Normalization

Consumers normalize provider costs to CU at ingestion time:

```python
def to_cu(input_tokens, output_tokens, cache_read_tokens=0, cu_rate):
    return (
        (input_tokens / 1000) * cu_rate["per_1k_input_tokens"] +
        (output_tokens / 1000) * cu_rate["per_1k_output_tokens"] +
        (cache_read_tokens / 1000) * cu_rate.get("per_1k_cache_read_tokens", 0)
    )
```

CU is stored alongside USD cost in billing records:

```sql
CREATE TABLE cost_records (
    id uuid PRIMARY KEY,
    task_id uuid,
    provider text,
    model text,
    input_tokens int,
    output_tokens int,
    cache_read_tokens int DEFAULT 0,
    cu_consumed decimal(10, 4),   -- normalized compute units
    cost_usd decimal(10, 6),      -- actual provider cost
    cu_rate_version text,         -- which rate declaration was used
    recorded_at timestamptz DEFAULT NOW()
);
```

USD fluctuates with provider repricing. CU provides a stable comparison baseline across time and providers.

### 4. Budget Expression

Budgets may be expressed in CU, USD, or both:

```yaml
budget:
  daily_cu: 500
  daily_usd: 2.00
  enforce: whichever_first
```

Enforcement logic runs at the proxy layer (e.g., LiteLLM gateway) before forwarding requests.

---

## Non-goals

- CU is **not** a tradeable token or cryptocurrency
- CU does **not** imply portability of workloads between providers
- CU does **not** track hardware efficiency improvements over time
- This RFC does **not** define a marketplace or exchange mechanism (see RFC-0003)
- This RFC does **not** cover training compute — inference only

---

## Open Questions

1. Should the reference model definition be updated on a fixed schedule (e.g., every 2 years), or remain permanently fixed at 2024-01-01?
2. How should multimodal inputs (images, audio, video) be normalized to CU?
3. Should cached tokens count at a reduced CU rate, or zero?
4. Who maintains the canonical `cu_rate` registry for major providers?

---

## Relationship to Other Standards

- **MLCommons**: focuses on training benchmark performance, not inference billing
- **FLOP-based metrics**: hardware-level, not usable at the API consumer layer  
- **ACP/AP2**: solve agent payment authorization, not compute metering
- **OpenTelemetry semantic conventions for LLM**: covers observability attributes, complementary to CU

compute-commons fills the gap between "I made an API call" and "I can compare that call to any other call on any provider."

---

## Reference Implementation

PZY V5 (`pzy-v5`) implements this RFC in production:

- `infra/litellm/config.yaml` — model configs with cu_rate declarations
- `shared/cost.py` — `to_cu()` normalization function  
- `cost_records` table — stores both `cu_consumed` and `cost_usd` per LLM call
- `system_config.budget.daily_cu` — runtime-configurable CU budget

---

## Changelog

- 2026-04: Initial draft
