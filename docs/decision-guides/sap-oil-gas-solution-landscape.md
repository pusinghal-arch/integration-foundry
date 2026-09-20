# SAP's oil & gas solution landscape: a map for architects

SAP's oil & gas capability has been renamed, re-bundled, and re-platformed enough times across the ECC-to-S/4HANA transition that even experienced SAP architects sometimes reach for the wrong module name in a design conversation. This page exists to fix vocabulary before it costs you a week of miscommunication with a systems integrator quoting the wrong scope. It also maps which capability integrates with which of the reference architectures in this repository.

**A note on sourcing:** the terminology below is drawn from SAP's own Help Portal and SAP Community, current as of when this page was written. SAP Help Portal pages are JavaScript-rendered and not always fully indexable, so treat specific field-level or configuration claims as a starting point for your own verification against a live system, not a substitute for it. Sources are linked at the bottom of each section.

## Upstream

| Legacy (IS-Oil / ECC) | Current (S/4HANA) | What it does |
|---|---|---|
| IS-Oil Upstream | **Upstream Operations Management** | Well lifecycle, production operations; available on both public and private cloud |
| PRA (IS-Oil) | **Production and Revenue Accounting (PRA)** | Volume allocation, ownership, contracts/pricing, revenue accounting, tax/royalty reporting — five distinct functional areas under one component |
| — | **Energy Integration Architecture** | SAP's own name for the integration layer connecting third-party ownership and field-data-capture systems to PRA — worth knowing as a literal term if you're scoping integration work with a systems integrator |
| JVA (IS-Oil) | **Joint Venture Accounting (JVA)** | Cutback, cash calls, partner billing, AFE tracking — integrated across FI, CO, Asset Accounting, MM, PM, PS |

Related: [Field measurement to Production and Revenue Accounting](../architectures/06-field-measurement-to-production-revenue-accounting.md), [Joint venture cutback and cross-ERP partner billing](../architectures/07-joint-venture-cutback-cross-erp-billing.md)

Sources: [Production and Revenue Accounting — SAP Help Portal](https://help.sap.com/docs/SAP_S4HANA_CLOUD/8bae74e1ba0c4c8cae3a97f15b76ad1e/9e58e0535e56424de10000000a174cb4.html), [Introduction to Joint Venture Accounting — SAP Help Portal](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/f049a59301a94f1c9bb60ca8394db217/6066d0531d8b4208e10000000a174cb4.html)

## Midstream and downstream

| Legacy (IS-Oil / ECC) | Current (S/4HANA) | What it does |
|---|---|---|
| TSW (IS-Oil) | **TSW — Trader's and Scheduler's Workbench** | Nominations, ticketing, three-way pegging between deals and transport; still the live S/4HANA on-premise component, not replaced |
| — | **SAP Commodity Management, Option for Deal Capture** | Formal deal/contract capture including Exchange Agreements (linking a purchase and a sales contract for a physical swap) |
| MCOE (IS-Oil) | **MCOE — Marketing, Contracts and Order Entry** | Sales-contract execution |
| HPM (IS-Oil) | **Liquid and Gaseous Hydrocarbon Product Management (HPM)** | Tank/silo stock, blending, ASTM/API-table volume and weight conversion — private-cloud/on-prem only, not currently offered on public cloud |
| TAS (IS-Oil) | **Terminal Automation System Interface** | Bridges terminal metering equipment (tank gauges, flow meters) into SAP, including automatic gain/loss posting when loaded and discharged quantities differ |
| Secondary distribution (IS-Oil) | **S4SCSD — S/4HANA Supply Chain for Secondary Distribution** | Wholesaler/reseller/service-station distribution processes |

Related: [Terminal measurement gain/loss reconciliation](../architectures/08-terminal-measurement-gain-loss-reconciliation.md), [Trading and scheduling orchestration](../architectures/09-trading-scheduling-orchestration-tsw-tm.md)

Sources: [TSW — Trader's and Scheduler's Workbench — SAP Help Portal](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/9609b5f9e9304ef6850945b359a1f5d4/b7a0cf535b804808e10000000a174cb4.html), [Liquid and Gaseous Hydrocarbon Product Management — SAP Help Portal](https://help.sap.com/docs/SAP_S4HANA_ON-PREMISE/0f4ab800d01c4366b0c9aaff06a64320/23c9cc5340487214e10000000a174cb4.html), [Exchange Agreements — SAP Help Portal](https://help.sap.com/docs/SAP_COMMODITY_MANAGEMENT_OPTION_FOR_DEAL_CAPTURE_FOR_SAP_S4_HANA/3b2ce84e99214101a01d1ba15f459b00/028fe5a239a642bcb8e52a6bee551e7d.html)

## Asset, safety, and environment

| Legacy (IS-Oil / ECC) | Current (S/4HANA) | What it does |
|---|---|---|
| EHS Management | **SAP S/4HANA for EHS** | Three pillars: Product Compliance, Incident Management, Health & Safety |
| — | **Environment Management** / Emission Management | GHG and air-pollutant tracking, water/wastewater, waste, feeding ESG frameworks like CSRD/ESRS |
| WCM | **Work Clearance Management (PM-WCM)** | Permit-to-work, natively part of Plant Maintenance/EAM — not a bolt-on integration, a same-system state machine (work order → permit → safety gate → de-isolation → close) |

A real gap worth knowing before you scope a project around it: SAP's own Emission Management documentation does not describe a native connector to third-party Continuous Emissions Monitoring Systems (CEMS). That integration has to be built, typically via SAP Integration Suite / BTP with a historian or data-hub intermediary — see [CEMS to SAP EHS Environment Management](../architectures/11-cems-emissions-to-sap-ehs-environment-management.md) for a reference design.

Related: [Permit-to-work safety gate integrated with Plant Maintenance](../architectures/10-permit-to-work-safety-gate-plant-maintenance.md), [Field telemetry to SAP EAM for upstream/midstream assets](../architectures/04-iot-to-sap-eam-upstream-midstream.md)

Sources: [Strategy Update: The Next Evolutionary Step of SAP S/4HANA for EHS — SAP News](https://news.sap.com/2025/07/strategy-update-sap-s4hana-ehs/), [SAP EHS Environment Management — SAP Community](https://community.sap.com/t5/sustainability-blog-posts/sap-ehs-environment-management-environmental-responsibility-and-regulatory/ba-p/14173083), [SAP Work Clearance Management (Permit to Work) — SAP Community](https://community.sap.com/t5/supply-chain-management-blog-posts-by-sap/sap-work-clearance-management-permit-to-work-making-maintenance-safer-and/ba-p/14386858)

## Field data capture — the layer SAP doesn't own

Almost every upstream and midstream architecture on this list depends on data that originates outside SAP entirely: **AVEVA PI (formerly OSIsoft PI)** is the dominant historian for upstream flow, pressure, and production data — one estimate puts it in use at roughly 85% of large upstream operators. SAP's bridge into that world is **SAP Plant Connectivity (PCo)**, which can consume the OSIsoft PI Web API, with OPC UA/DA/HDA as an alternative path for other SCADA sources. A recurring practitioner complaint: PI is built as an operational historian, not an analytics store, so its native query model doesn't support the cross-system joins production accounting actually needs — which is why many landscapes stage PI data into an intermediate warehouse before it ever reaches SAP, rather than integrating PI directly into PRA. This distinction matters when you're deciding where the "integration" actually happens.

Related: [Field measurement to Production and Revenue Accounting](../architectures/06-field-measurement-to-production-revenue-accounting.md)

Sources: [Installing the OSIsoft PI Web API — SAP Help Portal](https://help.sap.com/docs/PRODUCTION_CONNECTOR/fbfea14aa9b64588897025e49e6a9b03/ea0b688fd52b498fbc81c9403eecea75.html), [Databases and Historians for Oil & Gas — Petropt](https://petropt.com/articles/og-databases-historians-guide/)
