# RFC Process

## Statuses

- **Draft** — proposal under active development.
- **Research Required** — blocked on evidence or unresolved semantics.
- **Candidate** — specification text considered implementable and ready for independent validation.
- **Accepted** — approved normative specification.
- **Historical** — preserved for lineage but no longer normative.
- **Superseded** — replaced by an identified successor RFC.
- **Rejected** — considered and intentionally not adopted.

## Required RFC Sections

Every normative RFC should include:

1. abstract;
2. problem and scope;
3. terminology;
4. normative specification;
5. provenance/version semantics;
6. compatibility and migration;
7. security/privacy considerations where relevant;
8. alternatives considered;
9. validation evidence;
10. unresolved questions;
11. changelog.

## Evidence Rule

Claims about provider behavior, production implementations or interoperability must identify reproducible evidence. A repository path alone is insufficient when the claimed behavior depends on runtime state.

## Compatibility Rule

Provider-native observations must remain recoverable. New normalization methods or schema versions must not silently reinterpret historical records.

## Acceptance Gate

An RFC should not become Accepted solely because one internal implementation works. At minimum:

- the semantics are internally consistent;
- examples validate against the machine-readable schema where applicable;
- at least one implementation or dataset demonstrates the proposal;
- unresolved questions that affect core semantics are closed or explicitly deferred;
- known limitations are documented.

## Historical Preservation

Early designs that materially influenced later work should normally be reclassified rather than deleted. Superseded RFCs must point to their successor.
