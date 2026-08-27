# E1 — OpenAI preflight count vs response usage

**Issue**: #2  
**Status**: Protocol ready · observed evidence not yet captured

## Objective

Determine whether OpenAI's pre-execution input-token count and the execution-time Responses API usage agree for the same canonical request payload, and record any disagreement without selecting an authority.

## Frozen-input rule

The token-count request and execution request MUST derive from the same canonical payload object. If the two endpoints require different wrappers, the experiment MUST record the deterministic transformation used to construct each request.

The canonical payload itself may be stored directly when non-sensitive. Otherwise store:

- canonical serialization method;
- SHA-256 digest;
- privacy-safe description;
- exact model identifier;
- tool/schema/configuration inputs that may affect tokenization.

## Required observations

### Claim A — preflight count

Record at minimum:

- provider: `openai`;
- surface: `responses.input_tokens`;
- model;
- observed input token count;
- provider request/correlation id when exposed;
- observed timestamp;
- raw response or immutable evidence reference.

### Claim B — execution usage

Record at minimum:

- provider: `openai`;
- surface: `responses.create`;
- model;
- `input_tokens`;
- `output_tokens`;
- cache/reasoning details when present;
- response/request id;
- observed timestamp;
- raw response or immutable evidence reference.

## Comparison

Compute only deterministic deltas, for example:

`input_delta = execution_input_tokens - preflight_input_tokens`

A non-zero delta is a finding. A zero delta is also evidence and MUST be retained.

Do not infer the cause of a delta without additional evidence. Candidate explanations such as provider-side transforms, hidden instructions, caching, tokenizer changes, tool schemas, or endpoint semantics remain hypotheses until proven.

## CRE 0.1 test

After capture, attempt to represent both claims with the current `schemas/compute-resource-event.schema.json` without overwriting either observation. Document whether:

1. two CRE events are sufficient while preserving that both claims concern one logical execution;
2. event-level `evidence` is adequate for claim provenance;
3. the execution correlation fields are sufficient;
4. any required information is forced into `extensions`.

## Exit condition

E1 is complete only when the repository contains auditable observed records for both surfaces or a documented provider/access limitation explaining why one surface cannot be captured.
