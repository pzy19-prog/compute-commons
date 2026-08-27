# E3 — Gemini countTokens vs generateContent usageMetadata

**Issue**: #2  
**Status**: Protocol ready · observed evidence not yet captured

## Objective

Determine whether Gemini `countTokens` and post-generation `usageMetadata` report compatible input-token semantics for the same canonical request, while preserving all modality/cache/thought details exposed by the provider.

## Frozen-input rule

`countTokens` and `generateContent` MUST derive from one canonical request description. Record any endpoint-specific transformation explicitly.

Store the canonical payload directly when safe, otherwise record a canonical SHA-256 digest plus enough non-sensitive metadata to reproduce the request structure.

## Required observations

### Claim A — countTokens

Record:

- provider: `google-gemini`;
- surface: `countTokens`;
- exact model;
- `total_tokens` or provider-equivalent field;
- request/correlation identifier when exposed;
- observed timestamp;
- raw response or immutable evidence reference.

### Claim B — generateContent usageMetadata

Record:

- provider: `google-gemini`;
- surface: `generateContent.usageMetadata`;
- exact model;
- `promptTokenCount`;
- `cachedContentTokenCount` when present;
- `candidatesTokenCount`;
- `toolUsePromptTokenCount` when present;
- `thoughtsTokenCount` when present;
- `totalTokenCount`;
- modality token details when present;
- observed timestamp;
- raw response or immutable evidence reference.

## Comparison

Compare the preflight input count with the execution-time prompt count without assuming they are definitionally identical.

Preserve provider-native inclusive/component relationships. Do not rewrite Gemini fields into generic input/cache/reasoning fields until a mapping rule is justified.

## CRE 0.1 test

Attempt a lossless mapping to CRE 0.1 and record:

- directly mapped fields;
- provider-native fields retained in `extensions`;
- any semantic ambiguity;
- whether multiple claims for one logical execution can be preserved without loss.

## Exit condition

E3 is complete only when both surfaces have auditable observed evidence, or when an explicit access/provider limitation is recorded.
