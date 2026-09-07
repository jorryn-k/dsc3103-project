# %%

import pandas as pd

def rule_positive_price(df):
    """Return rows where price is negative or zero."""
    negative_prices = df[df["price"] <= 0].copy()
    negative_prices["Reason"] = "Non-positive price"
    return negative_prices

def rule_duplicate_ids(df):
    """Return rows that have a duplicated id."""
    duplicate_ids = df[df.duplicated(subset=["id"], keep=False)].copy()
    duplicate_ids["Reason"] = "Duplicate id"
    return duplicate_ids


def rule_duplicate_rows(df):
    """Return exact duplicate rows."""
    bad = df[df.duplicated(keep=False)].copy()
    bad["Reason"] = "Exact duplicate row"
    return bad


def rule_valid_date(df):
    """Return rows with invalid dates."""
    # Try to convert; invalid ones become NaT
    dates = pd.to_datetime(df["date"], errors="coerce")
    bad = df[dates.isna()].copy()
    bad["Reason"] = "Invalid date"
    return bad


def rule_missing_market(df):
    """Return rows where market is missing or empty."""
    bad = df[df["market"].isna() | (df["market"].astype(str).str.strip() == "")].copy()
    bad["Reason"] = "Missing market"
    return bad


def rule_known_commodity(df):
    """
    Return rows whose commodity is not a known value
    after normalising case and whitespace.
    """
    known = {"maize", "beans"}          # the only commodities we accept
    cleaned = df["commodities"].astype(str).str.strip().str.lower()
    bad = df[~cleaned.isin(known)].copy()
    bad["Reason"] = "Unknown or inconsistent commodity"
    return bad
# %%
