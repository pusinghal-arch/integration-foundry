"""
Generates synthetic SAP-style transactional data, referentially linked to master data:
  - sales_orders_header.csv  (mirrors VBAK fields)
  - sales_orders_items.csv   (mirrors VBAP fields)
  - billing_documents.csv    (mirrors VBRK fields, referencing sales orders)
  - gl_entries.csv           (mirrors BKPF/BSEG fields, referencing billing docs)
"""
import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import timedelta

random.seed(43)
np.random.seed(43)
fake = Faker()
Faker.seed(43)

OUT = "data"
customers = pd.read_csv(f"{OUT}/customers.csv", dtype=str)
materials = pd.read_csv(f"{OUT}/materials.csv", dtype={"MATNR": str, "WERKS": str})
materials["NETPR"] = materials["NETPR"].astype(float)

CUST_IDS = customers["KUNNR"].tolist()
MAT_IDS = materials["MATNR"].tolist()
MAT_PRICE = dict(zip(materials["MATNR"], materials["NETPR"]))
MAT_PLANT = dict(zip(materials["MATNR"], materials["WERKS"]))

AUART_CHOICES = ["OR", "RE", "CS", "ZOR"]  # standard order, returns, cash sale, rush order
AUART_WEIGHTS = [0.78, 0.08, 0.05, 0.09]
VKORG_CHOICES = ["1000", "2000", "3000"]
VTWEG_CHOICES = ["10", "12", "20"]  # direct sale, online, distributor
SPART_CHOICES = ["00", "01", "02"]

N_ORDERS = 1500
order_rows, item_rows = [], []
order_dates = []

for i in range(N_ORDERS):
    vbeln = f"{4500000000 + i:010d}"
    order_date = fake.date_between(start_date="-2y", end_date="today")
    order_dates.append(order_date)
    kunnr = np.random.choice(CUST_IDS)
    auart = np.random.choice(AUART_CHOICES, p=AUART_WEIGHTS)

    n_items = np.random.randint(1, 5)
    chosen_mats = np.random.choice(MAT_IDS, size=n_items, replace=False)
    net_total = 0.0
    for j, matnr in enumerate(chosen_mats):
        posnr = (j + 1) * 10
        qty = np.random.randint(1, 50)
        unit_price = round(MAT_PRICE[matnr] * np.random.uniform(0.92, 1.08), 2)
        item_value = round(qty * unit_price, 2)
        net_total += item_value
        item_rows.append({
            "VBELN": vbeln,
            "POSNR": posnr,
            "MATNR": matnr,
            "WERKS": MAT_PLANT[matnr],
            "KWMENG": qty,
            "NETPR": unit_price,
            "NETWR": item_value,
        })

    # order lifecycle status, correlated with age
    days_old = (pd.Timestamp("today").normalize() - pd.Timestamp(order_date)).days
    if days_old < 3:
        status = np.random.choice(["Open", "In Process"], p=[0.7, 0.3])
    elif days_old < 10:
        status = np.random.choice(["In Process", "Billed"], p=[0.35, 0.65])
    else:
        status = np.random.choice(["Billed", "Cancelled"], p=[0.94, 0.06])

    order_rows.append({
        "VBELN": vbeln,
        "ERDAT": order_date.isoformat(),
        "AUART": auart,
        "VKORG": np.random.choice(VKORG_CHOICES),
        "VTWEG": np.random.choice(VTWEG_CHOICES),
        "SPART": np.random.choice(SPART_CHOICES),
        "KUNNR": kunnr,
        "NETWR": round(net_total, 2),
        "WAERK": "USD",
        "STATUS": status,
    })

sales_orders_header = pd.DataFrame(order_rows)
sales_orders_items = pd.DataFrame(item_rows)
sales_orders_header.to_csv(f"{OUT}/sales_orders_header.csv", index=False)
sales_orders_items.to_csv(f"{OUT}/sales_orders_items.csv", index=False)

# ---------------------------------------------------------------- billing documents
billable = sales_orders_header[sales_orders_header["STATUS"] == "Billed"].reset_index(drop=True)
FKART_CHOICES = ["F2", "G2", "S1"]  # invoice, credit memo, cancellation
FKART_WEIGHTS = [0.90, 0.07, 0.03]

bill_rows = []
for i, row in billable.iterrows():
    vbeln_bill = f"{9000000000 + i:010d}"
    order_date = pd.Timestamp(row["ERDAT"])
    bill_date = order_date + timedelta(days=int(np.random.randint(1, 8)))
    if bill_date > pd.Timestamp("today"):
        bill_date = pd.Timestamp("today")
    fkart = np.random.choice(FKART_CHOICES, p=FKART_WEIGHTS)
    netwr = row["NETWR"] if fkart != "G2" else -round(row["NETWR"] * np.random.uniform(0.05, 0.3), 2)
    bill_rows.append({
        "VBELN": vbeln_bill,
        "FKART": fkart,
        "FKDAT": bill_date.date().isoformat(),
        "REF_SO": row["VBELN"],
        "KUNNR": row["KUNNR"],
        "NETWR": round(netwr, 2),
        "WAERK": "USD",
        "STATUS": "Cancelled" if fkart == "S1" else "Posted",
    })

billing_documents = pd.DataFrame(bill_rows)
billing_documents.to_csv(f"{OUT}/billing_documents.csv", index=False)

# ---------------------------------------------------------------- GL entries (2 lines per posted billing doc)
GL_AR = "0140000000"       # Accounts Receivable
GL_REVENUE = "0800000000"  # Product Revenue
GL_REV_RETURNS = "0801000000"  # Sales Returns/Credit memos

gl_rows = []
belnr_seed = 5000000000
for i, row in billing_documents.iterrows():
    if row["STATUS"] == "Cancelled":
        continue
    belnr = f"{belnr_seed + i:010d}"
    bukrs = np.random.choice(["US10", "DE20", "IN30"], p=[0.6, 0.25, 0.15])
    gjahr = pd.Timestamp(row["FKDAT"]).year
    amount = abs(row["NETWR"])
    revenue_acct = GL_REV_RETURNS if row["FKART"] == "G2" else GL_REVENUE
    dr_shkzg, cr_shkzg = ("H", "S") if row["FKART"] == "G2" else ("S", "H")
    # Debit line
    gl_rows.append({
        "BELNR": belnr, "BUKRS": bukrs, "GJAHR": gjahr, "BUDAT": row["FKDAT"],
        "BUZEI": "001", "HKONT": GL_AR, "SHKZG": dr_shkzg, "DMBTR": amount,
        "REF_BILLING": row["VBELN"],
    })
    # Credit line
    gl_rows.append({
        "BELNR": belnr, "BUKRS": bukrs, "GJAHR": gjahr, "BUDAT": row["FKDAT"],
        "BUZEI": "002", "HKONT": revenue_acct, "SHKZG": cr_shkzg, "DMBTR": amount,
        "REF_BILLING": row["VBELN"],
    })

gl_entries = pd.DataFrame(gl_rows)
gl_entries.to_csv(f"{OUT}/gl_entries.csv", index=False)

print("sales_orders_header:", sales_orders_header.shape)
print("sales_orders_items:", sales_orders_items.shape)
print("billing_documents:", billing_documents.shape)
print("gl_entries:", gl_entries.shape)
