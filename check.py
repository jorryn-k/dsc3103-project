# %%

import pandas as pd
from src.validate.rules import (
    rule_positive_price,
    rule_duplicate_ids,
    rule_duplicate_rows,
    rule_valid_date,
    rule_missing_market,
    rule_known_commodity,
    rule_negative_rain,
)
from src.ingest.source_a import ingest_source_a
from src.ingest.source_b import ingest_source_b
from src.transform.clean import clean_data

df = pd.read_csv("data/raw/prices.csv")

print("=== rule_positive_price ===")
print(rule_positive_price(df).head())
print(f"Failed rows: {len(rule_positive_price(df))}\n")

print("=== rule_duplicate_ids ===")
print(rule_duplicate_ids(df).head())
print(f"Failed rows: {len(rule_duplicate_ids(df))}\n")

print("=== rule_duplicate_rows ===")
print(rule_duplicate_rows(df).head())
print(f"Failed rows: {len(rule_duplicate_rows(df))}\n")

print("=== rule_valid_date ===")
print(rule_valid_date(df).head())
print(f"Failed rows: {len(rule_valid_date(df))}\n")

print("=== rule_missing_market ===")
print(rule_missing_market(df).head())
print(f"Failed rows: {len(rule_missing_market(df))}\n")

print("=== rule_known_commodity ===")
print(rule_known_commodity(df).head())
print(f"Failed rows: {len(rule_known_commodity(df))}\n")

source_a_df = ingest_source_a()
print(source_a_df.shape)

source_b_df = ingest_source_b()
print(source_b_df)

clean_prices, _ = clean_data()
print(len(clean_prices))

negative_rain = rule_negative_rain(source_b_df)
print(len(negative_rain))