import pandas as pd
from src.validate.rules import rule_positive_price, rule_missing_market

def test_rule_positive_price_rejects_negative():
    df = pd.DataFrame({"price": [100, -50, 0, 200]})
    bad = rule_positive_price(df)
    assert len(bad) == 2
    assert set(bad["price"]) == {-50, 0}

def test_rule_missing_market_finds_empty():
    df = pd.DataFrame({"market": ["Mukono", None, "", "Bwaise"]})
    bad = rule_missing_market(df)
    assert len(bad) == 2