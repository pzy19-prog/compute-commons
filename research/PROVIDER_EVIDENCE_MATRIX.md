# Provider Evidence Matrix — Phase 1A

**Status**: Evidence baseline · declared semantics only  
**Issue**: #2  
**Reviewed**: 2026-08-27  
**Branch**: `research/phase1-provider-evidence-01`

## Purpose

This document establishes the first provider/surface evidence matrix for Phase 1. It records provider-declared semantics from authoritative documentation before runtime experiments are performed.

This is **not runtime proof**. Every provider claim below is classified as `declared` until a reproducible execution artifact is captured. Runtime observations, billing exports and invoice/settlement records must remain distinct evidence sources even when their field names agree.

Phase 1 does not assume that one token counter is inherently authoritative, that same-name fields are semantically equivalent across providers, or that a scalar CU/SCU is valid.

## Evidence classes used here

- `declared` — authoritative provider or standards documentation.
- `observed` — captured directly from an execution/accounting surface in a reproducible experiment.
- `calculated` — deterministic derivation from cited inputs and a versioned method.
- `estimated` — inference from incomplete evidence with explicit uncertainty.

## Initial provider / surface matrix

| Provider / standard | Surface | Declared usage/accounting fields | Important declared semantics | Phase 1 evidence status |
|---|---|---|---|---|
| OpenAI | Responses API response | `input_tokens`, `output_tokens`, `total_tokens`, `input_tokens_details.cached_tokens`, `input_tokens_details.cache_write_tokens`, `output_tokens_details.reasoning_tokens` | Response-level usage exposes input/output totals plus cache/reasoning breakdowns. | `declared`; runtime capture required |
| OpenAI | Responses input-token count endpoint | `input_tokens` | Separate pre-execution input-token counting surface exists; useful for comparing a client/preflight count with response usage for the same request payload. | `declared`; correlated runtime capture required |
| OpenAI | Organization Usage / Costs API | usage buckets and cost records grouped by supported dimensions such as project/API key/model | Organization accounting is a separate surface from per-response usage and may be aggregated by time bucket; it must not be treated as request-level evidence unless request attribution is actually exposed. | `declared`; admin runtime/export capture required |
| Anthropic | Messages API response | `input_tokens`, `output_tokens`, `cache_creation_input_tokens`, `cache_read_input_tokens`, cache TTL breakdowns, `output_tokens_details.thinking_tokens` where available | Anthropic explicitly states that API-side transformations mean usage counts need not match visible request/response content one-to-one. Total input usage is the sum of uncached input, cache creation and cache read counts. `output_tokens` remains the inclusive billing total while thinking-token detail is an observability decomposition. | `declared`; runtime capture required |
| Anthropic | Admin Messages Usage Report | `uncached_input_tokens`, cache creation buckets, `cache_read_input_tokens`, `output_tokens`, grouped dimensions | Administrative usage reporting is an accounting/aggregation surface distinct from a single Messages response. | `declared`; admin runtime/export capture required |
| Google Gemini | `generateContent` response `usageMetadata` | `promptTokenCount`, `cachedContentTokenCount`, `candidatesTokenCount`, `toolUsePromptTokenCount`, `thoughtsTokenCount`, `totalTokenCount`, modality token detail arrays | `promptTokenCount` includes the effective prompt size including cached content; thinking and tool-use prompt counts are separate fields; modality detail is available for several categories. | `declared`; runtime capture required |
| Google Gemini | `countTokens` | input `total_tokens` | Preflight token counting covers input; it provides a natural same-execution comparison candidate against post-generation `usageMetadata`. | `declared`; correlated runtime capture required |
| Google Gemini | AI Studio / Cloud Billing | account/project usage and cost views | Billing/accounting data is processed on a different cadence from request execution and may be delayed; this surface must remain distinct from request-level `usageMetadata`. | `declared`; account/billing evidence required |
| OpenTelemetry GenAI | telemetry semantic conventions | `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, cache/reasoning usage attributes/conventions | OTel states that input-token totals should include input token categories such as cached tokens, and reasoning output tokens should be included in output totals. OTel is an observability convention, not a settlement authority. | interoperability baseline; mapping validation required |

## Immediate semantic mismatches to test

These are **test hypotheses**, not accepted schema defects.

### 1. Inclusive vs component token semantics

Providers expose different relationships between aggregate and component fields.

Examples to validate:

- OpenAI exposes input/output totals with cache/reasoning detail objects.
- Anthropic defines total input for billing as a sum across uncached/cache-write/cache-read categories and states that visible content does not map one-to-one to usage counts.
- Gemini documents `promptTokenCount` as including cached content while also exposing `cachedContentTokenCount` separately.

A generic field named `input_tokens` is therefore insufficient evidence of cross-provider semantic equivalence without a documented mapping rule.

### 2. Reasoning / thinking usage

Reasoning-related token fields differ in naming and declared semantics:

- OpenAI: `output_tokens_details.reasoning_tokens`.
- Anthropic: `output_tokens_details.thinking_tokens`; `output_tokens` remains the inclusive billing total.
- Gemini: `thoughtsTokenCount` contributes to documented generation totals.

Phase 1 must determine what can be mapped directly, what is a provider-native decomposition, and what must remain explicitly provider-specific.

### 3. Cache semantics

Cache usage is not represented identically:

- OpenAI distinguishes cached input and cache-write usage in response details.
- Anthropic distinguishes cache creation and cache read, with cache-creation TTL breakdowns.
- Gemini reports cached content as part of effective prompt count and also separately.

No normalization rule is authorized yet.

### 4. Preflight count vs execution usage

OpenAI and Gemini expose token-counting surfaces separate from generation usage. These enable a required Phase 1 experiment:

1. freeze one exact request payload;
2. capture preflight count;
3. execute the request;
4. capture provider response usage;
5. preserve request/response identifiers and timestamps;
6. compare values without overwriting or averaging disagreements.

The result may expose differences caused by provider-added content, hidden transforms, caching, tool schemas, reasoning, or tokenizer/version behavior.

### 5. Request usage vs organization/billing usage

OpenAI and Anthropic expose administrative usage surfaces; Gemini exposes account/billing views. These are not presumed request-level sources.

Phase 1 must preserve the distinction:

`request execution claim` → `telemetry claim` → `account usage aggregation` → `cost/billing claim` → `invoice/settlement claim`

Correlation is evidence-dependent and must not be invented when identifiers are unavailable.

## CRE 0.1 mapping questions

The current CRE 0.1 schema has one event-level `evidence` object and one `usage` object. Phase 1 must test whether it can losslessly preserve:

1. multiple simultaneous usage claims for the same execution;
2. claim-specific source/issuer and timestamps;
3. preflight count plus post-execution count;
4. administrative/billing evidence that aggregates many requests;
5. provider-specific inclusive/component relationships;
6. tokenizer identity/version where an independent count is performed;
7. corrections or later accounting records that supersede an earlier estimate.

No schema change is authorized solely by this document. A change requires an observed counterexample, interoperability requirement, or reproducibility requirement under #2.

## Phase 1 runtime experiment queue

### E1 — OpenAI same-request count vs response usage

Required artifacts:

- exact request payload or privacy-safe canonical hash/reference;
- model identifier;
- preflight `input_tokens` result;
- Responses API `usage` object;
- response/request identifier where exposed;
- timestamps;
- CRE 0.1 fixture attempt;
- discrepancy note, including zero-discrepancy results.

### E2 — Anthropic response usage with cache and/or thinking

Required artifacts:

- exact request evidence or privacy-safe canonical reference;
- Messages API `usage` object;
- cache creation/read fields when exercised;
- thinking-token detail when available;
- request/message identifier;
- timestamps;
- CRE 0.1 fixture attempt.

### E3 — Gemini `countTokens` vs `usageMetadata`

Required artifacts:

- exact request evidence or privacy-safe canonical reference;
- `countTokens` result;
- `generateContent.usageMetadata`;
- cache/thought/modality detail when exercised;
- timestamps and request/correlation identifiers where available;
- CRE 0.1 fixture attempt.

### E4 — Administrative/accounting cross-surface case

Capture at least one provider where a request-level execution can be compared with a later organization/account/billing usage surface. If exact request-level correlation is impossible, record that limitation as a finding rather than fabricating attribution.

### E5 — Multimodal/native-unit case

Use a provider surface that exposes modality-specific counts or a native non-token unit. Preserve the provider-native representation before any normalization attempt.

## OpenTelemetry mapping baseline

Preliminary mapping candidates:

| CRE 0.1 | OTel GenAI | Status |
|---|---|---|
| `usage.input_tokens` | `gen_ai.usage.input_tokens` | candidate direct mapping only when provider-inclusive semantics are understood |
| `usage.output_tokens` | `gen_ai.usage.output_tokens` | candidate direct mapping only when inclusive semantics are understood |
| `usage.cache_read_tokens` | cache-read input-token convention | semantic verification required |
| `usage.cache_write_tokens` | cache-creation/write input-token convention | semantic verification required |
| `usage.reasoning_tokens` | reasoning output-token convention | provider mapping required |

OTel telemetry is a useful interoperability source but does not resolve which competing usage claim should govern billing or settlement.

## Sources

Authoritative documentation reviewed for this baseline:

- OpenAI Responses API reference: https://developers.openai.com/api/reference/resources/responses/methods/create
- OpenAI Responses input-token count reference: https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens
- OpenAI Organization Usage API reference: https://developers.openai.com/api/reference/resources/admin/subresources/organization/subresources/usage
- Anthropic Messages API reference: https://platform.claude.com/docs/en/api/messages
- Anthropic Messages Usage Report: https://docs.anthropic.com/en/api/admin-api/usage-cost/get-messages-usage-report
- Gemini Generate Content API (`UsageMetadata`): https://ai.google.dev/api/generate-content
- Gemini token counting documentation: https://ai.google.dev/api/tokens
- Gemini billing documentation: https://ai.google.dev/gemini-api/docs/billing
- OpenTelemetry GenAI semantic conventions registry: https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/

## Current conclusion

`PHASE_1A_DECLARED_EVIDENCE_BASELINE_ESTABLISHED`

This does **not** imply runtime validation, RFC-0002 Candidate status, reconciliation semantics, or CU/SCU validity.
