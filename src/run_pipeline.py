from src.ingest.source_a import ingest_source_a
from src.ingest.source_b import ingest_source_b
from src.transform.clean import clean_data
from src.transform.merge import merge_data
from src.common.logging_setup import get_logger

PATH = "data/processed/prices_with_rainfall.parquet"
logger = get_logger()

def run_pipe():
    logger.info("=== Pipeline run started ===")

    logger.info("Stage 1: Ingesting Source A")
    source_a = ingest_source_a()
    logger.info(f"Stage 11: Source A Ingested rows out: {len(source_a)}")

    logger.info("=== Source B ===")
    logger.info("Stage 2: Ingesting Source B")
    source_b = ingest_source_b()
    logger.info(f"Stage 22: Source B Ingested rows out: {len(source_b)}")

    logger.info("Stage 3: Cleaning source a...")
    clean_prices, decisions = clean_data()   # ← may need to pass source_a here
    logger.info(
        f"Stage 33: Source A cleaned rows in: {len(source_a)} "
        f"rows out: {len(clean_prices)} "
        f"Decisions: {len(decisions)}"
    )

    logger.info("Stage 4: Merging Price and Rainfall")
    merged = merge_data(clean_prices, source_b)
    logger.info(
        f"Stage 44: Merge Complete: rows in: {len(clean_prices)} "
        f"rows out: {len(merged)}"
    )

    logger.info("Stage 5: Saving merged file")
    merged.to_parquet(PATH, index=False)
    logger.info(f"Stage 55: Saving complete: Saved {len(merged)} rows")
    logger.info("=== PIPELINE RUN COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_pipe()