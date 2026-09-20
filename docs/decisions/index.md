# Architecture Decision Records

The [decision guides](../decision-guides/sap-oil-gas-solution-landscape.md) elsewhere in this repository explain how to choose between options for a specific problem. ADRs are different: each one records a standing position this repository takes across *every* architecture in it — a rule you can point to when a new design has to decide the same question again, so the reasoning doesn't get re-litigated from scratch each time.

Format is deliberately terse: context, decision, consequences. If you're looking for the fuller reasoning and tradeoffs behind a position, the architecture and decision-guide docs linked from each ADR go deeper.

| ADR | Decision |
|---|---|
| [ADR-001](adr-001-agents-recommend-policy-gates-authorize.md) | Agents recommend; deterministic policy gates authorize |
| [ADR-002](adr-002-async-by-default.md) | Default to asynchronous, event-driven integration |
| [ADR-003](adr-003-human-approval-scales-with-blast-radius.md) | Human approval requirements scale with blast radius, not model confidence |

New ADRs are numbered sequentially and never renumbered or deleted once merged — if a decision changes, add a new ADR that supersedes it and says so, rather than editing history.
