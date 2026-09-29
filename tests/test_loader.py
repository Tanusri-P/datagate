from datagate.loader import load_data

def test_load_data():
    data = load_data()

    assert "orders" in data
    assert "items" in data
    assert "payments" in data

    assert not data["orders"].empty
    assert not data["items"].empty
    assert not data["payments"].empty