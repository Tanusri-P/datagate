from pathlib import Path
import pandas as pd

raw = Path("raw")

files = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_order_payments_dataset.csv",
]

for filename in files:
    path = raw / filename

    print(f"\n{'=' * 50}")
    print(filename)
    print("=" * 50)

    if not path.exists():
        print("File not found!")
        continue

    df = pd.read_csv(path)

    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())
    print("\nFirst 3 rows:")
    print(df.head(3).to_string(index=False))
    print("\nMissing values:")
    print(df.isnull().sum().to_string())