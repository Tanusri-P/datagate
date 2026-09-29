
import pandas as pd
from datagate import loader


def test_load_data(tmp_path, monkeypatch):
    raw_dir = tmp_path / "raw"
    raw_dir.mkdir()

    pd.DataFrame({
        "order_id": ["order_1"],
        "customer_id": ["customer_1"]
    }).to_csv(raw_dir / "olist_orders_dataset.csv", index=False)

    pd.DataFrame({
        "order_id": ["order_1"],
        "price": [100.0]
    }).to_csv(raw_dir / "olist_order_items_dataset.csv", index=False)

    pd.DataFrame({
        "order_id": ["order_1"],
        "payment_value": [100.0]
    }).to_csv(raw_dir / "olist_order_payments_dataset.csv", index=False)

    monkeypatch.setattr(loader, "RAW_DIR", raw_dir)

    data = loader.load_data()

    assert set(data.keys()) == {"orders", "items", "payments"}
    assert not data["orders"].empty
    assert not data["items"].empty
    assert not data["payments"].empty