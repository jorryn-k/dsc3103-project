import pandas as pd


def merge_data(clean_df: pd.DataFrame, rainfall_df: pd.DataFrame) -> pd.DataFrame:
    """
    Join cleaned prices with rainfall on market + date.
    Left join keeps all price rows even when rainfall is missing.
    """
    # Make sure date columns are the same type before joining
    clean_df = clean_df.copy()
    rainfall_df = rainfall_df.copy()

    clean_df["date"] = pd.to_datetime(clean_df["date"], errors="coerce")
    rainfall_df["date"] = pd.to_datetime(rainfall_df["date"], errors="coerce")

    # Standardise market names a bit to improve match rate
    clean_df["market"] = clean_df["market"].astype(str).str.strip()
    rainfall_df["market"] = rainfall_df["market"].astype(str).str.strip()

    merged = clean_df.merge(
        rainfall_df,
        on=["market", "date"],
        how="left"
    )

    return merged