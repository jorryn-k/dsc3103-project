
import json
import time

BROKER = "data/stream/events.jsonl"
LATE_LOG = "data/stream/late_events.jsonl"
DUP_LOG = "data/stream/duplicate_events.jsonl"

WINDOW = 10        # tumbling window length, seconds
WATERMARK = 20    # how long we wait for late events, seconds
IDLE_STOP = 90     # stop when no new events arrive for this long

DEDUP_ENABLED = True

def window_start(event_time):
    return int(event_time // WINDOW) * WINDOW


def append(path, record):
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")


def consume():
    for p in (LATE_LOG, DUP_LOG):
        open(p, "w").close()

    offset = 0
    windows = {}
    finalised = set()
    seen_ids = set()
    last_new = time.time()

    while time.time() - last_new < IDLE_STOP:

        # 1. Read new lines from the broker
        with open(BROKER) as f:
            lines = f.readlines()

        new_lines = lines[offset:]
        offset = len(lines)

        if new_lines:
            last_new = time.time()

        # 2. Process each event
        for line in new_lines:
            event = json.loads(line)
            now = time.time()

            # TODO A: Detect duplicates
            if DEDUP_ENABLED:
                if event["event_id"] in seen_ids:
                    append(DUP_LOG, event)
                    continue

                seen_ids.add(event["event_id"])

            ws = window_start(event["event_time"])

            # TODO B: Detect late events
            if ws in finalised:
                event["reason"] = "Window already finalised"
                append(LATE_LOG, event)
                continue

            if now >= ws + WINDOW + WATERMARK:
                event["reason"] = "Beyond allowed lateness"
                append(LATE_LOG, event)
                continue

            # TODO C: Update the window
            window = windows.setdefault(
                ws, {"n": 0, "total": 0.0}
            )

            window["n"] += 1
            window["total"] += event["price"]

        # 3. Finalise completed windows
        now = time.time()

        for ws in sorted(windows):

            # TODO D: Print final window results
            if ws not in finalised and now >= ws + WINDOW + WATERMARK:
                count = windows[ws]["n"]
                mean_price = windows[ws]["total"] / count

                print(
                    f"Window {ws}: "
                    f"count={count}, "
                    f"mean_price={mean_price:.2f}"
                )

                finalised.add(ws)

        time.sleep(0.2)

    print(
        "Consumer idle, stopping. Late:",
        sum(1 for _ in open(LATE_LOG)),
        "| Duplicates:",
        sum(1 for _ in open(DUP_LOG))
    )


if __name__ == "__main__":
    consume()
