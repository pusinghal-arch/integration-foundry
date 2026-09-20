# ADR-003: Human approval requirements scale with blast radius, not model confidence

**Status:** Accepted

## Context

It's tempting to set a single confidence threshold above which an agent's action runs autonomously, and below which it goes to a human. That conflates two independent variables: how sure the model is, and how bad it is if the model is wrong. A highly confident, irreversible, financially significant action deserves more scrutiny than an uncertain, reversible, inconsequential one — a single threshold can't express that.

## Decision

The human-approval requirement for any agentic action is set by that action's blast radius — reversibility, financial impact, and downstream data consequences — not by the model's confidence score. Low blast radius (refreshing an expired token, re-triggering a stuck job) can be automated with a lighter gate. Anything that changes financial or master data requires human approval regardless of confidence, unless a separate, explicitly validated trust signal (not raw confidence) says otherwise.

## Consequences

- Every architecture has to classify its own action space by blast radius before deciding what can run autonomously — this classification work doesn't disappear just because a project skips it
- A trust signal (model agreement, data completeness, distribution shift) is a different thing from a confidence score, and conflating them is the failure mode this ADR exists to prevent
- This is more conservative than "ship whatever the model is confident about," on purpose — the cost of getting a low-blast-radius action wrong should be cheap regret, not an incident

## Related

- [Guardrails for agentic AI in ERP](../decision-guides/agentic-ai-guardrails-for-erp.md) — the blast-radius question is one item on a longer checklist
- [Agentic AI in SAP landscapes: shipped vs. announced](../decision-guides/agentic-ai-in-sap-where-things-stand.md) — SAP's own "human-on-the-loop" framing lines up with this position
- [ADR-001](adr-001-agents-recommend-policy-gates-authorize.md) — the policy-gate mechanism this ADR's approval requirement runs through
