import pandas as pd
import json
import random
import string
from pathlib import Path

# Base output path
base = Path.home() / "airflow-docker/data/landing"
date = "20250101"

# Make dirs if missing
(base / "customers").mkdir(parents=True, exist_ok=True)
(base / "products").mkdir(parents=True, exist_ok=True)
(base / "orders").mkdir(parents=True, exist_ok=True)

#generate 500 Customers 
customers = []
countries = ["USA", "Canada", "India", "UK", "Germany"]

for i in range(500):
    cid = 1000 + i
    first = ''.join(random.choices(string.ascii_letters, k=6)).capitalize()
    last = ''.join(random.choices(string.ascii_letters, k=7)).capitalize()
    email = f"{first.lower()}.{last.lower()}@example.com"
    signup = f"202{random.randint(0,4)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
    country = random.choice(countries)
    customers.append([cid, first, last, email, signup, country])

df_customers = pd.DataFrame(customers, columns=[
    "customer_id", "first_name", "last_name", "email", "signup_date", "country"
])
df_customers.to_csv(base / "customers" / f"customers_{date}.csv", index=False)

# generate 500 products
products = []
categories = ["Electronics", "Home", "Accessories", "Fitness", "Toys"]

for i in range(500):
    pid = 500 + i
    name = f"Product_{pid}"
    cat = random.choice(categories)
    price = round(random.uniform(5, 500), 2)
    products.append([pid, name, cat, price])

df_products = pd.DataFrame(products, columns=[
    "product_id", "product_name", "category", "unit_price"
])
df_products.to_csv(base / "products" / f"products_{date}.csv", index=False)

#generate 500 Orders
orders = []

for i in range(500):
    oid = 9000 + i
    timestamp = f"2025-01-01T{random.randint(0,23):02d}:{random.randint(0,59):02d}:00"
    cust = random.choice(df_customers["customer_id"].tolist())
    prod = random.choice(df_products["product_id"].tolist())
    qty = random.randint(1, 5)
    price = df_products.loc[df_products["product_id"] == prod, "unit_price"].iloc[0]
    total = round(qty * price, 2)
    currency = "USD"
    status = random.choice(["completed", "completed", "completed", "cancelled"])

    orders.append({
        "order_id": oid,
        "order_timestamp": timestamp,
        "customer_id": cust,
        "product_id": prod,
        "quantity": qty,
        "total_amount": total,
        "currency": currency,
        "status": status
    })

with open(base / "orders" / f"orders_{date}.json", "w") as f:
    json.dump(orders, f, indent=2)

print("Datasets generated successfully!")
print(base)
