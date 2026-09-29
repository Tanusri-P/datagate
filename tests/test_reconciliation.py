from datagate.checks import check_reconciliation

def test_matching_revenue():
    result = check_reconciliation(1000, 1000)
    assert result["passed"] is True

def test_mismatched_revenue():
    result = check_reconciliation(1000, 1200)
    assert result["passed"] is False

def test_small_difference():
    result = check_reconciliation(1000, 1000.005)
    assert result["passed"] is True