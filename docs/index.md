# Intelligent Enterprise Integration Architecture Foundry

Reference architectures, decision guides, and open data for the place where SAP, enterprise integration, and agentic AI actually meet operational reality — including the parts of that reality specific to oil & gas and other heavy-asset industries, where most public architecture content doesn't bother going.

## Why this exists

Most SAP integration knowledge lives in three places: vendor documentation that describes what a product does but not when to use it, consulting decks that never leave the client who paid for them, and forum threads answering one narrow question at a time. There's very little that sits between those — architecture written the way a practitioner would explain it to another practitioner, with the tradeoffs and failure modes included, published where it can actually be reused and argued with.

This site is that middle layer, built from real integration and architecture work: ERP-to-ERP data flows, industrial IoT into asset management, and the operational mess that shows up when agentic AI is asked to do more than generate a suggestion. It leads with SAP because that's the deepest expertise behind it, and it doesn't stop at SAP, because most of the hard integration problems in a large enterprise happen at the boundary between SAP and everything else.

## Where to start

- **New to this repository?** Start with [Reference architectures](architectures/index.md) — each one follows the same structure: the actual problem, the architecture with a diagram, the design decisions that matter, and when the pattern does and doesn't fit.
- **Working in oil & gas specifically?** Start with [SAP's oil & gas solution landscape](decision-guides/sap-oil-gas-solution-landscape.md) — a terminology map from legacy IS-Oil to current S/4HANA naming, with links into the architectures that use each capability.
- **Designing an agent that acts inside an ERP system?** Go straight to [Guardrails for agentic AI in ERP](decision-guides/agentic-ai-guardrails-for-erp.md).
- **Want to build against something concrete?** The [companion dataset](dataset.md) is a synthetic, CC0 SAP/ERP dataset built specifically so you can prototype against realistic data without touching anything real.

## How this is organized

| Section | What's in it |
|---|---|
| [Reference architectures](architectures/index.md) | Full architecture writeups — problem, diagram, decisions, when to use and when not to |
| [Decision guides](decision-guides/sap-oil-gas-solution-landscape.md) | Cross-cutting guidance for choosing between patterns, not tied to one architecture |
| [Architecture Decision Records](decisions/index.md) | Short, standing positions this repository takes across every architecture — what was decided and why |
| [Pattern catalog](patterns/integration-patterns-catalog.md) | A reference table of SAP integration patterns and common error codes |
| [Dataset](dataset.md) | The synthetic SAP ERP dataset backing several of the architectures above |

Every document cites its sources where it draws on external material, and says plainly where something is a design opinion versus a documented fact. Diagrams are Mermaid, rendered live on this page — no exported images to keep in sync by hand.

Source, license, and contribution guidelines live in the [GitHub repository](https://github.com/pusinghal-arch/integration-foundry).
