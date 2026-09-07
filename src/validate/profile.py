#%%
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from src.validate import rules

raw_path = "data/raw/prices.csv"

#%%
def inferred_schema(df):
    print("Inferred Schema: ")
    print("---------------")
    print(df.dtypes)

#%%
def row_count(df):
    print("\nRow count: ")
    print("----------")
    print(len(df))

#%%
def missing_values(df):
    print("\nMissing Values per Column: ")
    print("--------------------------")
    print(df.isna().sum())

#%%
def duplicate_counts(df):
    print("\nDuplicate Counts: ")
    print("-----------------")
    exact_dups = rules.rule_duplicate_rows(df)
    id_dups = rules.rule_duplicate_ids(df)
    print(f"Exact duplicate rows  : {len(exact_dups)}")
    print(f"Rows with duplicate id: {len(id_dups)}")

#%%
def invalid_values(df):
    print("\nInvalid Values: ")
    print("---------------")
    neg = rules.rule_positive_price(df)
    bad_dates = rules.rule_valid_date(df)
    print(f"Non-positive prices : {len(neg)}")
    print(f"Invalid dates       : {len(bad_dates)}")

#%%
def inconsistent_categories(df):
    print("\nInconsistent Categories (commodities): ")
    print("-------------------------------------")
    print(df["commodities"].value_counts())

#%%
def summary_statistics(df):
    print("\nSummary Statistics (numeric columns): ")
    print("-------------------------------------")
    print(df.describe())

#%%
def price_histogram(df):
    print("\nPrice Histogram: ")
    print("----------------")
    print("Saving plot to docs/price_histogram.png ...")

    positive = df[df["price"] > 0]["price"]

    plt.figure(figsize=(8, 5))
    plt.hist(positive, bins=30, edgecolor="black")
    plt.title("Distribution of Price (positive values only)")
    plt.xlabel("Price")
    plt.ylabel("Frequency")
    plt.grid(axis="y", alpha=0.5)

    Path("docs").mkdir(exist_ok=True)
    plt.savefig("docs/price_histogram.png", dpi=120, bbox_inches="tight")
    plt.close()

    print("Plot saved → docs/price_histogram.png")

#%%
def run_files(path=raw_path):
    df = pd.read_csv(path)
    inferred_schema(df)
    row_count(df)
    missing_values(df)
    duplicate_counts(df)
    invalid_values(df)
    inconsistent_categories(df)
    summary_statistics(df)
    price_histogram(df)

#%%
if __name__ == "__main__":
    run_files()