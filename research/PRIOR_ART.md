# Prior Art Map

**Status**: Research baseline, not exhaustive.  
**Last reviewed**: 2026-08

compute-commons should interoperate with existing standards rather than rename their concepts. The key question is whether an existing system already provides the same semantics or only an adjacent layer.

## OpenTelemetry Semantic Conventions

OpenTelemetry semantic conventions standardize attribute names, units and meanings for telemetry. Generative-AI conventions are maintained in a dedicated GenAI semantic-conventions repository.

**Relevant to compute-commons**: event/trace correlation, provider/model attributes, token usage and observability naming.

**Gap addressed here**: compute-commons focuses on portable resource accounting, commercial/quota separation, provenance and normalization semantics. It should map to OpenTelemetry where possible instead of inventing incompatible telemetry fields.

References:
- https://opentelemetry.io/docs/specs/semconv/
- https://opentelemetry.io/docs/specs/otel/semantic-conventions/

## MLPerf Inference / MLCommons

MLPerf Inference provides architecture-neutral, representative and reproducible benchmarking of inference systems, with workload definitions, quality targets, latency/throughput scenarios and published results. Inference v6.0 also covers contemporary reasoning workloads, and MLCommons has introduced work on agentic inference.

**Relevant to compute-commons**: workload definition, reproducibility, performance measurement and potential empirical anchors for compute-proxy research.

**Not equivalent**: benchmark-system performance does not by itself define API-consumer billing, subscription quota semantics or per-request portable accounting.

References:
- https://mlcommons.org/working-groups/benchmarks/inference/
- https://mlcommons.org/2026/04/mlperf-inference-v6-0-results/
- https://mlcommons.org/2026/07/agentic-inference-for-mlperf-inference/

## LiteLLM

LiteLLM provides a unified interface across many model providers and supports spend tracking, budgets, routing, rate limiting and proxy-based observability.

**Relevant to compute-commons**: practical provider adapters and cost/usage ingestion.

**Not equivalent**: a gateway's cost normalization and budget controls do not by themselves establish a provider-independent definition of physical compute or quota equivalence.

Reference:
- https://docs.litellm.ai/

## Provider Usage and Billing APIs

Individual providers expose differing combinations of token counts, cached-token semantics, model identifiers, request-level usage, billing exports and account-level limits.

**Relevant to compute-commons**: these are primary evidence sources for provider-native fields.

**Research rule**: provider semantics must be captured with effective dates and source references. A field with the same name across providers is not presumed to have the same semantics.

## Hardware-level Metrics

GPU/accelerator seconds, power and FLOP estimates are closer to physical compute than commercial price, but they are often unavailable to hosted API consumers and may not capture serving optimizations, sparsity, speculative decoding, batching or hidden system work.

**Research implication**: hardware-level metrics should be modeled as optional compute proxies with provenance, not silently inferred from token counts.

## Adjacent Payment/Authorization Protocols

Payment, checkout and authorization protocols address economic transfer or permission. compute-commons is intentionally upstream of payment execution: it describes resource/accounting evidence and derivation semantics.

## Current Gap Hypothesis

No single item above is assumed to provide all of the following together:

1. provider-native inference usage preservation;
2. quota-state representation;
3. commercial price/version provenance;
4. optional physical-compute proxies;
5. explicit evidence classes and uncertainty;
6. purpose-specific normalization without claiming false equivalence.

This gap hypothesis must be tested continuously as standards evolve.
