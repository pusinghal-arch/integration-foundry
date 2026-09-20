# SAP ERP integration dataset

A synthetic, multi-table, referentially-linked dataset modeling a typical SAP-centric enterprise integration landscape: master data, order-to-cash transactions, financial postings, IDoc/BAPI/RFC/OData error patterns, and interface-level monitoring telemetry.

**All data is synthetically generated.** No real company, customer, vendor, transaction, or system data is included. Field names follow standard, publicly documented SAP Data Dictionary conventions (`KUNNR`, `MATNR`, `VBELN`, `BUKRS`, and so on) purely for domain realism — this is not extracted from, or a redistribution of, any SAP software or dataset.

## Why it exists

Public datasets for classic ERP/middleware integration work — IDoc processing, BAPI/RFC failures, OData error codes, interface monitoring — are almost nonexistent, because production SAP data is confidential. This dataset fills that gap with a structurally realistic, freely reusable substitute, built specifically so the [agentic root-cause copilot](architectures/02-agentic-root-cause-copilot-for-interfaces.md) architecture on this site could be prototyped without touching anything real.

## What's in it

| Table | Rows | Models |
|---|---|---|
| `customers.csv` | 200 | Customer master (KNA1-style) |
| `vendors.csv` | 100 | Vendor master (LFA1-style) |
| `materials.csv` | 300 | Material master (MARA/MAKT-style) |
| `sales_orders_header.csv` | 1,500 | Sales order headers (VBAK-style) |
| `sales_orders_items.csv` | 3,734 | Sales order line items (VBAP-style) |
| `billing_documents.csv` | 1,399 | Billing documents, linked to orders (VBRK-style) |
| `gl_entries.csv` | 2,694 | GL journal lines, linked to billing (BKPF/BSEG-style) |
| `idoc_error_log.csv` | 800 | Individual IDoc processing events |
| `integration_error_catalog.csv` | 27 | Curated IDoc/BAPI/RFC/OData/EDI/CPI error knowledge base |
| `integration_patterns_catalog.csv` | 10 | Common SAP integration pattern reference — see the [pattern catalog](patterns/integration-patterns-catalog.md) for the annotated version |
| `middleware_monitoring_logs.csv` | 5,000 | Interface-level latency/status time series |

Every foreign key resolves — there are no orphaned rows. Full data dictionary, entity-relationship diagram, and generation scripts are in the repository.

## Suggested uses

- Root-cause classification: predict error category or resolution steps from the free-text `STATUS_DESC`/`ROOT_CAUSE` fields
- Anomaly detection on interface health: the monitoring logs include injected latency spikes and failure clusters
- Order-to-cash analytics: revenue trends, order-to-bill cycle time, credit memo rate by customer/industry
- Data lineage and reconciliation exercises: trace a sales order through billing to its GL postings
- A sandbox for practicing SAP-adjacent SQL, ETL, or integration-monitoring dashboards without any confidentiality concerns

## License

Released under **CC0 1.0 (Public Domain)** — free to use, modify, and redistribute with no attribution required.

## Get it

Full README, data dictionary, and generation scripts: [`datasets/sap-erp-integration-dataset/`](https://github.com/pusinghal-arch/integration-foundry/tree/main/datasets/sap-erp-integration-dataset) on GitHub.
