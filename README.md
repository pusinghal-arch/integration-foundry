# Intelligent Enterprise Integration Architecture Foundry

Reference architectures, decision guides, and open data for the place where SAP, enterprise integration, and agentic AI actually meet operational reality — including the parts of that reality specific to oil & gas and other heavy-asset industries, where most public architecture content doesn't bother going.

[![License: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-blue.svg)](LICENSE-DOCS.md)
[![License: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)

## Why this exists

Most SAP integration knowledge lives in three places: vendor documentation that describes what a product does but not when to use it, consulting decks that never leave the client who paid for them, and forum threads answering one narrow question at a time. There's very little that sits between those — architecture written the way a practitioner would explain it to another practitioner, with the tradeoffs and failure modes included, published where it can actually be reused and argued with.

This repository is that middle layer, built from real integration and architecture work: SAP finance, ERP-to-ERP data flows, industrial IoT into asset management, and the operational mess that shows up when agentic AI is asked to do more than generate a suggestion. It leads with SAP because that's the deepest expertise behind it, and it doesn't stop at SAP, because most of the hard integration problems in a large enterprise happen at the boundary between SAP and everything else.

## Reference architectures

| Architecture | Domain | What it solves |
|---|---|---|
| [Trust-aware agentic finance posting](docs/architectures/01-trust-aware-agentic-finance-posting.md) | SAP FI/CO, agentic AI | Letting an agent recommend or execute a posting without letting model confidence override authorization, SoD, or policy controls |
| [Agentic root-cause copilot for SAP interfaces](docs/architectures/02-agentic-root-cause-copilot-for-interfaces.md) | Integration operations | Turning IDoc/BAPI/RFC/OData/EDI/CPI error events into ranked, evidence-backed remediation instead of a status code and a runbook search |
| [Hybrid integration: BTP and legacy middleware coexistence](docs/architectures/03-hybrid-integration-btp-legacy-coexistence.md) | Enterprise integration | Running SAP PI/PO (or another iPaaS) and SAP BTP Integration Suite side by side for the length of a real migration, without duplicate processing or lost ownership |
| [Field telemetry to SAP EAM for upstream/midstream assets](docs/architectures/04-iot-to-sap-eam-upstream-midstream.md) | Industrial IoT, oil & gas | Converting continuous sensor telemetry into maintenance notifications a planner can trust, instead of alert fatigue |
| [Multi-ERP master data governance for M&A-heavy portfolios](docs/architectures/05-multi-erp-master-data-governance-mna.md) | Master data, oil & gas | Reconciling vendor, material, and customer identity across ERP instances left behind by acquisitions, divestitures, and joint ventures |

## Decision guides

- [Choosing an integration pattern for SAP landscapes](docs/decision-guides/choosing-integration-pattern.md) — sync vs. async, IDoc vs. BAPI vs. OData vs. event-driven, and the failure-mode questions that should drive the choice
- [Guardrails for agentic AI in ERP: a policy-gate checklist](docs/decision-guides/agentic-ai-guardrails-for-erp.md) — what has to be true before an agent is allowed to act autonomously inside an ERP system, generalized from the finance-posting architecture

## Pattern and error catalog

- [SAP integration pattern and error catalog](docs/patterns/integration-patterns-catalog.md) — the ten patterns that cover most SAP landscapes, and the error codes that come up most often against each

## Dataset

[`datasets/sap-erp-integration-dataset/`](datasets/sap-erp-integration-dataset/) — a synthetic, referentially-linked SAP/ERP dataset covering master data, order-to-cash transactions, financial postings, and IDoc/BAPI/RFC/OData error patterns. Released under CC0 (public domain). Built specifically because production SAP data is confidential and public datasets for this kind of integration and anomaly-detection work barely exist. Use it to prototype the [root-cause copilot](docs/architectures/02-agentic-root-cause-copilot-for-interfaces.md) or the [finance posting controller](docs/architectures/01-trust-aware-agentic-finance-posting.md) without touching anything real.

## Research

**Puneet Singhal**, "TA-SAP: Trust-Aware Agentic AI for Policy-Constrained SAP Finance Posting and Human Escalation." The paper behind the [trust-aware finance posting architecture](docs/architectures/01-trust-aware-agentic-finance-posting.md) — full methodology, ensemble anomaly detection design, and the evaluation numbers cited in that document.

*Citation and link to the published or preprint version to be added once available.*

## Using this repository

Each document under `docs/` follows the same structure: the actual problem (not a restated feature list), the architecture with a diagram, the two or three design decisions that matter most and why, when the pattern fits, and — just as important — when it doesn't. Start from whichever architecture matches the problem in front of you; the "Related" section at the bottom of each links sideways to the ones that share a design principle.

Diagrams are Mermaid, inline in the Markdown, so they render directly on GitHub in both light and dark themes and stay diffable in pull requests — no exported images to regenerate every time a box moves.

## Contributing

Real-world corrections and new architectures grounded in actual experience are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) — it's short, and it says no to a few things on purpose.

## License

Written content (`docs/`) is [CC BY 4.0](LICENSE-DOCS.md). Code and the dataset generators are [MIT](LICENSE). SAP, IDoc, BAPI, S/4HANA, and related terms are used descriptively to refer to the technologies discussed and are trademarks of SAP SE; this project is independent and not affiliated with or endorsed by SAP.

## About

Written and maintained by [Puneet Singhal](https://github.com/puneetsinghal83) — Senior Member, IEEE, and enterprise integration architect working across SAP S/4HANA, integration platforms, and agentic AI, with a focus on oil & gas and other heavy-asset industries.

*LinkedIn and additional publication links to be added.*
