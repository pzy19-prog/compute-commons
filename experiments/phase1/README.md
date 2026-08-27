# Phase 1 Runtime Evidence Experiments

This directory contains reproducible experiment protocols and privacy-safe evidence formats for Issue #2.

## Evidence rule

Files under this directory are experiment definitions or captured evidence. A record may be classified as `observed` only when it comes from an actual execution/accounting surface and includes enough metadata to reproduce or audit the observation. Documentation-derived examples remain `declared`.

## Initial queue

- `E1-openai-count-vs-response.md` — compare OpenAI preflight input-token count with Responses API execution usage for the same frozen payload.
- `E2-anthropic-count-vs-usage.md` — compare Anthropic `messages/count_tokens` with Messages execution usage, preserving cache and thinking-token semantics.
- `E3-gemini-count-vs-usage.md` — compare Gemini `countTokens` with post-generation `usageMetadata` for the same frozen payload.
- `capture-record.schema.json` — experiment evidence envelope used before mapping into CRE 0.1.
- `validate_capture.py` — local structural validator for capture records and required provenance fields.

## Why three dual-surface experiments

Current provider documentation confirms that OpenAI, Anthropic and Gemini each expose a pre-execution token-counting surface separate from generation-time usage. Phase 1 therefore tests the same general question across three materially different provider semantics rather than treating any one provider as representative.

Documentation examples and API references remain `declared` evidence. Runtime equality or disagreement must be captured separately.

## Control state

`PHASE_1_RUNTIME_EXPERIMENT_PROTOCOLS_AVAILABLE`

`E1_E2_E3_OBSERVED_EVIDENCE_NOT_YET_CAPTURED`

This does not imply runtime validation, RFC-0002 Candidate status, reconciliation semantics, or CU/SCU validity.
