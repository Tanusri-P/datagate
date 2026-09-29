from datagate.loader import load_data
from datagate.checks import check_schema

def test_orders_schema():
    data = load_data()
    result = check_schema(
        data["orders"],
        ["order_id", "customer_id", "order_status"]
    )
    assert result["passed"] is True

def test_items_schema():
    data = load_data()
    result = check_schema(
        data["items"],
        ["order_id", "order_item_id", "price"]
    )
    assert result["passed"] is True