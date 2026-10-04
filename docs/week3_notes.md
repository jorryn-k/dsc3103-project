
# Week 3 Notes – Pipeline Design

## ETL vs ELT

I chose an ETL-style approach. Source A (messy prices CSV) is cleaned before it is joined with Source B (rainfall API data). Source B is already fairly clean, but Source A contains negative prices, invalid dates, and inconsistent commodity names, so transforming it first avoids spreading bad values into the merged dataset. The cleaned prices and rainfall are then loaded together into a single Parquet file for later analysis.

## Idempotency

Each run of `run_pipeline.py` overwrites `data/processed/prices_with_rainfall.parquet`. This is simple and guarantees that running the pipeline twice does not duplicate rows. Because the output is a full rebuild from the raw sources, overwrite is safer than appending for this project.
