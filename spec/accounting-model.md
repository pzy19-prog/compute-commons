# Candidate Accounting Model

**Status**: Pre-RFC design note

## Principle

Accounting must be reproducible. A future reader should be able to distinguish what was observed at execution time from what was calculated later.

## Record Classes

### Native observation

Immutable provider/source values captured at or near execution time.

### Commercial calculation

A deterministic calculation using a named pricing schedule. Store the pricing version/effective interval and the source usage fields.

### Quota snapshot

State observed at a point in time. Do not infer per-request quota consumption from before/after snapshots unless the method explicitly records the uncertainty and possible concurrent activity.

### Derived normalization

A versioned transform for a stated purpose. Recalculation must not mutate the original event; new method versions produce new derived records or values.

## Time Semantics

At minimum distinguish:

- event time;
- observation time;
- pricing effective time;
- normalization method version/effective time;
- quota reset/window boundaries.

## Provenance

Each non-native value should identify its source or derivation method. Where a provider billing export later supersedes an estimate, both records may be retained with an explicit supersession relation.

## Historical Reproducibility

Provider repricing must not silently change historical cost. Historical events should resolve against the price schedule that applied to the event, unless the stored cost is an authoritative observed charge.

Likewise, changes to a normalization formula must not rewrite historical normalized values without preserving the original method version.

## Aggregation

Aggregation is allowed only between semantically compatible values. Examples:

- token counts may be summed within the same defined token category;
- monetary values require currency handling and price semantics;
- quota snapshots are not additive usage by default;
- compute proxies with different definitions must not be summed without an explicit conversion method.

## Missing and Unknown Values

Unknown is a first-class state. Implementations must not convert missing reasoning tokens, cache usage, quota values or physical-compute proxies into zero merely to simplify arithmetic.
