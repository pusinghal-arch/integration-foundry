"""
Generates event-level / time-series synthetic data:
  - idoc_error_log.csv          : individual IDoc processing events sampled against the error catalog
  - middleware_monitoring_logs.csv : interface-level time series (latency, status, payload size)
"""
import pandas as pd
import numpy as np
from faker import Faker
from datetime import timedelta

np.random.seed(44)
fake = Faker()
Faker.seed(44)

OUT = "data"
error_catalog = pd.read_csv(f"{OUT}/integration_error_catalog.csv")
idoc_errors = error_catalog[error_catalog["INTEGRATION_TYPE"] == "IDoc"].reset_index(drop=True)

MESTYP_CHOICES = ["ORDERS", "ORDRSP", "DESADV", "INVOIC", "MATMAS", "DEBMAS", "CREMAS", "WMMBXY"]
PARTNER_SYSTEMS = ["EDI_GATEWAY", "CRM_SFDC", "WMS_MANHATTAN", "3PL_PROVIDER", "B2B_VAN_SPS",
                   "LEGACY_MAINFRAME", "ARIBA_NETWORK", "BTP_INTEGRATION_SUITE"]

N_IDOC_EVENTS = 800
rows = []
start = pd.Timestamp("today") - timedelta(days=180)

for i in range(N_IDOC_EVENTS):
    idoc_number = f"{600000000 + i:010d}"
    ts = start + timedelta(
        days=int(np.random.randint(0, 180)),
        hours=int(np.random.randint(0, 24)),
        minutes=int(np.random.randint(0, 60)),
    )
    is_error = np.random.random() < 0.35  # 35% of logged events are true errors; rest are healthy/status-64 style
    if is_error:
        err = idoc_errors.sample(1).iloc[0]
        status_code = err["ERROR_CODE"]
        status_desc = err["SHORT_DESCRIPTION"]
        category = err["ERROR_CODE"]
        root_cause = err["LIKELY_CAUSE"]
        resolution = err["RESOLUTION_STEPS"]
        resolved = np.random.choice([True, False], p=[0.75, 0.25])
    else:
        status_code = "53"
        status_desc = "Application document posted"
        root_cause = ""
        resolution = ""
        resolved = True

    rows.append({
        "IDOC_NUMBER": idoc_number,
        "MESTYP": np.random.choice(MESTYP_CHOICES),
        "DIRECTION": np.random.choice(["INBOUND", "OUTBOUND"]),
        "PARTNER_SYSTEM": np.random.choice(PARTNER_SYSTEMS),
        "STATUS_CODE": status_code,
        "STATUS_DESC": status_desc,
        "ROOT_CAUSE": root_cause,
        "RESOLUTION": resolution,
        "TIMESTAMP": ts.isoformat(sep=" "),
        "RESOLVED_FLAG": resolved,
    })

idoc_error_log = pd.DataFrame(rows).sort_values("TIMESTAMP").reset_index(drop=True)
idoc_error_log.to_csv(f"{OUT}/idoc_error_log.csv", index=False)

# ---------------------------------------------------------------- middleware monitoring logs (time series)
INTERFACES = [
    ("IF-001", "SAP_ECC", "SFDC_CRM", "ORDERS"),
    ("IF-002", "SAP_S4HANA", "WMS_MANHATTAN", "DESADV"),
    ("IF-003", "SAP_S4HANA", "ARIBA_NETWORK", "ORDRSP"),
    ("IF-004", "SAP_ECC", "B2B_VAN_SPS", "INVOIC"),
    ("IF-005", "SAP_S4HANA", "BTP_APP", "OData"),
    ("IF-006", "LEGACY_MAINFRAME", "SAP_ECC", "MATMAS"),
    ("IF-007", "SAP_S4HANA", "DATA_LAKE", "CDC"),
    ("IF-008", "SAP_CPI", "3PL_PROVIDER", "DESADV"),
]

N_LOG_ROWS = 5000
mon_rows = []
start = pd.Timestamp("today") - timedelta(days=30)

for i in range(N_LOG_ROWS):
    iface_id, src, tgt, mtype = INTERFACES[np.random.randint(0, len(INTERFACES))]
    ts = start + timedelta(
        days=int(np.random.randint(0, 30)),
        hours=int(np.random.randint(0, 24)),
        minutes=int(np.random.randint(0, 60)),
        seconds=int(np.random.randint(0, 60)),
    )
    # inject a mild "business hours are busier / occasional latency spike" pattern
    base_latency = np.random.lognormal(mean=4.2, sigma=0.6)
    is_spike = np.random.random() < 0.04
    latency = base_latency * (6 if is_spike else 1)
    status = np.random.choice(
        ["SUCCESS", "FAILED", "RETRY", "TIMEOUT"],
        p=[0.90, 0.05, 0.035, 0.015] if not is_spike else [0.35, 0.30, 0.20, 0.15]
    )
    mon_rows.append({
        "LOG_ID": f"LOG-{i+1:07d}",
        "TIMESTAMP": ts.isoformat(sep=" "),
        "INTERFACE_ID": iface_id,
        "SOURCE_SYSTEM": src,
        "TARGET_SYSTEM": tgt,
        "MESSAGE_TYPE": mtype,
        "STATUS": status,
        "LATENCY_MS": round(latency, 1),
        "PAYLOAD_SIZE_KB": round(np.random.lognormal(mean=2.0, sigma=1.0), 2),
        "RETRY_COUNT": 0 if status == "SUCCESS" else int(np.random.randint(0, 4)),
    })

middleware_monitoring_logs = pd.DataFrame(mon_rows).sort_values("TIMESTAMP").reset_index(drop=True)
middleware_monitoring_logs.to_csv(f"{OUT}/middleware_monitoring_logs.csv", index=False)

print("idoc_error_log:", idoc_error_log.shape)
print("middleware_monitoring_logs:", middleware_monitoring_logs.shape)
