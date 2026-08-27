# Phase 1 Runtime Evidence Experiments

This directory contains reproducible experiment protocols and privacy-safe evidence formats for Issue #2.

## Evidence rule

Files under this directory are experiment definitions or captured evidence. A record may be classified as `observed` only when it comes from an actual execution/accounting surface and includes enough metadata to reproduce or audit the observation. Documentation-derived examples remain `declared`.

## Initial queue

- `E1-openai-count-vs-response.md` — compare OpenAI preflight input-token count with Responses API execution usage for the same frozen payload.
- `E3-gemini-count-vs-usage.md` — compare Gemini `countTokens` with post-generation `usageMetadata` for the same frozen payload.
- `capture-record.schema.json` — experiment evidence envelope used before mapping into CRE 0.1.
- `validate_capture.py` — local structural validator for capture records and required provenance fields.

## Control state

`PHASE_1_RUNTIME_EXPERIMENT_PROTOCOLS_AVAILABLE`

This does not imply that E1 or E3 has produced observed evidence.
