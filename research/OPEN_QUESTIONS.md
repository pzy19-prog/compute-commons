# Open Questions

These questions are intentionally unresolved. Closing one requires evidence, a decision record or an accepted RFC.

## Measurement Semantics

1. Are input/output/reasoning/cache token categories sufficiently stable for cross-provider comparison?
2. How should providers with opaque or partially exposed reasoning usage be represented?
3. What is the correct event boundary for agentic workloads: request, turn, step, task or trajectory?
4. How should retries, speculative decoding and server-side hidden calls be represented when only partial evidence is exposed?
5. How should images, audio and video preserve native units while still supporting useful comparison?

## Commercial Accounting

6. Should historical cost always be stored as observed charge when available, recalculated from an immutable price schedule, or both?
7. How should negotiated pricing, credits, free tiers and subscription bundles be represented?
8. How should currency conversion be versioned without confusing FX effects with provider repricing?

## Quota

9. Can quota consumption be mapped to request-level events when providers expose only account-level snapshots?
10. How should rolling windows, weekly pools, model-family pools and dynamic rate limits be modeled?
11. Is a normalized quota-pressure metric useful, and if so is it explicitly separate from compute?

## Physical Compute

12. What useful compute proxies can an API consumer obtain without provider cooperation?
13. When is a FLOP estimate meaningful for sparse/MoE, reasoning, batching or speculative decoding systems?
14. Should latency ever be used as a compute proxy, given network and scheduling effects?
15. Can energy/carbon accounting be attached without overstating precision?

## Normalization / CU

16. What exact question should a scalar CU answer?
17. Can one scalar serve both budgeting and physical-compute comparison? Current assumption: probably not without conflating dimensions.
18. Should there be multiple explicitly named indexes instead of one CU, such as commercial-equivalent, quota-pressure and compute-proxy indexes?
19. Who owns normalization coefficients and how are conflicts handled?
20. What uncertainty threshold should prevent a normalized scalar from being emitted?

## Governance

21. What evidence is required to add or change provider semantics?
22. How long must historical normalization/pricing versions remain reproducible?
23. Which parts of the specification should become stable first?
24. What compatibility policy applies when providers change tokenization or usage reporting?
