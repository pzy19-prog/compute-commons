# Candidate Resource Model

**Status**: Pre-RFC design note

The baseline model is multidimensional. It preserves source observations and prevents a normalized scalar from replacing the evidence used to derive it.

## Resource Event Envelope

Each event should identify:

- schema version;
- event identifier and timestamp;
- provider, model and execution surface;
- execution boundary/correlation identifiers;
- evidence source and evidence class;
- native usage dimensions;
- optional commercial accounting;
- optional quota snapshot/reference;
- optional compute proxies;
- optional normalized values with method provenance.

## Usage Dimension

Candidate fields include:

- input tokens;
- output tokens;
- reasoning tokens;
- cache-read tokens;
- cache-write tokens;
- request count;
- provider-native media usage;
- provider-native custom units.

A missing field means unknown/not exposed. It must not default to zero unless the source semantics guarantee zero.

## Commercial Dimension

Commercial information is separate from usage:

- amount;
- currency;
- pricing version/effective time;
- observed versus calculated status;
- discounts/credits metadata where known.

## Quota Dimension

Quota is modeled as state or a referenced snapshot rather than assumed request-level compute:

- quota identifier/scope;
- limit;
- remaining;
- consumed where directly exposed;
- unit;
- reset time/window;
- observation timestamp.

## Compute Proxy Dimension

Optional values may include:

- accelerator seconds;
- accelerator type;
- FLOP estimate;
- energy estimate;
- method/version;
- confidence/uncertainty.

## Derived/Normalized Dimension

Every derived value must carry:

- metric name;
- value/unit;
- normalization method identifier and version;
- input-field references where practical;
- evidence class (`calculated` or `estimated`);
- confidence/uncertainty when estimated.

No derived value is allowed to erase or overwrite provider-native evidence.

## Extensibility

Provider-specific fields belong under a namespaced extension object unless promoted through the RFC process. This avoids forcing new provider semantics into misleading standard fields.
