# A quick self-test for any proposed architecture

Eight questions, meant to take five minutes, not a design review. Use this before committing to a design; use the [guardrails checklist](agentic-ai-guardrails-for-erp.md) once the design is real enough to need the full treatment.

1. **Which system owns the authoritative business state here — and does the design actually read from it, or from a copy that can drift?** A cache, an extract, or a replicated table is not the same as the system of record, and the gap between them is where stale data quietly causes wrong decisions.

2. **What does the reasoning layer have access to that a human reviewer wouldn't also need to reach the same conclusion?** If the honest answer is "nothing, it just does it faster," that's fine — say so. If the answer is unclear, the design probably hasn't defined what evidence the reasoning is actually built on.

3. **What is the worst plausible consequence if this specific recommendation is wrong, and who bears it?** Not the average case — the worst case. This is the blast-radius question, and it should drive the next two answers, not the model's confidence score.

4. **Is there a policy gate between the recommendation and the action, or does confidence alone decide?** See [ADR-001](../decisions/adr-001-agents-recommend-policy-gates-authorize.md). If a low anomaly score or a high confidence score is what makes an action happen, there is no gate — there's a suggestion with extra steps.

5. **Given the blast radius from question 3, does this action require a human, or is it genuinely in a pre-approved, reversible set?** See [ADR-003](../decisions/adr-003-human-approval-scales-with-blast-radius.md). Naming the pre-approved set explicitly, rather than leaving it implicit, is what makes this answerable later.

6. **If this integration is synchronous, would anything actually break by making it asynchronous — or is synchronous just the default nobody questioned?** See [ADR-002](../decisions/adr-002-async-by-default.md). "It felt more responsive in the demo" is not a business requirement.

7. **What evidence gets logged with the decision, and could someone reconstruct why it happened six months from now?** If the answer requires re-running the model or guessing, the audit trail is decorative.

8. **What in this design updates automatically as the business changes, and what will quietly go stale?** Master data mappings, thresholds, and role assignments all rot. Name the ones in this design and who's responsible for noticing when they do.

## Related

- [Guardrails for agentic AI in ERP](agentic-ai-guardrails-for-erp.md) — the full checklist for a design that's past this quick pass
- [Architecture Decision Records](../decisions/index.md) — the standing positions questions 4-6 are drawn from
