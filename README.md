# compute-commons

> Open research and specifications for provider-agnostic AI inference resource accounting.

**Status**: Research Rebaseline · 2026-08  
**Author**: [@pzy19-prog](https://github.com/pzy19-prog)

compute-commons studies a basic question before standardizing an answer:

> Which AI inference resource measurements are meaningfully comparable across providers, and at what layer should they be normalized?

The project does **not** assume that all AI compute can be losslessly represented by one scalar unit.

## Scope

compute-commons separates four layers that are often conflated:

1. **Usage** — tokens, requests, media units, cache activity and other provider-visible usage.
2. **Commercial** — price, currency and pricing-version information.
3. **Quota** — limits, remaining allowance, reset cycles and subscription-specific constraints.
4. **Compute proxies** — GPU time, accelerator type, FLOP or energy estimates when such evidence is actually available.

The project researches whether an aggregate **Compute Unit (CU)** can be derived from these dimensions without hiding material differences. CU is therefore a research hypothesis, not a settled primitive.

## Project Structure

- `research/` — problem framing, terminology, prior art and open questions.
- `spec/` — candidate resource, accounting and normalization models.
- `rfcs/` — versioned protocol proposals and historical drafts.
- `schemas/` — machine-readable interchange schemas.
- `experiments/` — validation plans and empirical work.

## RFC Status

| RFC | Title | Status |
|---|---|---|
| [RFC-0001](rfcs/RFC-0001-compute-unit.md) | Compute Unit Definition | Historical Draft · Under Re-evaluation |
| [RFC-0002](rfcs/RFC-0002-compute-resource-event.md) | Compute Resource Event Model | Draft |

See [RFC Process](rfcs/RFC-PROCESS.md).

## Relationship to Other Systems

compute-commons defines **measurement and accounting semantics**. It does not choose models or route tasks.

- **CLI Quota Watch** is a candidate observation and validation source for quota/usage evidence.
- **Forge Orchestrator** may consume normalized resource evidence for routing and budget decisions, but routing is out of scope here.
- **PZY V5** is a candidate future reference consumer. It is **not currently claimed to implement compute-commons in production**.

## Relationship to Existing Protocols

compute-commons is not a payments protocol. Payment and authorization standards answer how agents pay or are authorized to pay; compute-commons focuses on describing what resource usage was observed and how accounting claims are derived.

## Research Baseline

Start with:

- [Research Agenda](research/RESEARCH_AGENDA.md)
- [Problem Statement](research/PROBLEM_STATEMENT.md)
- [Terminology](research/TERMINOLOGY.md)
- [Prior Art](research/PRIOR_ART.md)
- [Open Questions](research/OPEN_QUESTIONS.md)

## License

MIT. See [LICENSE](LICENSE).
