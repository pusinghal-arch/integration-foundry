"""
Generates synthetic SAP-style master data:
  - customers.csv   (mirrors KNA1 fields)
  - vendors.csv     (mirrors LFA1 fields)
  - materials.csv   (mirrors MARA/MAKT fields)

All data is 100% synthetic (Faker-generated), for portfolio / research / ML use only.
"""
import pandas as pd
import numpy as np
from faker import Faker
import random

random.seed(42)
np.random.seed(42)
fake = Faker()
Faker.seed(42)

OUT = "data"

COUNTRIES = ["US", "DE", "GB", "FR", "IN", "CN", "BR", "CA", "MX", "NL", "SG", "AU", "JP", "ZA", "AE"]
COUNTRY_WEIGHTS = [0.28, 0.14, 0.08, 0.07, 0.10, 0.07, 0.05, 0.05, 0.04, 0.03, 0.03, 0.02, 0.02, 0.01, 0.01]
INDUSTRIES = ["Automotive", "High Tech", "Consumer Goods", "Pharma", "Retail",
              "Industrial Manufacturing", "Chemicals", "Utilities", "Logistics", "Life Sciences"]

# ---------------------------------------------------------------- customers
N_CUST = 200
cust_rows = []
for i in range(N_CUST):
    kunnr = f"{100000 + i:010d}"
    country = np.random.choice(COUNTRIES, p=COUNTRY_WEIGHTS)
    cust_rows.append({
        "KUNNR": kunnr,
        "NAME1": fake.company(),
        "LAND1": country,
        "ORT01": fake.city(),
        "PSTLZ": fake.postcode(),
        "REGIO": fake.state_abbr() if country == "US" else "",
        "KTOKD": np.random.choice(["Z001", "Z002", "Z003"], p=[0.6, 0.25, 0.15]),  # domestic/export/intercompany
        "INDUSTRY": np.random.choice(INDUSTRIES),
        "ERDAT": fake.date_between(start_date="-6y", end_date="-30d").isoformat(),
    })
customers = pd.DataFrame(cust_rows)
customers.to_csv(f"{OUT}/customers.csv", index=False)

# ---------------------------------------------------------------- vendors
N_VEND = 100
vend_rows = []
for i in range(N_VEND):
    lifnr = f"{200000 + i:010d}"
    country = np.random.choice(COUNTRIES, p=COUNTRY_WEIGHTS)
    vend_rows.append({
        "LIFNR": lifnr,
        "NAME1": fake.company(),
        "LAND1": country,
        "ORT01": fake.city(),
        "PSTLZ": fake.postcode(),
        "KTOKK": np.random.choice(["Y001", "Y002"], p=[0.7, 0.3]),  # raw material / services
        "INDUSTRY": np.random.choice(INDUSTRIES),
        "ERDAT": fake.date_between(start_date="-6y", end_date="-30d").isoformat(),
    })
vendors = pd.DataFrame(vend_rows)
vendors.to_csv(f"{OUT}/vendors.csv", index=False)

# ---------------------------------------------------------------- materials
N_MAT = 300
MTART_CHOICES = ["FERT", "ROH", "HAWA", "DIEN"]  # finished good, raw material, trading good, service
MTART_WEIGHTS = [0.45, 0.25, 0.20, 0.10]
MATKL_CHOICES = ["ELEC-COMP", "MECH-PART", "PACKAGING", "RAW-CHEM", "FINISHED-ASSY", "SERVICES", "CONSUMABLES"]
UNIT_BY_TYPE = {"FERT": ["EA", "PC"], "ROH": ["KG", "L", "EA"], "HAWA": ["EA", "PC"], "DIEN": ["AU", "HR"]}

mat_rows = []
for i in range(N_MAT):
    matnr = f"{900000 + i:010d}"
    mtart = np.random.choice(MTART_CHOICES, p=MTART_WEIGHTS)
    base_price = round(np.random.lognormal(mean=3.2, sigma=1.1), 2)
    mat_rows.append({
        "MATNR": matnr,
        "MAKTX": fake.catch_phrase(),
        "MTART": mtart,
        "MATKL": np.random.choice(MATKL_CHOICES),
        "MEINS": np.random.choice(UNIT_BY_TYPE[mtart]),
        "NETPR": base_price,
        "WAERS": "USD",
        "WERKS": np.random.choice(["1000", "1010", "1020", "2000", "2010"]),
        "BRGEW_KG": round(np.random.uniform(0.05, 120), 2),
    })
materials = pd.DataFrame(mat_rows)
materials.to_csv(f"{OUT}/materials.csv", index=False)

print("customers:", customers.shape)
print("vendors:", vendors.shape)
print("materials:", materials.shape)
