# SAP integration pattern and error catalog

A working reference for the ten integration patterns that cover most SAP landscapes, and the error codes that show up most often against each. This is the same catalog structure shipped as data in the [companion dataset](../../datasets/sap-erp-integration-dataset/) — this page is the human-readable version, the CSV is the machine-readable one an agent or script can join against.

## Patterns

| ID | Pattern | Technology | Sync/Async | Typical use case | Common challenges |
|---|---|---|---|---|---|
| PAT-001 | Master Data Distribution (ALE) | IDoc | Async | Sync customer/material/vendor master across SAP systems | Filter object maintenance; segment version mismatches across releases |
| PAT-002 | Order-to-Cash IDoc Flow | IDoc | Async | ORDERS/ORDRSP/DESADV/INVOIC exchange with EDI trading partners | Partner-specific mapping variance; sequencing of DESADV before INVOIC |
| PAT-003 | Real-time Order Creation | BAPI | Sync | External web/mobile front-end creates sales orders in real time | Transaction rollback handling; duplicate submission from client retries |
| PAT-004 | Batch Financial Posting | BAPI | Sync (batch-scheduled) | Nightly bulk posting of GL/AP/AR documents from a sub-ledger | Number range contention; partial-batch failure recovery |
| PAT-005 | Remote Function Call Integration | RFC | Sync | Direct calls for lookups (credit check, ATP, pricing) | Connection pool exhaustion; timeout tuning under peak load |
| PAT-006 | S/4HANA API for Cloud Apps | OData | Sync | Cloud app reads/writes business objects via API Business Hub | CSRF token handling; entity deep-insert limitations |
| PAT-007 | Event-Driven Notifications | SAP Event Mesh / Webhook | Async | Publish business events (e.g. goods receipt) to subscribers | At-least-once delivery requiring consumer idempotency |
| PAT-008 | EDI B2B Exchange | EDI (X12/EDIFACT) | Async | POs, ASNs, invoices exchanged with trading partners | Functional acknowledgment SLAs; partner onboarding overhead |
| PAT-009 | Data Replication to Data Lake | CDC / ODP | Async (near real-time) | Replicate SAP tables to a cloud data lake for analytics | Delta queue backlog under high change volume |
| PAT-010 | Middleware Orchestration Hub | Multi-protocol | Mixed | Central platform brokering SAP and 20+ non-SAP systems | Interface sprawl; inconsistent error-handling standards |

For guidance on choosing between these, see [Choosing an integration pattern for SAP landscapes](../decision-guides/choosing-integration-pattern.md).

## Error catalog highlights

The full catalog covers IDoc, BAPI, RFC, OData, EDI, and CPI errors with likely cause and resolution steps. A few worth knowing by number because they come up constantly:

| Type | Code | Short description | Likely cause | Severity |
|---|---|---|---|---|
| IDoc | 51 | Application document not posted | Missing referenced master data in target system | High |
| IDoc | 64 | IDoc ready to be transferred | Not actually an error — inbound processing job isn't running | Medium |
| IDoc | 20 | Error passing data to port | RFC destination or file port unreachable | Critical |
| BAPI | E-102 | Commit not executed | Caller never called `BAPI_TRANSACTION_COMMIT` | High |
| RFC | RFC_ERROR_LOGON_FAILURE | Logon failure to remote system | Expired password or locked service user | High |
| OData | 403 | Forbidden — CSRF token missing | Write sent without fetching `X-CSRF-Token` first | Medium |
| OData | 409 | Conflict — concurrent modification | ETag mismatch; entity changed since last read | Medium |
| CPI | MPL-RETRY-EXHAUSTED | Retry count exhausted | Persistent downstream failure past retry limit | Critical |

The distinction between IDoc status 51 and 64 is a good illustration of why a maintained catalog beats institutional memory: both look like "something's stuck," but one means a data problem in the target system and the other means a scheduling problem with your own background jobs — same visible symptom, completely different fix, and the on-call engineer either knows this from experience or burns twenty minutes rediscovering it.

Full catalog: [`integration_error_catalog.csv`](../../datasets/sap-erp-integration-dataset/data/integration_error_catalog.csv) (27 entries).

## Related

- [Agentic root-cause copilot for SAP interfaces](../architectures/02-agentic-root-cause-copilot-for-interfaces.md) — an architecture that consumes this catalog programmatically to triage errors automatically
- [Choosing an integration pattern for SAP landscapes](../decision-guides/choosing-integration-pattern.md)
