# RFC-0001: Compute Unit (CU) Definition

**Status**: Historical Draft · Under Re-evaluation  
**Created**: 2026-04  
**Reclassified**: 2026-08  
**Author**: pzy19-prog

> This document is preserved as the first-generation design of compute-commons. It is **not** the current normative baseline. The 2026-08 rebaseline identified unresolved assumptions in collapsing heterogeneous AI inference usage, commercial pricing and physical compute into a single scalar CU.

## Historical Proposal

The original proposal defined one Compute Unit as the compute equivalent of processing 1,000 input tokens and generating 100 output tokens using a GPT-3.5-turbo-equivalent capability tier anchored to 2024-01-01, with provider-specific `cu_rate` declarations.

That proposal was intended to make cross-provider budgeting and comparison easier. It remains useful as a hypothesis and as project history, but several assumptions require evidence before the model can become normative.

## Why This RFC Was Reclassified

The original design did not establish a defensible derivation rule for provider `cu_rate` values. A rate based on price measures commercial exchange, not physical compute. A rate based on FLOPs or GPU time is usually unavailable to API consumers. A rate based on model capability becomes a benchmark/capability metric rather than a compute metric. Provider self-declaration alone does not guarantee cross-provider comparability.

The original design also mixed dimensions that should initially remain separate:

- provider-visible usage such as input/output/cache tokens;
- commercial cost and pricing versions;
- subscription or CLI quota limits and reset cycles;
- hardware-level or estimated compute proxies.

The current research baseline therefore starts with a multidimensional resource event and tests whether an aggregate CU can be derived without hiding material differences.

## Historical Non-goals

The original proposal already excluded training compute, cryptocurrency/tokenization and workload portability. Those exclusions remain useful, but the overall project scope is now defined in the repository research baseline.

## Correction to Previous Reference-Implementation Claim

Earlier versions of this RFC stated that PZY V5 implemented CU accounting in production through `cu_rate`, `cu_consumed`, `shared/cost.py` and `system_config.budget.daily_cu`.

That statement is withdrawn. The current PZY V5 repository has cost-observation infrastructure but does not provide the claimed compute-commons implementation. PZY V5 is treated only as a **candidate future reference consumer** unless a separate evidence-backed integration is implemented and verified.

## Successor Work

The active baseline is:

- `research/RESEARCH_AGENDA.md`
- `spec/resource-model.md`
- `spec/accounting-model.md`
- `spec/normalization-model.md`
- `rfcs/RFC-0002-compute-resource-event.md`
- `schemas/compute-resource-event.schema.json`

## Historical Design Questions Retained for Research

1. Can any stable scalar CU be derived from provider-visible evidence?
2. Should a scalar represent compute, commercial value, quota pressure, or a clearly named composite index?
3. How should cache, reasoning and multimodal usage be represented?
4. Which party is authoritative for normalization coefficients?
5. How should versions and uncertainty be carried with every derived value?

## Changelog

- 2026-04: Initial draft.
- 2026-08: Reclassified as historical draft; production implementation claim withdrawn; scalar-CU assumptions moved back into research.
