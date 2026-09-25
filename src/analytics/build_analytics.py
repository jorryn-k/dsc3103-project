import os
import time
import pandas as pd
import duckdb as db

RAW_JOINED_PATH = "data/processed/prices_with_rainfall.parquet"
DB_PATH = "data/processed/analytics.duckdb"

def baseline_query_maize():
    t0 = time.perf_counter()
    result = db.sql(f"""
        SELECT market, AVG(price) AS mean_price
        FROM '{RAW_JOINED_PATH}'
        WHERE commodity = 'Maize'
        GROUP BY market
        ORDER BY mean_price DESC
    """).df()
    elapsed = time.perf_counter() - t0
    print("=== Step 1: Baseline query - Maize ===")
    print(result)
    print(f"Time: {elapsed:.4f}s | File size: {os.path.getsize(RAW_JOINED_PATH)} bytes")
    return elapsed

def baseline_query_beans():
    t0 = time.perf_counter()
    result = db.sql(f"""
        SELECT market, AVG(price) AS mean_price
        FROM '{RAW_JOINED_PATH}'
        WHERE commodity = 'Beans'
        GROUP BY market
        ORDER BY mean_price DESC
    """).df()
    elapsed = time.perf_counter() - t0
    print("=== Step 1: Baseline query - Beans ===")
    print(result)
    print(f"Time: {elapsed:.4f}s | File size: {os.path.getsize(RAW_JOINED_PATH)} bytes")
    return elapsed

def build_star_schema():
    df = pd.read_parquet(RAW_JOINED_PATH)
    con = db.connect(DB_PATH)

    # --- dim_market (already given) ---
    dim_market = df[["market"]].drop_duplicates().reset_index(drop=True)
    dim_market["market_id"] = dim_market.index
    con.execute("CREATE OR REPLACE TABLE dim_market AS SELECT * FROM dim_market")

    # --- dim_commodity (you fill this in) ---
    dim_commodity = df[["commodity"]].drop_duplicates().reset_index(drop=True)
    dim_commodity["commodity_id"] = dim_commodity.index
    con.execute("CREATE OR REPLACE TABLE dim_commodity AS SELECT * FROM dim_commodity")

    # --- fact table ---
    # First attach the IDs by merging
    fact = df.merge(dim_market, on="market", how="left")
    fact = fact.merge(dim_commodity, on="commodity", how="left")

    # Keep only the columns we need
    fact = fact[["id", "date", "market_id", "commodity_id", "price", "rainfall_mm"]]

    con.execute("CREATE OR REPLACE TABLE fact_price_observation AS SELECT * FROM fact")

    print("=== Step 3: Star schema built ===")
    print("Fact table row count:", con.sql("SELECT COUNT(*) FROM fact_price_observation").fetchone()[0])
    con.close()

def run_analytical_queries():
    con = db.connect(DB_PATH)

    # Query 1 (given)
    print("=== Query 1: Average price by market ===")
    print(con.sql("""
        SELECT dm.market, AVG(f.price) AS mean_price
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
        ORDER BY mean_price DESC
    """).df())

    # Query 2 (given)
    print("=== Query 2: Observation count by commodity ===")
    print(con.sql("""
        SELECT dc.commodity, COUNT(*) AS n_observations
        FROM fact_price_observation f
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dc.commodity
        ORDER BY n_observations DESC
    """).df())

    # Query 3 – Average price + average rainfall by commodity
    print("=== Query 3: Average price and rainfall by commodity ===")
    print(con.sql("""
        SELECT dc.commodity,
               AVG(f.price) AS mean_price,
               AVG(f.rainfall_mm) AS mean_rainfall
        FROM fact_price_observation f
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dc.commodity
        ORDER BY mean_price DESC
    """).df())

    # Query 4 – Top market-commodity combinations by average price
    print("=== Query 4: Top 5 market-commodity combinations by mean price ===")
    print(con.sql("""
        SELECT dm.market, dc.commodity, AVG(f.price) AS mean_price, COUNT(*) AS n
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        JOIN dim_commodity dc ON f.commodity_id = dc.commodity_id
        GROUP BY dm.market, dc.commodity
        ORDER BY mean_price DESC
        LIMIT 5
    """).df())

    # Query 5 – Mean price and rainfall by market
    print("=== Query 5: Mean price and rainfall by market ===")
    print(con.sql("""
        SELECT dm.market,
               AVG(f.price) AS mean_price,
               AVG(f.rainfall_mm) AS mean_rainfall,
               COUNT(*) AS n_obs
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
        ORDER BY mean_rainfall DESC
    """).df())

    con.close()

def compare_performance():
    # Time the flat Parquet version
    t0 = time.perf_counter()
    db.sql(f"""
        SELECT market, AVG(price) FROM '{RAW_JOINED_PATH}' GROUP BY market
    """).df()
    flat_time = time.perf_counter() - t0

    # Time the same logical query against the star schema
    con = db.connect(DB_PATH)
    t0 = time.perf_counter()
    con.sql("""
        SELECT dm.market, AVG(f.price)
        FROM fact_price_observation f
        JOIN dim_market dm ON f.market_id = dm.market_id
        GROUP BY dm.market
    """).df()
    star_time = time.perf_counter() - t0
    con.close()

    print("=== Step 5: Performance comparison ===")
    print(f"Flat Parquet query time:  {flat_time:.4f}s")
    print(f"Star schema query time:   {star_time:.4f}s")    

if __name__ == "__main__":
    baseline_query_maize()
    baseline_query_beans()
    build_star_schema()
    run_analytical_queries()
    compare_performance()
    # TODO