import time
import duckdb as db
from pyspark.sql import SparkSession, functions as F
import os
import sys

os.environ["PYSPARK_PYTHON"] = sys.executable
os.environ["PYSPARK_DRIVER_PYTHON"] = sys.executable

BIG_PATH = "data/processed/prices_skewed.parquet"

def duckdb_job():
    t0 = time.perf_counter()
    result = db.sql(f"""
        SELECT market, AVG(price) AS mean_price, COUNT(*) AS n
        FROM '{BIG_PATH}'
        WHERE price IS NOT NULL
        GROUP BY market
        ORDER BY mean_price DESC
    """).df()
    elapsed = time.perf_counter() - t0
    print("=== DuckDB ===")
    print(result)
    print(f"Time: {elapsed:.3f}s")
    return elapsed

def spark_job():
    spark = (SparkSession.builder
             .appName("DSC3103")
             .master("local[*]")
             .getOrCreate())

    t0 = time.perf_counter()
    df = spark.read.parquet(BIG_PATH)

    summary = (df.filter(F.col("price").isNotNull())
                 .groupBy("market")
                 .agg(F.avg("price").alias("mean_price"),
                      F.count("*").alias("n"))
                 .orderBy(F.col("mean_price").desc()))

    print("=== Spark plan ===")
    summary.explain()

    print("=== Spark result ===")
    summary.show()
    elapsed = time.perf_counter() - t0
    print(f"Time: {elapsed:.3f}s")

    print("Partitions in input:", df.rdd.getNumPartitions())

    df.groupBy("market").count().orderBy(F.col("count").desc()).show()

    repartitioned = df.repartition(6, "market")
    repartitioned.groupBy(F.spark_partition_id().alias("pid")).count().show()
    
    spark.stop()
    return elapsed

if __name__ == "__main__":
    duckdb_job()
    spark_job()