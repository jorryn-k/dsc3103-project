#%%
import pandas as pd
from pathlib import Path
from src.validate import rules

RAW_PATH = "data/raw/prices.csv"
CLEAN_PATH = "data/processed/prices_clean.parquet"

#%%
def clean_data(path=RAW_PATH):
    print("=" * 60)
    print("DATA CLEANING – Lab 02")
    print("=" * 60)

    df = pd.read_csv(path)
    original_rows = len(df)
    print(f"Starting with {original_rows} rows\n")

    log = []

    # 1. Reject non-positive prices
    bad_price = rules.rule_positive_price(df)
    n = len(bad_price)
    df = df[df["price"] > 0].copy()
    log.append(f"Rejected {n} rows with non-positive price")
    print(f"Rejected {n} rows with non-positive price")

    # 2. Reject exact duplicate rows
    before = len(df)
    df = df.drop_duplicates(keep="first")
    n = before - len(df)
    log.append(f"Rejected {n} exact duplicate rows")
    print(f"Rejected {n} exact duplicate rows")

    # 3. Reject duplicate ids
    before = len(df)
    df = df.drop_duplicates(subset=["id"], keep="first")
    n = before - len(df)
    log.append(f"Rejected {n} rows with duplicate id")
    print(f"Rejected {n} rows with duplicate id")

    # 4. Reject invalid dates
    bad_dates = rules.rule_valid_date(df)
    n = len(bad_dates)
    df = df[pd.to_datetime(df["date"], errors="coerce").notna()].copy()
    log.append(f"Rejected {n} rows with invalid dates")
    print(f"Rejected {n} rows with invalid dates")

    # 5. Impute missing market
    missing_market = rules.rule_missing_market(df)
    n = len(missing_market)
    df["market"] = df["market"].fillna("Unknown")
    df.loc[df["market"].astype(str).str.strip() == "", "market"] = "Unknown"
    log.append(f"Imputed {n} missing market values with 'Unknown'")
    print(f"Imputed {n} missing market values with 'Unknown'")

    # 6. Normalize commodity names
    unknown = rules.rule_known_commodity(df)
    n_unknown = len(unknown)

    df["commodities"] = (
        df["commodities"]
        .astype(str)
        .str.strip()
        .str.lower()
        .replace({"maize": "Maize", "beans": "Beans"})
    )

    known = {"Maize", "Beans"}
    mask = ~df["commodities"].isin(known)
    n_still_unknown = mask.sum()
    df.loc[mask, "commodities"] = "Unknown"

    log.append(f"Normalized commodity names; {n_unknown} originally unknown, "
               f"{n_still_unknown} set to 'Unknown'")
    print(f"Normalized commodity names")
    print(f"  - Originally unknown: {n_unknown}")
    print(f"  - Set to 'Unknown'  : {n_still_unknown}")

    # Final summary
    final_rows = len(df)
    print("\n" + "=" * 60)
    print(f"Original rows : {original_rows}")
    print(f"Final rows    : {final_rows}")
    print(f"Rows removed  : {original_rows - final_rows}")
    print("=" * 60)

    print("\nCleaning decisions log:")
    for entry in log:
        print(" •", entry)

    # Save
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    df.to_parquet(CLEAN_PATH, index=False)
    print(f"\nCleaned data saved to → {CLEAN_PATH}")

    return df, log

#%%
if __name__ == "__main__":
    clean_data()