# Experiments

This directory holds empirical validation for compute-commons proposals. Experiments should test semantic claims rather than merely demonstrate code execution.

## Initial Validation Matrix

The first validation set should include materially different execution surfaces:

1. token-billed text API with input/output usage;
2. provider or CLI surface exposing subscription/quota state;
3. cache-aware provider usage;
4. reasoning-token or opaque-reasoning case;
5. multimodal/native-unit case;
6. a pricing change that proves historical accounting reproducibility.

CLI Quota Watch is a candidate source for quota and usage evidence. Its raw/provider-native observations should be retained before any compute-commons normalization.

## Experiment Requirements

Each experiment should record:

- objective and hypothesis;
- provider/surface and effective date;
- raw evidence or a reproducible evidence reference;
- schema version;
- transformation/normalization method versions;
- expected result;
- actual result;
- limitations and unresolved ambiguity.

## Prohibited Shortcuts

- Do not replace missing values with zero.
- Do not label price-derived indexes as physical compute.
- Do not infer request-level quota consumption from account snapshots without marking the inference.
- Do not claim provider behavior from documentation alone when the experiment is intended to validate runtime behavior.

## Phase 1 Exit Evidence

At least three heterogeneous provider/surface examples must validate against the draft schema before RFC-0002 can advance to Candidate.
