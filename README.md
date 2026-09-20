# Intelligent Enterprise Integration Architecture Foundry

Reference architectures, decision guides, and open data for the place where SAP, enterprise integration, and agentic AI actually meet operational reality — including the parts of that reality specific to oil & gas and other heavy-asset industries, where most public architecture content doesn't bother going.

**Browse the searchable site: [pusinghal-arch.github.io/integration-foundry](https://pusinghal-arch.github.io/integration-foundry/)**

[![License: CC BY 4.0](https://img.shields.io/badge/docs-CC%20BY%204.0-blue.svg)](LICENSE-DOCS.md)
[![License: MIT](https://img.shields.io/badge/code-MIT-green.svg)](LICENSE)

## Why this exists

Most enterprise integration knowledge lives in three places: vendor documentation that describes what a product does but not when to use it, consulting decks that never leave the client who paid for them, and forum threads answering one narrow question at a time. There's very little that sits between those — architecture written the way a practitioner would explain it to another practitioner, with the tradeoffs and failure modes included, published where it can actually be reused and argued with.

This repository is that middle layer, built from real integration and architecture work: SAP finance, ERP-to-ERP data flows, industrial IoT into asset management, and the operational mess that shows up when agentic AI is asked to do more than generate a suggestion. It leads with SAP because that's the deepest expertise behind it, and it doesn't stop at SAP, because most of the hard integration problems in a large enterprise happen at the boundary between SAP and everything else.

## How this fits together

Every architecture in this repository sits somewhere on the same path, whether or not the document says so explicitly:

**Systems of record → Integration → Context → Reasoning → Governed action**

- **Systems of record** — SAP and the other transactional systems that hold the data of consequence
- **Integration** — the APIs, events, and middleware that move that data without corrupting it
- **Context** — the master data, ownership, and historical outcomes an agent or a human needs to interpret a situation correctly
- **Reasoning** — the model, agent, or rules engine proposing a classification, ranking, or recommendation
- **Governed action** — the policy gate and audit trail deciding whether that recommendation is actually allowed to happen ([ADR-001](docs/decisions/adr-001-agents-recommend-policy-gates-authorize.md))

The path loops back on itself — every architecture that's worth including here feeds its outcomes back into Context, not just forward into Action:

**Systems of record → Integration → Context → Reasoning → Governed action → (outcome feeds back into Context)**

This isn't a diagram flourish. It's concrete in the architectures themselves: the [root-cause copilot](docs/architectures/02-agentic-root-cause-copilot-for-interfaces.md)'s remediation outcomes feed back into its ranking model, the [joint venture cutback](docs/architectures/07-joint-venture-cutback-cross-erp-billing.md) architecture routes partner disputes back into the billing process that produced them, and the [field measurement](docs/architectures/06-field-measurement-to-production-revenue-accounting.md) architecture explicitly reprocesses allocation when a late correction arrives. An architecture that only points forward has no way to get better at the thing it's already doing, and no way to notice when the conditions it was designed under have quietly changed.

Most architecture writeups collapse Reasoning and Governed action into one step, which is exactly the assumption [the guardrails checklist](docs/decision-guides/agentic-ai-guardrails-for-erp.md) and the [ADRs](docs/decisions/index.md) argue against. Before committing to a design, run it through the [quick self-test](docs/decision-guides/architecture-self-test.md) — eight questions, five minutes.

## Reference architectures

**Cross-industry**

| Architecture | Domain | What it solves |
|---|---|---|
| [Agentic root-cause copilot for SAP interfaces](docs/architectures/02-agentic-root-cause-copilot-for-interfaces.md) | Integration operations | Turning IDoc/BAPI/RFC/OData/EDI/CPI error events into ranked, evidence-backed remediation instead of a status code and a runbook search |
| [Hybrid integration: BTP and legacy middleware coexistence](docs/architectures/03-hybrid-integration-btp-legacy-coexistence.md) | Enterprise integration | Running SAP PI/PO (or another iPaaS) and SAP BTP Integration Suite side by side for the length of a real migration, without duplicate processing or lost ownership |
| [Agentic supplier risk and performance reasoning](docs/architectures/12-agentic-supplier-risk-and-performance-reasoning.md) | Procurement, SAP Ariba | Joining supplier risk signals against actual spend/contract exposure before treating a risk score as actionable |

**Oil & gas**

| Architecture | Domain | What it solves |
|---|---|---|
| [Field telemetry to SAP EAM for upstream/midstream assets](docs/architectures/04-iot-to-sap-eam-upstream-midstream.md) | Industrial IoT | Converting continuous sensor telemetry into maintenance notifications a planner can trust, instead of alert fatigue |
| [Multi-ERP master data governance for M&A-heavy portfolios](docs/architectures/05-multi-erp-master-data-governance-mna.md) | Master data | Reconciling vendor, material, and customer identity across ERP instances left behind by acquisitions, divestitures, and joint ventures |
| [Field measurement to Production and Revenue Accounting](docs/architectures/06-field-measurement-to-production-revenue-accounting.md) | Upstream, SAP PRA | Getting historian-based field measurement (AVEVA PI/SCADA) into SAP's allocation and revenue-accounting engine without forcing a historian to answer relational questions it wasn't built for |
| [Joint venture cutback and cross-ERP partner billing](docs/architectures/07-joint-venture-cutback-cross-erp-billing.md) | Upstream, SAP JVA | Billing non-operating partners on a different ERP entirely, with a defensible audit trail back to source AFEs |
| [Terminal measurement to ledger: gain/loss reconciliation](docs/architectures/08-terminal-measurement-gain-loss-reconciliation.md) | Midstream/downstream | Reconciling physical, temperature-corrected terminal volumes against contract volumes with an audit trail, not a black-box auto-posting |
| [Trading and scheduling orchestration across Commodity Management, TSW, and TM](docs/architectures/09-trading-scheduling-orchestration-tsw-tm.md) | Trading & logistics | Keeping a physical swap consistent across the trade, the schedule, and the transport when any one of them changes mid-stream |
| [Permit-to-work as a safety gate on Plant Maintenance](docs/architectures/10-permit-to-work-safety-gate-plant-maintenance.md) | Safety, SAP PM-WCM | Configuring SAP's native permit-to-work state machine so it's a real safety gate, not a checklist formality |
| [Bridging continuous emissions monitoring into SAP Environment Management](docs/architectures/11-cems-emissions-to-sap-ehs-environment-management.md) | Environmental compliance | Closing a real gap in SAP's out-of-box connectivity between CEMS hardware and emissions compliance reporting |

## Decision guides

- [A quick self-test for any proposed architecture](docs/decision-guides/architecture-self-test.md) — eight questions, five minutes, before you commit to a design
- [SAP's oil & gas solution landscape: a map for architects](docs/decision-guides/sap-oil-gas-solution-landscape.md) — current terminology (IS-Oil to S/4HANA), what integrates with what, and where the architectures above fit
- [Choosing an integration pattern for SAP landscapes](docs/decision-guides/choosing-integration-pattern.md) — sync vs. async, IDoc vs. BAPI vs. OData vs. event-driven, and the failure-mode questions that should drive the choice
- [Guardrails for agentic AI in ERP: a policy-gate checklist](docs/decision-guides/agentic-ai-guardrails-for-erp.md) — what has to be true before an agent is allowed to act autonomously inside an ERP system, generalized from the finance-posting architecture
- [Agentic AI in SAP landscapes: what's actually shipped versus announced](docs/decision-guides/agentic-ai-in-sap-where-things-stand.md) — separating SAP's shipped Joule/AI Agent Hub capabilities from roadmap announcements, and where SAP's own governance direction lines up with the guardrails checklist above

## Architecture Decision Records

Short, standing positions this repository takes across every architecture in it — not "how to choose," but "what we decided and why." See [docs/decisions/](docs/decisions/index.md):

- [ADR-001: Agents recommend; deterministic policy gates authorize](docs/decisions/adr-001-agents-recommend-policy-gates-authorize.md)
- [ADR-002: Default to asynchronous, event-driven integration](docs/decisions/adr-002-async-by-default.md)
- [ADR-003: Human approval requirements scale with blast radius, not model confidence](docs/decisions/adr-003-human-approval-scales-with-blast-radius.md)

## Pattern and error catalog

- [SAP integration pattern and error catalog](docs/patterns/integration-patterns-catalog.md) — the ten patterns that cover most SAP landscapes, and the error codes that come up most often against each

## Dataset

[`datasets/sap-erp-integration-dataset/`](datasets/sap-erp-integration-dataset/) — a synthetic, referentially-linked SAP/ERP dataset covering master data, order-to-cash transactions, financial postings, and IDoc/BAPI/RFC/OData error patterns. Released under CC0 (public domain). Built specifically because production SAP data is confidential and public datasets for this kind of integration and anomaly-detection work barely exist. Use it to prototype the [root-cause copilot](docs/architectures/02-agentic-root-cause-copilot-for-interfaces.md) without touching anything real.

## Using this repository

Each document under `docs/` follows the same structure: the actual problem (not a restated feature list), the architecture with a diagram, the two or three design decisions that matter most and why, when the pattern fits, and — just as important — when it doesn't. Start from whichever architecture matches the problem in front of you; the "Related" section at the bottom of each links sideways to the ones that share a design principle. Where a document draws on SAP-specific terminology or public research, a "Sources" section at the bottom links to what it's actually based on.

Diagrams are Mermaid, inline in the Markdown, so they render directly on GitHub in both light and dark themes and stay diffable in pull requests — no exported images to regenerate every time a box moves.

## Automation

- `./scripts/check-links.sh` — verifies every relative Markdown link in the repo resolves to a real file. Runs in CI on every push and pull request.
- `./scripts/validate-mermaid.sh` — extracts every Mermaid block under `docs/` and renders it with [mermaid-cli](https://github.com/mermaid-js/mermaid-cli) to catch syntax errors before they hit a PR. Runs in CI (needs `npm install -g @mermaid-js/mermaid-cli` locally).
- `./scripts/new-architecture.sh <slug>` — scaffolds a new numbered architecture doc from `templates/architecture-template.md`.
- CI ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)) also runs a best-effort external link check ([lychee](https://github.com/lycheeverse/lychee)) against every source citation, non-blocking since SAP Community and vendor sites routinely rate-limit or 403 automated checks.
- The searchable site is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) from `mkdocs.yml` and deployed to GitHub Pages by [`.github/workflows/docs.yml`](.github/workflows/docs.yml) on every push to `main`. Build locally with `pip install -r requirements.txt && mkdocs serve`.

## Contributing

Real-world corrections and new architectures grounded in actual experience are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) — it's short, and it says no to a few things on purpose.

## License

Written content (`docs/`) is [CC BY 4.0](LICENSE-DOCS.md). Code and the dataset generators are [MIT](LICENSE). SAP, IDoc, BAPI, S/4HANA, and related terms are used descriptively to refer to the technologies discussed and are trademarks of SAP SE; this project is independent and not affiliated with or endorsed by SAP.

Citation metadata is in [CITATION.cff](CITATION.cff) — GitHub surfaces this automatically as a "Cite this repository" option in the sidebar.

## About

Written and maintained by [Puneet Singhal](https://github.com/pusinghal-arch) — Senior Member, IEEE, and enterprise integration architect working across SAP S/4HANA, integration platforms, and agentic AI, with a focus on oil & gas and other heavy-asset industries.

*LinkedIn and additional publication links to be added.*
