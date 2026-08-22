# Problem Statement

AI inference providers expose heterogeneous resource, billing and quota semantics. Consumers can observe token counts, request counts, cache usage, media units, monetary cost, subscription limits or reset windows depending on provider and access surface. These values are useful but are not automatically equivalent measures of compute.

## The Core Problem

A multi-provider system needs to answer questions such as:

- What resources did this task consume?
- How much did it cost under the applicable price schedule?
- How much quota pressure did it create?
- Can two executions be compared fairly?
- Which values are directly observed and which are estimates?

Today these answers are usually encoded in provider-specific application logic. This reduces portability, makes historical accounting fragile and encourages misleading comparisons.

## Why a Single Number Is Dangerous

Four distinct concepts are commonly collapsed:

1. **Usage**: provider-visible consumption such as tokens or media units.
2. **Commercial value**: monetary price under a versioned pricing schedule.
3. **Quota pressure**: consumption against a subscription or service limit.
4. **Physical compute**: hardware work such as accelerator time, FLOPs or energy.

These dimensions can correlate without being interchangeable. A cheap token is not necessarily less physical compute; a quota unit is not necessarily a token; a provider price change does not retroactively change physical work.

## Project Goal

compute-commons aims to define a portable, evidence-preserving accounting model first, then research whether specific normalization functions are justified for specific purposes.

The primary object is therefore a structured resource event, not an assumed universal scalar.

## Success

A successful standard should let a consumer:

- preserve provider-native observations;
- distinguish observed, declared, calculated and estimated fields;
- reconstruct historical commercial cost under the correct pricing version;
- represent quota state without pretending it is physical compute;
- attach provenance and uncertainty to derived values;
- compare providers only along dimensions with defensible semantics;
- extend to multimodal inference without redefining the entire model.

## Non-goals

The current baseline does not define payment rails, agent authorization, a model router, a provider marketplace, training-compute accounting, cryptocurrency, or a mandatory universal CU.
