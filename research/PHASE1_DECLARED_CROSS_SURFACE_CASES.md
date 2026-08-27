# Phase 1 Declared Cross-Surface Cases

**Issue**: #2  
**Evidence class**: `declared` only  
**Reviewed**: 2026-08-27

## Purpose

Record authoritative provider documentation that establishes why same-execution multi-surface runtime experiments are necessary. These cases justify experiments; they are not substitutes for observed evidence.

## OpenAI

OpenAI exposes both:

- `POST /responses/input_tokens`, returning a pre-execution `input_tokens` count; and
- Responses API execution usage containing `input_tokens`, `output_tokens`, `total_tokens`, cache details and reasoning-token details.

This creates two distinct provider surfaces that can be correlated for one frozen request. Current documentation establishes surface availability but does not, by itself, prove equality or disagreement for our experiment payload.

Sources:

- https://developers.openai.com/api/reference/resources/responses/subresources/input_tokens
- https://developers.openai.com/api/reference/resources/responses/methods/create

## Anthropic

Anthropic exposes `POST /v1/messages/count_tokens`, which counts Message input without creating the Message. Its Messages usage documentation separately states that requests are transformed into model-suitable form and outputs are parsed before becoming API responses; therefore usage counts need not match visible request/response content one-to-one.

Anthropic also declares:

- total input usage is `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`;
- `output_tokens` is the inclusive billing total;
- `output_tokens_details.thinking_tokens` is an observability decomposition and must not be added to `output_tokens` again.

These semantics make Anthropic a direct test case for distinguishing provider-native components, calculated totals and visible-content tokenization.

Sources:

- https://platform.claude.com/docs/en/api/http/messages/count_tokens
- https://platform.claude.com/docs/en/api/messages/create

## Google Gemini

Gemini exposes both `countTokens` and generation-time `usageMetadata`.

The current official token-counting documentation contains an illustrative text example in which the preflight count is shown as 10 tokens while the subsequent generation response is shown with `prompt_token_count` 11. The documentation marks these values as examples, so this is not runtime proof for compute-commons, but it is a provider-published counterexample to assuming that preflight and execution input counts must always be identical.

Gemini's `UsageMetadata` also declares that:

- `promptTokenCount` includes cached content in the effective prompt size;
- `cachedContentTokenCount` is separately exposed;
- `thoughtsTokenCount` records thinking tokens;
- `totalTokenCount` covers prompt + thoughts + response candidates;
- modality-specific token detail arrays may be returned.

Sources:

- https://ai.google.dev/api/tokens
- https://ai.google.dev/api/generate-content

## Research implication

The provider documentation is already sufficient to reject the following assumption as an architectural premise:

> A single generic `input_tokens` field is necessarily the unique, surface-independent truth for one execution.

It is **not** sufficient to conclude which surface should govern billing, revenue sharing or settlement.

Phase 1 therefore preserves the stronger control state:

`MULTIPLE_USAGE_SURFACES_DECLARED`

`RUNTIME_CROSS_SURFACE_EQUIVALENCE_NOT_YET_PROVEN`

`SETTLEMENT_AUTHORITY_NOT_DEFINED`
