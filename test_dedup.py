
import json
from collections import Counter

BROKER = "data/stream/events.jsonl"

with open(BROKER, encoding="utf-8") as f:
    events = [json.loads(line) for line in f if line.strip()]

unique_events = {}
for event in events:
    unique_events.setdefault(event["event_id"], event)

print("DEDUPLICATION EXPERIMENT")
print("------------------------")
print("Total records without deduplication:", len(events))
print("Total records with deduplication:", len(unique_events))
print("Duplicate records removed:", len(events) - len(unique_events))

raw_total = sum(event["price"] for event in events)
dedup_total = sum(event["price"] for event in unique_events.values())

print("Sum of prices without deduplication:", round(raw_total, 2))
print("Sum of prices with deduplication:", round(dedup_total, 2))
print("Mean price without deduplication:", round(raw_total / len(events), 2))
print("Mean price with deduplication:", round(dedup_total / len(unique_events), 2))
