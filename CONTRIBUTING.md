# Contributing

compute-commons is a research-and-specification project. Contributions should make claims easier to verify, not merely make the repository larger.

## Contribution Types

- provider evidence and measurement profiles;
- prior-art corrections;
- schema and RFC proposals;
- empirical experiments;
- mappings to adjacent standards;
- critiques of normalization assumptions.

## Evidence Expectations

When a contribution claims provider behavior, include an authoritative documentation source, reproducible runtime evidence, or both as appropriate.

Distinguish clearly between observed behavior, provider declarations, deterministic calculations, and estimates or hypotheses.

Do not claim production implementation without repository/runtime evidence that matches the claim.

## RFC Changes

Follow `rfcs/RFC-PROCESS.md`. Material semantic changes should be proposed through an RFC or an explicit revision to a Draft RFC rather than hidden inside implementation code.

## Compatibility

Preserve provider-native observations and version normalization/pricing methods. Do not silently reinterpret historical records.

## Pull Requests

Keep each pull request bounded to one research/specification objective where practical. The PR description should state the problem, files or semantics changed, evidence added, compatibility impact, and unresolved questions.
