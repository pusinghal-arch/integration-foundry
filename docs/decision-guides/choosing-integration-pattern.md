# Choosing an integration pattern for SAP landscapes

Most integration design mistakes trace back to picking the pattern that was easiest to demo, not the one that matches the actual failure modes of the use case. This guide is a set of questions to ask before defaulting to whatever technology the team already knows.

## Start with the failure mode you can least afford

Not "how fast does this need to be" — that's usually answered wrong, in the direction of "as fast as possible," which pushes everything toward synchronous calls even when the business process doesn't actually need a synchronous answer. Ask instead: if the receiving system is down for ten minutes, what has to happen? If the answer is "nothing breaks, it catches up when the system comes back," you want asynchronous. If the answer is "the calling process cannot proceed without an answer right now" — a credit check before an order is accepted, an ATP check before confirming a delivery date — you want synchronous, and you need to design explicitly for what happens when the synchronous call times out.

| If you need... | Lean toward | Because |
|---|---|---|
| An immediate yes/no the caller acts on | Sync (RFC, OData, BAPI) | The caller has no useful next step without the answer |
| Guaranteed eventual delivery, no immediate response needed | Async (IDoc, Event Mesh, queued messaging) | Decouples availability — the sender doesn't need the receiver up at the same instant |
| High volume, non-urgent, tolerant of delay | Async batch (scheduled BAPI, CDC replication) | Batching amortizes overhead; urgency doesn't justify the connection overhead of per-transaction sync calls |
| External partner exchange with compliance/audit requirements | EDI, or OData/API with strict versioning | Partners need stable contracts and acknowledgment semantics your internal services don't |

## Match the pattern to who owns the schema

IDoc and EDI both assume a fairly stable, jointly-agreed message schema — that's their strength for stable partner relationships and their weakness for anything evolving fast. OData and REST APIs assume the provider owns and versions the schema, and consumers adapt — better fit when you control the SAP side and the consumers are internal or under your influence. Getting this backwards shows up later as either partners breaking every time you touch a field (should have used a versioned API contract) or an internal team unable to add a field without a multi-week EDI change-control process (should have used OData).

## Don't let "everything through one platform" become the default

A middleware orchestration hub (MuleSoft, Boomi, SAP CPI, webMethods) brokering between SAP and dozens of non-SAP systems is a real, common, and reasonable pattern — but it earns its complexity when the alternative is genuinely worse: 20+ point-to-point connections nobody can reason about as a whole. If there are five interfaces, five point-to-point connections with clear ownership are easier to operate than a hub with all the associated platform overhead. The switchover point isn't a fixed number — it's whether anyone can currently draw an accurate picture of what talks to what without archaeology.

## Ask what happens on a duplicate message before you ask about throughput

Every asynchronous pattern (IDoc, Event Mesh, queued messaging) has to answer: what happens if the same message arrives twice? At-least-once delivery is the norm, not the exception, for anything using a message queue or event broker. If the consuming logic isn't idempotent — checking a natural key before creating a record, rather than assuming "one message equals one create" — a network blip that causes a harmless retry becomes a duplicate sales order or a double-posted invoice. This gets skipped in design reviews because it doesn't show up until the system has run in production long enough to hit a retry, and by then it's a production incident instead of a design decision.

## Related

- [Integration pattern and error catalog](../patterns/integration-patterns-catalog.md) — the ten patterns referenced above, with common failure modes for each
- [Hybrid integration: SAP BTP Integration Suite and legacy middleware coexistence](../architectures/03-hybrid-integration-btp-legacy-coexistence.md)
