# ADR-002: Default to asynchronous, event-driven integration

**Status:** Accepted

## Context

Integration designs default to synchronous calls more often than the business process actually requires, usually because synchronous is easier to reason about in a design meeting and easier to demo. That default pushes fragility into places that didn't need it: a caller blocked on a response from a system that's slow or briefly down, for no reason the business process actually cares about.

## Decision

Default to asynchronous, event-driven integration for state changes and cross-system propagation. Reserve synchronous calls for the specific case where the caller has no useful next step without an immediate answer — a credit check before accepting an order, an ATP check before confirming a delivery date.

## Consequences

- Every asynchronous flow has to answer the at-least-once delivery question up front: what happens if this message arrives twice. See the duplicate-detection discussion in the [pattern catalog](../patterns/integration-patterns-catalog.md)
- Synchronous integrations need an explicit answer for what happens on timeout, not just a longer timeout value
- This trades immediate consistency for resilience and decoupling — correct for most cross-system propagation, wrong for the genuinely synchronous minority of cases

## Related

- [Choosing an integration pattern for SAP landscapes](../decision-guides/choosing-integration-pattern.md) — the full decision guide this ADR summarizes
- [Hybrid integration: BTP and legacy middleware coexistence](../architectures/03-hybrid-integration-btp-legacy-coexistence.md) — idempotency requirements when async flows cross a platform boundary
