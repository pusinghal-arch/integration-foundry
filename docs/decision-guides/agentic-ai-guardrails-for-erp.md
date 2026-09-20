# Guardrails for agentic AI in ERP: a policy-gate checklist

A checklist for any agent that can take an action inside an ERP system — postings, master data changes, workflow approvals, procurement actions. If you can't answer these questions about a proposed agent, it isn't ready to act autonomously yet, whatever its model accuracy looks like in a demo.

## Before the agent can act at all

**Can you state, in a form the system checks mechanically, what this agent is and isn't authorized to do?** Not "the agent is trained to be careful" — an actual authorization boundary: which company codes, which transaction types, which value limits, which fields. If the answer is "we trust the model's judgment," the agent doesn't have a policy gate, it has a suggestion that nobody is actually gating.

**Is the authorization check independent of the model's confidence?** A model that's 99% confident about an unauthorized action is still an unauthorized action. The most common design mistake here is letting a high confidence score substitute for an authorization check instead of sitting behind it. Confidence should influence whether a *permitted* action needs human sign-off — it should never be what makes an action permitted.

**Does segregation of duties survive contact with an agent?** If a human couldn't both create and approve the same transaction under your controls, an agent acting on behalf of that human shouldn't be able to either, and an agent acting as "the system" needs its own SoD conflicts checked against its own action history, not exempted because it isn't a named human user.

## Before the agent can act autonomously, not just recommend

**Do you have a real trust signal, separate from the risk score?** Risk asks "is this unusual." Trust asks "should the system believe its own assessment right now" — model agreement, data completeness, and how far the current case sits from the conditions the system was validated under. Without a trust signal, the system has no way to reduce autonomy automatically when it's operating outside its validated conditions — it just keeps acting confidently until an audit or an incident catches it.

**What is the blast radius if this specific action is wrong, and does the action set match it?** Auto-remediating a stuck background job is low blast radius — reversible, no data changed. Auto-posting a financial document is not. The line between "safe to automate" and "needs a human" should be drawn by blast radius and reversibility, not by how good the model's accuracy metric looks on a test set.

**Is there a case where a human reviewed the agent's recommendation and confirmed it was wrong — and does the system learn from that?** A reliability estimate that never updates from actual reviewer outcomes drifts away from reality the moment the business context changes. This is what separates a system that degrades gracefully under change from one that fails silently until someone notices months later.

## Before you trust the audit trail

**Can you reconstruct, after the fact, exactly why the agent did what it did?** Not just "the model said so" — the specific evidence: which policy checks passed, what the risk and trust scores were, what alternative actions were considered and rejected. If a regulator, auditor, or your own incident review can't reconstruct the decision, the audit trail is decorative.

**Does the audit log capture the outcome, not just the action?** An action without a recorded outcome (was the recommendation correct? did the auto-remediation actually fix the problem?) can't feed back into the trust or reliability estimate, and the system can't tell the difference between "working well" and "nobody's checked in three months."

## Related

- [Agentic root-cause copilot for SAP interfaces](../architectures/02-agentic-root-cause-copilot-for-interfaces.md) — this checklist applied to a lower-stakes domain, showing how the answers change with blast radius
- [Agentic AI in SAP landscapes: what's actually shipped versus announced](agentic-ai-in-sap-where-things-stand.md) — how this checklist compares to SAP's own governance direction (Joule, AI Agent Hub)
