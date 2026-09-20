# ADR-001: Agents recommend; deterministic policy gates authorize

**Status:** Accepted

## Context

Every architecture in this repository that involves an LLM or agent eventually faces the same question: should the agent itself decide to take the action, or should something else decide whether the agent's suggestion is allowed to happen? Treating "the model is confident" as sufficient grounds to act is the single most common design mistake across agentic-AI writeups, because a model's confidence and an action's authorization are answers to two different questions, and a high score on one says nothing about the other.

## Decision

Agents produce recommendations, rankings, and drafts. A separate, deterministic policy gate — authorization rules, segregation of duties, value limits, data-completeness checks — decides whether a specific action is permitted, independent of how confident the agent was. No model output is allowed to substitute for a failed policy check.

## Consequences

- Every architecture that lets an agent act has to name its policy gate explicitly, not leave it implied
- Blast radius, not model accuracy, determines how much of the action space can be autonomous — see [ADR-003](adr-003-human-approval-scales-with-blast-radius.md)
- This adds real engineering cost (a second system to build and maintain) in exchange for an audit trail that survives the question "why did it do that"

## Related

- [Guardrails for agentic AI in ERP](../decision-guides/agentic-ai-guardrails-for-erp.md) — the full checklist this ADR summarizes
- [Agentic root-cause copilot for SAP interfaces](../architectures/02-agentic-root-cause-copilot-for-interfaces.md) — an example of the boundary drawn narrowly (auto-remediation limited to a pre-approved, reversible action set)
