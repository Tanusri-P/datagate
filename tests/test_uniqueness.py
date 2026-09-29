import pandas as pd
from datagate.checks import check_uniqueness

def test_unique_values():
    df = pd.DataFrame({"order_id": [1, 2, 3]})
    result = check_uniqueness(df, "order_id")
    assert result["passed"] is True

def test_duplicate_values():
    df = pd.DataFrame({"order_id": [1, 2, 2, 3]})
    result = check_uniqueness(df, "order_id")
    assert result["passed"] is False
    assert result["duplicates"] == 1