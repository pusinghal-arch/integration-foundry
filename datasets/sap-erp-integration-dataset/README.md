# Synthetic SAP / ERP Enterprise Integration Dataset

A multi-table, referentially-linked synthetic dataset modeling a typical **SAP-centric enterprise
integration landscape**: master data, order-to-cash transactions, financial postings, IDoc/BAPI/RFC/OData
error patterns, and interface-level monitoring telemetry.

**⚠️ All data in this package is synthetically generated.** No real company, customer, vendor,
transaction, or system data is included. Field names follow standard, publicly documented SAP
Data Dictionary conventions (e.g. `KUNNR`, `MATNR`, `VBELN`, `BUKRS`) purely for domain realism —
this is not extracted from, or a redistribution of, any SAP software or dataset.

## Why this dataset exists

Public datasets for classic ERP/middleware integration work (IDoc processing, BAPI/RFC failures,
OData error codes, interface monitoring) are almost nonexistent, because production SAP data is
confidential. This package fills that gap with a structurally realistic, freely reusable substitute
so people can practice, teach, benchmark, or publish research on:

- Root-cause classification of integration failures (structured + text fields)
- Interface health / anomaly detection on time-series monitoring data
- Order-to-cash analytics (order → billing → GL posting lineage)
- Building or demoing SAP-adjacent data pipelines, dashboards, or ML models without confidentiality risk

## Directory structure

```
data/
├── customers.csv                     # 200 rows  — customer master (KNA1-style)
├── vendors.csv                       # 100 rows  — vendor master (LFA1-style)
├── materials.csv                     # 300 rows  — material master (MARA/MAKT-style)
├── sales_orders_header.csv           # 1,500 rows — sales order headers (VBAK-style)
├── sales_orders_items.csv            # 3,734 rows — sales order line items (VBAP-style)
├── billing_documents.csv             # 1,399 rows — billing docs, linked to orders (VBRK-style)
├── gl_entries.csv                    # 2,694 rows — GL journal lines, linked to billing (BKPF/BSEG-style)
├── idoc_error_log.csv                # 800 rows   — individual IDoc processing events
├── integration_error_catalog.csv     # 27 rows    — curated IDoc/BAPI/RFC/OData/EDI/CPI error KB
├── integration_patterns_catalog.csv  # 10 rows    — common SAP integration pattern reference
└── middleware_monitoring_logs.csv    # 5,000 rows — interface-level latency/status time series
README.md
dataset-metadata.json                 # Kaggle CLI upload metadata (edit the "id" field first)
```

## Entity relationships

```
customers (KUNNR) ──┐
                     ├──< sales_orders_header (KUNNR) ──< sales_orders_items (VBELN → MATNR)
materials (MATNR) ───┘                │
                                       └──< billing_documents (REF_SO → VBELN)
                                                    │
                                                    └──< gl_entries (REF_BILLING → VBELN)

integration_error_catalog (ERROR_CODE, INTEGRATION_TYPE)
        ▲
        └── sampled by ── idoc_error_log (STATUS_CODE)

integration_patterns_catalog  (standalone reference table, not row-linked)
middleware_monitoring_logs    (standalone interface time series, INTERFACE_ID is a free-standing key)
```

`sales_orders_items.MATNR` → `materials.MATNR`, `sales_orders_header.KUNNR` → `customers.KUNNR`,
`billing_documents.REF_SO` → `sales_orders_header.VBELN`, `gl_entries.REF_BILLING` →
`billing_documents.VBELN`. Every foreign key resolves — there are no orphaned rows.

## Data dictionary

### customers.csv
| Column | Type | Description |
|---|---|---|
| KUNNR | string(10) | Customer number, zero-padded |
| NAME1 | string | Customer name |
| LAND1 | string(2) | ISO-ish country code |
| ORT01 | string | City |
| PSTLZ | string | Postal code |
| REGIO | string | Region/state (US only) |
| KTOKD | string | Account group: Z001 domestic, Z002 export, Z003 intercompany |
| INDUSTRY | string | Industry sector |
| ERDAT | date | Record creation date |

### vendors.csv
| Column | Type | Description |
|---|---|---|
| LIFNR | string(10) | Vendor number |
| NAME1 | string | Vendor name |
| LAND1 | string(2) | Country code |
| ORT01 | string | City |
| PSTLZ | string | Postal code |
| KTOKK | string | Account group: Y001 raw material supplier, Y002 services |
| INDUSTRY | string | Industry sector |
| ERDAT | date | Record creation date |

### materials.csv
| Column | Type | Description |
|---|---|---|
| MATNR | string(10) | Material number |
| MAKTX | string | Material description |
| MTART | string | Material type: FERT finished good, ROH raw material, HAWA trading good, DIEN service |
| MATKL | string | Material group |
| MEINS | string | Base unit of measure |
| NETPR | float | Standard price |
| WAERS | string | Currency |
| WERKS | string(4) | Plant |
| BRGEW_KG | float | Gross weight (kg) |

### sales_orders_header.csv
| Column | Type | Description |
|---|---|---|
| VBELN | string(10) | Sales order number |
| ERDAT | date | Order creation date |
| AUART | string | Order type: OR standard, RE returns, CS cash sale, ZOR rush order |
| VKORG | string(4) | Sales organization |
| VTWEG | string(2) | Distribution channel |
| SPART | string(2) | Division |
| KUNNR | string(10) | Sold-to customer → `customers.KUNNR` |
| NETWR | float | Order net value (sum of items) |
| WAERK | string | Currency |
| STATUS | string | Open / In Process / Billed / Cancelled |

### sales_orders_items.csv
| Column | Type | Description |
|---|---|---|
| VBELN | string(10) | Sales order number → `sales_orders_header.VBELN` |
| POSNR | int | Item number (10, 20, 30…) |
| MATNR | string(10) | Material → `materials.MATNR` |
| WERKS | string(4) | Delivering plant |
| KWMENG | int | Order quantity |
| NETPR | float | Net price per unit |
| NETWR | float | Item net value (KWMENG × NETPR) |

### billing_documents.csv
| Column | Type | Description |
|---|---|---|
| VBELN | string(10) | Billing document number |
| FKART | string | Billing type: F2 invoice, G2 credit memo, S1 cancellation |
| FKDAT | date | Billing date |
| REF_SO | string(10) | Reference sales order → `sales_orders_header.VBELN` |
| KUNNR | string(10) | Customer → `customers.KUNNR` |
| NETWR | float | Net value (negative for credit memos) |
| WAERK | string | Currency |
| STATUS | string | Posted / Cancelled |

### gl_entries.csv
| Column | Type | Description |
|---|---|---|
| BELNR | string(10) | Accounting document number |
| BUKRS | string(4) | Company code |
| GJAHR | int | Fiscal year |
| BUDAT | date | Posting date |
| BUZEI | string(3) | Line item number |
| HKONT | string(10) | GL account (AR: 0140000000, Revenue: 0800000000, Returns: 0801000000) |
| SHKZG | string(1) | Debit/credit indicator: S debit, H credit |
| DMBTR | float | Amount in local currency |
| REF_BILLING | string(10) | Reference billing document → `billing_documents.VBELN` |

### idoc_error_log.csv
| Column | Type | Description |
|---|---|---|
| IDOC_NUMBER | string(10) | IDoc number |
| MESTYP | string | Message type: ORDERS, ORDRSP, DESADV, INVOIC, MATMAS, DEBMAS, CREMAS, WMMBXY |
| DIRECTION | string | INBOUND / OUTBOUND |
| PARTNER_SYSTEM | string | Sending/receiving partner system |
| STATUS_CODE | string | IDoc status code (matches `integration_error_catalog.ERROR_CODE` when an error) |
| STATUS_DESC | string | Status description |
| ROOT_CAUSE | string | Likely root cause (blank for healthy IDocs) |
| RESOLUTION | string | Resolution steps (blank for healthy IDocs) |
| TIMESTAMP | datetime | Event timestamp |
| RESOLVED_FLAG | bool | Whether the error was resolved |

### integration_error_catalog.csv
| Column | Type | Description |
|---|---|---|
| ERROR_ID | string | Surrogate key |
| INTEGRATION_TYPE | string | IDoc / BAPI / RFC / OData / EDI / CPI |
| ERROR_CODE | string | Native error/status code |
| SHORT_DESCRIPTION | string | Human-readable summary |
| LIKELY_CAUSE | string | Common root cause |
| RESOLUTION_STEPS | string | Recommended remediation |
| SEVERITY | string | Low / Medium / High / Critical |
| TYPICAL_SYSTEM | string | Where this typically occurs |

### integration_patterns_catalog.csv
| Column | Type | Description |
|---|---|---|
| PATTERN_ID | string | Surrogate key |
| PATTERN_NAME | string | Integration pattern name |
| TECHNOLOGY | string | Underlying technology |
| SYNC_ASYNC | string | Sync / Async / Mixed |
| TYPICAL_USE_CASE | string | Business scenario |
| MIDDLEWARE_EXAMPLES | string | Common tooling |
| COMMON_CHALLENGES | string | Known pain points |

### middleware_monitoring_logs.csv
| Column | Type | Description |
|---|---|---|
| LOG_ID | string | Surrogate key |
| TIMESTAMP | datetime | Log timestamp (last 30 days) |
| INTERFACE_ID | string | Interface identifier (IF-001 … IF-008) |
| SOURCE_SYSTEM | string | Sending system |
| TARGET_SYSTEM | string | Receiving system |
| MESSAGE_TYPE | string | Message/interface type |
| STATUS | string | SUCCESS / FAILED / RETRY / TIMEOUT |
| LATENCY_MS | float | Round-trip latency in milliseconds |
| PAYLOAD_SIZE_KB | float | Payload size |
| RETRY_COUNT | int | Number of retries for this message |

## Suggested use cases

- **Root-cause classification**: predict `ERROR_CATEGORY`/`SEVERITY` or the correct `RESOLUTION_STEPS`
  from free-text `STATUS_DESC`/`ROOT_CAUSE` (NLP / text classification, or a RAG demo over the KB).
- **Anomaly detection on interface health**: flag latency spikes or failure clusters in
  `middleware_monitoring_logs.csv` (the data includes injected spike periods).
- **Order-to-cash analytics**: revenue trends, order-to-bill cycle time, credit memo rate by customer/industry.
- **Data lineage / reconciliation exercises**: trace a sales order through billing to its GL postings.
- **Interview / teaching material**: a realistic sandbox for practicing SAP-adjacent SQL, ETL, or
  integration-monitoring dashboard building without any confidentiality concerns.

## License & attribution

This package is released under **CC0 1.0 (Public Domain)** — free to use, modify, and redistribute
with no attribution required. If you publish derivative work, a link back is appreciated but not required.
SAP, IDoc, BAPI, and related terms are used descriptively to refer to the technologies being modeled and
are trademarks of SAP SE; this dataset is an independent, unaffiliated synthetic work.

## Publishing to Kaggle

1. Install the CLI: `pip install kaggle`
2. Place your Kaggle API token at `~/.kaggle/kaggle.json`
3. Edit `dataset-metadata.json` — replace `"your-kaggle-username"` in the `id` field with your actual username
4. From this folder, run:
   ```bash
   kaggle datasets create -p data --dir-mode zip
   ```
   (or `kaggle datasets version -p data -m "update"` for subsequent updates)

## Regenerating / extending

The `gen_0*.py` scripts (included alongside this README) regenerate every table from scratch with a
fixed random seed. Adjust row counts, categorical distributions, or add new tables (e.g. a returns/RMA
flow, or a second company code) by editing those scripts directly.
