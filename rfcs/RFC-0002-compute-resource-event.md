# RFC-0002: Compute Resource Event Model

**Status**: Draft  
**Created**: 2026-08  
**Author**: pzy19-prog

## Abstract

This RFC proposes a provider-agnostic event envelope for AI inference resource accounting. The model preserves provider-native observations and separates usage, commercial cost, quota state and optional physical-compute proxies. It does not require a universal scalar Compute Unit.

## Problem and Scope

Cross-provider systems need portable accounting without pretending that tokens, money, quota and hardware work are interchangeable. The Compute Resource Event (CRE) is the base interchange object for recording those dimensions with provenance.

This RFC covers inference resource events only. It does not define routing, payments, training-compute accounting or a marketplace.

## Normative Terms

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** are to be interpreted as requirement levels for this draft.

## Event Requirements

A CRE MUST contain:

- `schema_version`;
- `event_id`;
- `event_time`;
- `provider`;
- `model`;
- `surface` describing the observation/execution surface;
- `evidence` describing evidence class and source.

A CRE SHOULD contain at least one resource/accounting dimension: `usage`, `commercial`, `quota`, `compute_proxy` or `normalized`.

Missing values MUST remain absent/null according to schema semantics. Implementations MUST NOT substitute zero for an unknown value.

## Evidence

`evidence.class` MUST be one of:

- `observed`;
- `declared`;
- `calculated`;
- `estimated`.

Estimated values SHOULD include confidence or uncertainty metadata either in the relevant object or its derivation metadata.

## Usage

The standard usage object may contain input/output/reasoning/cache token counts and request count. Provider-native media or custom units SHOULD be preserved in `native_units` rather than coerced into token counts.

## Commercial

Commercial accounting MUST identify currency and SHOULD identify the pricing version or effective-time reference when cost is calculated rather than directly observed.

Commercial cost MUST NOT be described as physical compute solely because it correlates with provider usage.

## Quota

Quota values represent provider/subscription state. A quota snapshot SHOULD identify scope, unit, observation time and reset semantics when available.

Account-level quota deltas MUST NOT be attributed to a single request as observed request consumption unless the provider exposes that attribution. Inferred attribution must be marked calculated/estimated.

## Compute Proxies

Hardware-level or estimated compute fields are optional. Each non-observed compute proxy SHOULD identify its method/version and confidence where meaningful.

## Normalized Values

A normalized metric MUST provide a metric name, value, unit and method/version identifier. The metric definition MUST state its intended interpretation. Normalized values MUST NOT replace native evidence.

The name `CU` is reserved for future accepted work on a Compute Unit and SHOULD NOT be emitted as a normative metric under this RFC.

## Example

```json
{
  "schema_version": "0.1",
  "event_id": "evt_01JXYZ",
  "event_time": "2026-08-23T03:00:00Z",
  "provider": "example-provider",
  "model": "example-model",
  "surface": "api",
  "evidence": {
    "class": "observed",
    "source": "provider_response"
  },
  "usage": {
    "input_tokens": 1200,
    "output_tokens": 240,
    "cache_read_tokens": 800,
    "request_count": 1
  },
  "commercial": {
    "amount": 0.0042,
    "currency": "USD",
    "class": "calculated",
    "pricing_version": "example-2026-08-01"
  },
  "quota": {
    "scope": "weekly-model-pool",
    "unit": "provider_units",
    "remaining": 73.4,
    "observed_at": "2026-08-23T03:00:01Z"
  }
}
```

## Compatibility and Versioning

Schema-version changes that reinterpret an existing field require an explicit migration rule. Implementations SHOULD preserve the original source payload or an auditable source reference where practical.

## Validation

The machine-readable draft schema is `schemas/compute-resource-event.schema.json`.

Before this RFC advances to Candidate, the project requires:

1. examples from at least three materially different provider/execution surfaces;
2. validation of missing/opaque reasoning and cache fields;
3. at least one quota-reset/rolling-window example;
4. one multimodal/native-unit example;
5. mapping notes for OpenTelemetry GenAI conventions where applicable.

## Alternatives Considered

### Universal scalar CU as the base object

Rejected for the current baseline because a defensible universal derivation has not yet been established.

### USD as the common unit

Useful for commercial accounting but not equivalent to physical compute and unstable under repricing, discounts and currency effects.

### Tokens only

Too narrow for multimodal usage, quota-only surfaces and hardware-level measurements.

## Open Questions

See `research/OPEN_QUESTIONS.md`.

## Changelog

- 2026-08: Initial draft created during COMPUTE-COMMONS-REBASELINE-01.
