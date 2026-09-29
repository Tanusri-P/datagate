import pandas as pd
from datagate.checks import check_nulls

def test_no_nulls():
    df = pd.DataFrame({"order_id": [1, 2, 3]})
    result = check_nulls(df, "order_id")
    assert result["passed"] is True

def test_excessive_nulls():
    df = pd.DataFrame({"order_id": [1, None, None, 4]})
    result = check_nulls(df, "order_id")
    assert result["passed"] is False

def test_acceptable_nulls():
    df = pd.DataFrame({
        "order_id": [1] * 19 + [None]
    })
    result = check_nulls(df, "order_id")
    assert result["passed"] is True