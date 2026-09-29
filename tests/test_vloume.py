from datagate.checks import check_volume

def test_normal_volume():
    result = check_volume(100, 100)
    assert result["passed"] is True

def test_low_volume():
    result = check_volume(40, 100)
    assert result["passed"] is False

def test_high_volume():
    result = check_volume(200, 100)
    assert result["passed"] is False