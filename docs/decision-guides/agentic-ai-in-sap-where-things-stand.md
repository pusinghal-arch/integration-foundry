# Agentic AI in SAP landscapes: what's actually shipped versus announced

SAP's own marketing routinely blurs the line between what's live today and what's targeted for a future quarter — a Sapphire keynote and a GA release note don't read very differently if you're not looking for the distinction. This page exists to separate the two, because designing an architecture around a capability that's still a roadmap item is a common and avoidable mistake. Current as of when this page was last checked against SAP's public materials — verify against current SAP announcements before treating any date below as still accurate.

## What's actually shipped

- **Joule** — SAP's chat-based AI assistant, generally available.
- **Joule Agents in finance and service** — cash collection agents in finance, Q&A/knowledge-creation/case-classification agents in service, GA from early 2025.
- **SAP AI Agent Hub** — SAP states this is generally available, "with additional capabilities rolling out through 2026." It's positioned as the governance layer for agentic AI across SAP: a lifecycle model (Proposed → Evaluated → Approved → Active → Retired), risk ratings, compliance mapping, identity/access-control integration, and runtime enforcement limiting production workflows to verified components.
- **Agent Builder in Joule Studio** — SAP describes this as generally available, supporting connections to external agent/tool servers via MCP (Model Context Protocol).

## What's announced but not yet generally available

- **Joule Agent-to-Agent (A2A) coordination** — targeted for Q4 of the year it was announced.
- **SAP Domain Models** — targeted Q3.
- **Joule Work**, a desktop application — targeted second half of the year.
- Broader **"agentic orchestration"** — Joule autonomously planning and executing multi-step workflows — described directionally in SAP's materials without a specific, scoped GA commitment. Treat any claim of full autonomous orchestration as aspirational until a specific feature and date is attached to it.
- Industry-specific extensions for asset-intensive sectors (gate-pass and time-capture features aimed at oil, gas, mining, utilities) — announced with a target date, not yet confirmed shipped as of this writing.

The practical rule: if SAP's material describes a capability with a specific past GA date, treat it as real and design against it. If it's described in future tense, with a target quarter, or with language like "will enable" — treat it as a roadmap input to your planning, not something to architect a production dependency on yet.

## SAP's own position on governance — and it's more aligned with this repository's guardrails than you might expect

SAP frames the shift explicitly as **"human-in-the-loop" moving toward "human-on-the-loop"** — employees supervising and orchestrating rather than executing every step, not employees removed from the loop entirely. Their own language ties agent governance to "approval flows, compliance processes, identity management, and the ability to audit decision-making," and explicitly to external frameworks: EU AI Act risk classification and transparency requirements, GDPR/PDPA data handling, ISO 42001, NIST AI RMF. The AI Agent Hub's lifecycle model — an agent has to be proposed, evaluated, and approved before it's active, and can be retired — is functionally the same idea as the policy-gate discipline in [guardrails for agentic AI in ERP](agentic-ai-guardrails-for-erp.md): an agent doesn't get to act just because it exists and someone built it.

**The gap is adoption, not intent, and SAP's own data says so.** A 2026 SAP-commissioned survey found only 12% of respondents felt able to govern AI effectively, 38% had no human-in-the-loop process for agent oversight at all, and only 63% had access controls in place for agents. Read that as confirmation that the governance tooling SAP is building is running ahead of what most customers have actually implemented — which is exactly the gap the [guardrails checklist](agentic-ai-guardrails-for-erp.md) in this repository is meant to help close, independent of which specific SAP product delivers the enforcement.

## One concrete example worth knowing

A practitioner blog post from SAP Community ("SAP Joule Agent and SAP Asset Performance Management: Turning Asset Alerts into Conversations") describes wiring a Joule Agent to APM so maintenance teams can query technical-object alerts and S/4HANA maintenance notifications conversationally instead of navigating alert screens directly. It's the most concrete asset-heavy-industry example available in public SAP Community content, and it's a reasonable model for where conversational agent access to EAM data is heading — a lower-risk, read/query-oriented use of agentic AI, well short of autonomous action, which is exactly the kind of blast-radius-appropriate starting point the [root-cause copilot](../architectures/02-agentic-root-cause-copilot-for-interfaces.md) and [guardrails checklist](agentic-ai-guardrails-for-erp.md) in this repository argue for.

## Related

- [Guardrails for agentic AI in ERP: a policy-gate checklist](agentic-ai-guardrails-for-erp.md)
- [Trust-aware agentic control for SAP finance posting](../architectures/01-trust-aware-agentic-finance-posting.md)

## Sources

- [Joule Agents: How SAP Uniquely Delivers AI Agents That Truly Mean Business — SAP News](https://news.sap.com/2025/02/joule-sap-uniquely-delivers-ai-agents/)
- [The Future of the Enterprise Is Autonomous — SAP Sapphire](https://news.sap.com/2026/05/future-enterprise-autonomous/)
- [SAP recasts Joule as the front door to autonomous enterprise AI — SiliconANGLE](https://siliconangle.com/2026/05/12/sap-recasts-joule-front-door-autonomous-enterprise-ai/)
- [SAP AI Agent Hub: Observe and Govern Enterprise AI — SAP Community](https://community.sap.com/t5/technology-blog-posts-by-sap/sap-agent-hub-observe-and-govern-enterprise-ai/ba-p/14423572)
- [SAP AI Agent Hub | AI Governance and Agent Management System — SAP](https://www.sap.com/products/artificial-intelligence/ai-agent-hub.html)
- [SAP Study: AI pays off, but governance lags behind — CIO.com](https://www.cio.com/article/4197428/sap-study-ai-pays-off-but-governance-is-lagging-behind.html)
- [SAP Joule Agent and SAP Asset Performance Management (APM) — SAP Community](https://community.sap.com/t5/technology-blog-posts-by-members/sap-joule-agent-and-sap-asset-performance-management-apm-turning-asset/ba-p/14479185)
- [SAP Sapphire 2026: The Autonomous Enterprise and AI Agent Guardrails — SAPinsider](https://sapinsider.org/blogs/sap-sapphire-2026-autonomous-enterprise-ai-agents/)
