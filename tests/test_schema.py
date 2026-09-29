
import pandas as pd
from datagate.checks import check_schema


def test_orders_schema():
    df = pd.DataFrame({
        "order_id": ["order_1"],
        "customer_id": ["customer_1"],
        "order_status": ["delivered"]
    })

    result = check_schema(
        df,
        ["order_id", "customer_id", "order_status"]
    )

    assert result["passed"] is True


def test_items_schema():
    df = pd.DataFrame({
        "order_id": ["order_1"],
        "order_item_id": [1],
        "price": [100.0]
    })

    result = check_schema(
        df,
        ["order_id", "order_item_id", "price"]
    )

    assert result["passed"] is True