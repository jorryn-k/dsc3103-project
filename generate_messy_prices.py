import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)
base_date = datetime(2020, 1, 1)
markets = ["Mukono", "Bwaise", "Nakasero", "Kansanga", None]
commodities = ["Maize", "MAIZE", "Beans", "BEANS"]

rows = []

for i in range(1000):
    row = {
        "id": i if random.random() > 0.02 else i - 1,
        "date": (base_date + timedelta(days=random.randint(0, 500))).strftime("%Y-%m-%d")
                if random.random() > 0.03 else "2020-14-50",
        "market": random.choice(markets),
        "commodities": random.choice(commodities),
        "price": random.randint(500, 5000) if random.random() > 0.05 else -2000
    }
    rows.append(row)

rows += rows[20:30]

Path("data/raw").mkdir(parents=True, exist_ok=True)

with open("data/raw/prices.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["id", "date", "market", "commodities", "price"])
    writer.writeheader()
    writer.writerows(rows)

print("Messy file created successfully!")
print(f"Total rows: {len(rows)}")
