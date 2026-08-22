# Compute Commons Research Agenda

**Baseline**: COMPUTE-COMMONS-REBASELINE-01  
**Status**: Active  
**Date**: 2026-08

## Research Objective

Determine which AI inference resource measurements can be represented consistently across providers, which dimensions must remain distinct, and under what evidence an aggregate normalization unit is justified.

## Core Research Questions

1. What is observable at the API, CLI, proxy and infrastructure layers?
2. Which observations are semantically comparable across providers?
3. Which quantities represent usage, commercial value, quota pressure or physical compute rather than the same underlying concept?
4. How should uncertainty, missing fields and provider-specific semantics be represented?
5. Can a scalar Compute Unit be derived without creating false precision?
6. What versioning and provenance are required so historical accounting remains reproducible after provider repricing or API changes?

## Workstreams

### R1 — Provider Measurement Survey

Build evidence-backed profiles for major providers and execution surfaces. Record token categories, cache semantics, multimodal units, request limits, subscriptions, reset windows, prices and any exposed infrastructure metrics.

### R2 — Semantic Resource Model

Define a provider-agnostic event envelope that preserves native observations rather than immediately converting everything into one number.

### R3 — Accounting and Provenance

Define how observed values, derived values, prices, quota snapshots, model identifiers, timestamps and evidence sources are recorded and versioned.

### R4 — Normalization Research

Evaluate candidate normalization approaches:

- price-index normalization;
- workload-based normalization;
- hardware/compute-proxy normalization;
- capability-adjusted normalization;
- multidimensional vectors with no scalar aggregate.

Every candidate must state what it measures and what it does not measure.

### R5 — Empirical Validation

Use real provider/CLI observations where permitted. CLI Quota Watch is a candidate evidence source. Validation should include cross-provider examples, missing-data cases, pricing changes and quota resets.

### R6 — Interoperability

Map compute-commons fields to relevant observability, benchmarking and billing conventions without claiming equivalence where semantics differ.

## Phase 1 Deliverables

- Problem statement and terminology baseline.
- Prior-art map with source-backed claims.
- Compute Resource Event schema draft.
- Accounting and normalization design notes.
- Provider evidence matrix.
- At least three end-to-end example records from different provider surfaces.
- Decision memo on whether CU remains scalar, becomes explicitly composite, or is rejected.

## Research Discipline

- Observation must be separated from inference.
- Provider-native values must be retained alongside normalized values.
- Derived metrics must carry method/version metadata.
- Unknown values must remain unknown; zero is not a substitute for missing evidence.
- Commercial price is not physical compute unless explicitly modeled as a price index.
- No production-implementation claim without repository/runtime evidence.

## Exit Criteria for Rebaseline

The rebaseline can advance from research baseline to candidate specification only when:

1. the resource event schema covers the target provider evidence without lossy coercion;
2. accounting semantics distinguish usage, commercial, quota and compute-proxy dimensions;
3. normalization claims have a documented derivation and limitations;
4. at least one independent consumer can implement the schema from the written specification;
5. historical records remain reproducible under versioned pricing/normalization changes.
