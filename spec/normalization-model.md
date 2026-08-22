# Candidate Normalization Model

**Status**: Pre-RFC design note

Normalization is purpose-specific. The baseline rejects the assumption that one scalar automatically represents usage, price, quota pressure and physical compute.

## Required Properties of a Normalized Metric

A normalized metric must declare:

1. the question it is intended to answer;
2. input dimensions and admissible evidence classes;
3. formula and coefficients;
4. method/version identifier;
5. effective interval where relevant;
6. units and interpretation;
7. limitations and known non-comparabilities;
8. uncertainty/confidence rules.

## Candidate Families

### Commercial-equivalent index

Normalizes commercial value using price schedules or a reference basket. Useful for budgeting/comparison of spend, but must not be called physical compute.

### Quota-pressure index

Expresses consumption or remaining allowance relative to a provider-defined quota window. Useful for operational routing, but subscription-specific and not physical compute.

### Workload-equivalent index

Compares executions against a reproducible reference workload or benchmark. Potentially useful for cross-system comparison, but sensitive to workload definition and quality constraints.

### Compute-proxy index

Uses hardware-level observations or estimates such as accelerator time/FLOPs/energy. Potentially closer to physical compute, but often unavailable or uncertain for hosted APIs.

### Multidimensional vector

Retains several normalized dimensions without forcing them into one scalar. This is the default safe representation when no defensible aggregation function exists.

## Scalar CU Decision Gate

A scalar CU may become normative only if the project can specify:

- exactly what CU measures;
- a reproducible derivation across target providers;
- treatment of multimodal, cache and reasoning usage;
- uncertainty behavior for opaque providers;
- evidence that the scalar preserves the comparisons it is claimed to support.

Until then, `CU` is historical/research terminology.
