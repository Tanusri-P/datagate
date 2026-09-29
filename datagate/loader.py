from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = ROOT / "raw"

def load_data():
    orders = pd.read_csv(RAW_DIR / "olist_orders_dataset.csv")
    items = pd.read_csv(RAW_DIR / "olist_order_items_dataset.csv")
    payments = pd.read_csv(RAW_DIR / "olist_order_payments_dataset.csv")

    return {
        "orders": orders,
        "items": items,
        "payments": payments,
    }