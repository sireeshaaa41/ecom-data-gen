import sqlite3
import pandas as pd
from pathlib import Path

conn = sqlite3.connect("ecom.db")
data_path = Path("output")

for file in ["customers", "products", "orders", "order_items", "reviews"]:
    df = pd.read_csv(data_path / f"{file}.csv")
    df.to_sql(file, conn, if_exists="replace", index=False)

conn.close()
print("✅ Data successfully loaded into ecom.db")
