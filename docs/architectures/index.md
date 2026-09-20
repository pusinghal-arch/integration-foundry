# Reference architectures

Each architecture below follows the same structure: the actual problem (not a restated feature list), the architecture with a diagram, the two or three design decisions that matter most and why, when the pattern fits, and — just as important — when it doesn't. The "Related" section at the bottom of each links sideways to the ones that share a design principle.

## Cross-industry

| Architecture | Domain | What it solves |
|---|---|---|
| [Agentic root-cause copilot for SAP interfaces](02-agentic-root-cause-copilot-for-interfaces.md) | Integration operations | Turning IDoc/BAPI/RFC/OData/EDI/CPI error events into ranked, evidence-backed remediation instead of a status code and a runbook search |
| [Hybrid integration: BTP and legacy middleware coexistence](03-hybrid-integration-btp-legacy-coexistence.md) | Enterprise integration | Running SAP PI/PO (or another iPaaS) and SAP BTP Integration Suite side by side for the length of a real migration, without duplicate processing or lost ownership |

## Oil & gas

| Architecture | Domain | What it solves |
|---|---|---|
| [Field telemetry to SAP EAM for upstream/midstream assets](04-iot-to-sap-eam-upstream-midstream.md) | Industrial IoT | Converting continuous sensor telemetry into maintenance notifications a planner can trust, instead of alert fatigue |
| [Multi-ERP master data governance for M&A-heavy portfolios](05-multi-erp-master-data-governance-mna.md) | Master data | Reconciling vendor, material, and customer identity across ERP instances left behind by acquisitions, divestitures, and joint ventures |
| [Field measurement to Production and Revenue Accounting](06-field-measurement-to-production-revenue-accounting.md) | Upstream, SAP PRA | Getting historian-based field measurement (AVEVA PI/SCADA) into SAP's allocation and revenue-accounting engine |
| [Joint venture cutback and cross-ERP partner billing](07-joint-venture-cutback-cross-erp-billing.md) | Upstream, SAP JVA | Billing non-operating partners on a different ERP entirely, with a defensible audit trail back to source AFEs |
| [Terminal measurement to ledger: gain/loss reconciliation](08-terminal-measurement-gain-loss-reconciliation.md) | Midstream/downstream | Reconciling physical, temperature-corrected terminal volumes against contract volumes with an audit trail |
| [Trading and scheduling orchestration across Commodity Management, TSW, and TM](09-trading-scheduling-orchestration-tsw-tm.md) | Trading & logistics | Keeping a physical swap consistent across the trade, the schedule, and the transport when any one of them changes mid-stream |
| [Permit-to-work as a safety gate on Plant Maintenance](10-permit-to-work-safety-gate-plant-maintenance.md) | Safety, SAP PM-WCM | Configuring SAP's native permit-to-work state machine so it's a real safety gate, not a checklist formality |
| [Bridging continuous emissions monitoring into SAP Environment Management](11-cems-emissions-to-sap-ehs-environment-management.md) | Environmental compliance | Closing a real gap in SAP's out-of-box connectivity between CEMS hardware and emissions compliance reporting |

Not sure where to start? [SAP's oil & gas solution landscape](../decision-guides/sap-oil-gas-solution-landscape.md) maps current SAP terminology to the architectures above, if you're trying to match a business problem to the right document.
