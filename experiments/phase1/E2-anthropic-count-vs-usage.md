# E2 — Anthropic count_tokens vs Messages usage

**Issue**: #2  
**Status**: Protocol ready · observed evidence not yet captured

## Objective

Compare Anthropic's pre-execution `POST /v1/messages/count_tokens` result with the execution-time Messages API `usage` object for one frozen logical request, while separately preserving cache and thinking-token semantics.

This experiment is justified by provider documentation, not by a pre-assumed schema defect. Anthropic documents both a token-counting endpoint and service-side transformations that can make API usage counts differ from the exact visible request/response content.

## Frozen-input rule

The count request and Messages execution request MUST derive from the same canonical request description, including where applicable:

- exact model identifier;
- messages;
- system content;
- tools/function schemas;
- thinking configuration;
- images/documents or other supported content;
- cache-control settings.

If endpoint-specific wrappers differ, record the deterministic transformation. Store the canonical payload directly when safe, otherwise store its canonical SHA-256 digest plus a privacy-safe structural description.

## Required observations

### Claim A — preflight token count

Record at minimum:

- provider: `anthropic`;
- surface: `messages.count_tokens`;
- exact model;
- returned `input_tokens`;
- request/correlation identifier when exposed;
- observed timestamp;
- raw response or immutable evidence reference.

Anthropic documents this count as covering the provided messages, system prompt and tools; supported rich inputs should remain part of the canonical request evidence.

### Claim B — execution usage

Record at minimum:

- provider: `anthropic`;
- surface: `messages.create`;
- exact model;
- `input_tokens`;
- `cache_creation_input_tokens` when present;
- `cache_read_input_tokens` when present;
- cache TTL breakdowns when present;
- `output_tokens`;
- `output_tokens_details.thinking_tokens` when present;
- message/request identifier;
- observed timestamp;
- raw response or immutable evidence reference.

## Comparison rules

Do not compare `count_tokens.input_tokens` only with the execution `usage.input_tokens` field when caching is active without first respecting Anthropic's declared semantics.

Anthropic documents total request input usage as:

`input_tokens + cache_creation_input_tokens + cache_read_input_tokens`

Therefore preserve both:

1. the provider-native component fields; and
2. a deterministic calculated `execution_total_input_tokens` when all required components are available.

Any calculated total MUST be labeled `calculated`, with the formula/version recorded. It MUST NOT replace the observed component fields.

A difference between preflight count and execution total is a finding; equality is also evidence. Do not infer causation without additional evidence.

## Thinking-token rule

Anthropic documents `output_tokens` as the inclusive billing total and `thinking_tokens` as an observability decomposition. Preserve that relationship. Do not add thinking tokens to `output_tokens` again.

## CRE 0.1 test

Attempt to preserve both the preflight claim and execution claim under CRE 0.1 and record whether:

1. two events can be correlated losslessly to one logical execution;
2. claim-specific provenance is preserved;
3. provider-native cache component semantics fit the generic usage fields without semantic distortion;
4. the calculated total input needs separate derivation metadata;
5. thinking-token decomposition maps without double counting;
6. any essential evidence is forced into `extensions`.

## Authoritative declared sources

Reviewed 2026-08-27:

- Anthropic Count tokens in a Message: https://platform.claude.com/docs/en/api/http/messages/count_tokens
- Anthropic Create a Message / Usage semantics: https://platform.claude.com/docs/en/api/messages/create

These sources are `declared` evidence only. They do not satisfy the runtime-observation requirement.

## Exit condition

E2 is complete only when the repository contains auditable observed records for both token-count and execution surfaces, or an explicit access/provider limitation is recorded.
