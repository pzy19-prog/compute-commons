# Terminology

This document defines working terms for the research baseline. Terms may become normative only through an accepted RFC.

| Term | Working definition |
|---|---|
| **Resource Event** | A timestamped record describing provider-native inference usage and related accounting evidence for an execution boundary. |
| **Usage** | Directly observed or provider-reported consumption such as input tokens, output tokens, cache activity, requests or media units. |
| **Commercial Cost** | Monetary charge or calculated price under a named/versioned pricing schedule. |
| **Quota** | A provider- or subscription-defined allowance, limit, remaining balance or reset cycle. |
| **Compute Proxy** | A measurement or estimate intended to approximate physical compute, such as accelerator seconds, FLOPs or energy. |
| **Native Unit** | A provider-defined unit retained without normalization. |
| **Normalization** | An explicit transformation from one or more source dimensions to a comparable representation for a stated purpose. |
| **Normalization Method** | The versioned formula, coefficients and assumptions used to derive a normalized value. |
| **CU / Compute Unit** | Historical name for a proposed scalar normalization unit. In the current baseline CU is a hypothesis under evaluation, not a canonical unit. |
| **Provider Declaration** | Provider- or adapter-supplied metadata describing semantics, pricing, quota rules or model identifiers. It is evidence with provenance, not automatically ground truth. |
| **Observation Source** | API response, CLI output, proxy telemetry, billing export, infrastructure telemetry or other origin of a field. |
| **Provenance** | Metadata identifying where a value came from and how a derived value was produced. |
| **Confidence** | An optional bounded assessment of evidence quality for estimated or inferred values. |
| **Pricing Version** | An immutable identifier or effective-time reference for the price schedule used to calculate commercial cost. |
| **Quota Snapshot** | Quota state observed at a particular time. It is stateful and should not be treated as an immutable per-request usage measurement. |
| **Execution Boundary** | The task, request, model call, agent step or other unit for which a Resource Event is recorded. |

## Evidence Classes

The baseline distinguishes:

- **observed** — directly returned by an authoritative execution surface;
- **declared** — supplied by a provider/configuration/registry;
- **calculated** — deterministically derived from cited inputs and a versioned method;
- **estimated** — inferred from incomplete evidence and accompanied by uncertainty metadata.

## Reserved Distinctions

The following terms must not be used interchangeably without an explicit mapping:

- tokens and compute;
- cost and compute;
- quota and cost;
- quota and usage;
- model capability and resource consumption;
- latency and accelerator time.
