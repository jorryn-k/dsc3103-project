Step 1 — Event Time

The producer deliberately generates some earlier event timestamps to simulate delayed events. In real life, an event may occur before it reaches a processing system because of network delays or temporary connectivity problems. For example, a market vendor could record a maize price at 10:00 AM, but the central system might only receive that information at 10:05 AM.


Step 3 — Window Finalisation

> A window's result does not appear immediately after the window ends. The consumer waits for an additional period controlled by the `<span>WATERMARK</span>` constant. In this experiment, the window duration is 10 seconds and the allowed lateness is 20 seconds. Therefore, a window is eligible for finalisation 20 seconds after its end. This gives delayed events an opportunity to be included in their correct event-time window.
>
>
> The producer generated 300 unique market-price events and wrote 308 records to the event log, including 8 duplicate records.
>
> The consumer used 10-second tumbling windows and a 20-second allowed-lateness setting.
>
> **Observed results:**
>
> * Total records: 308
> * Duplicate events: 8
> * Late events: 57
> * Events included in finalised windows: 243
> * Number of finalised windows: 4
>
> The consumer successfully detected duplicate events, identified events that arrived beyond the permitted lateness period, and calculated the count and average market price for each completed window.
>
> The results demonstrate how event-time windowing, duplicate detection, and lateness handling influence streaming analytics.
>
>
> ### Watermark Experiment — 5 Seconds
>
> **Configuration:**
>
> * Window size: 10 seconds
> * Watermark allowance: 5 seconds
> * Idle timeout: 90 seconds
>
> **Results:**
>
> * Total records generated: 319
> * Duplicate records: 19
> * Late events: 30
> * Events processed into windows: 270
> * Finalised windows: 4
>
> **Interpretation:**
>
> The consumer successfully processed 270 unique, on-time events into four tumbling windows. It detected 19 duplicate records and classified 30 events as late.
>
> A 5-second watermark allowance means that each window becomes eligible for finalisation five seconds after its end. This reduces the waiting time for results but may exclude events that arrive after the allowed period.
>
> The results demonstrate the trade-off between producing timely results and accommodating delayed events.

### Watermark Experiment — Comparison and Interpretation

The experiment compared two allowed-lateness settings: 5 seconds and 40 seconds, using 10-second tumbling windows.

**Results:**

| Metric | 5-second watermark | 40-second watermark |
|---|---:|---:|
| Total records | 319 | 317 |
| Duplicates | 19 | 17 |
| Late events | 30 | 0 |
| Processed events | 270 | 300 |
| Finalised windows | 4 | 5 |

**Interpretation:**

With a 5-second watermark allowance, 30 events were rejected as late. With a 40-second allowance, no events were rejected, and all 300 unique events were included in the window calculations.

This demonstrates the trade-off between result timeliness and completeness. A shorter watermark allowance produces finalised results sooner but increases the possibility of excluding delayed events. A longer allowance accommodates more delayed events but postpones finalisation.

The two runs used newly generated event streams with random delays, so the results are illustrative rather than a controlled comparison using identical events.

**Conclusion:**

The appropriate watermark allowance depends on the application. Systems requiring immediate results may prefer shorter waiting periods, while systems prioritising complete analytical results may tolerate longer delays.

Total records without deduplication: 317
Total records with deduplication: 300
Duplicate records removed: 17
Sum of prices without deduplication: 880444.0
Sum of prices with deduplication: 828638.0
Mean price without deduplication: 2777.43
Mean price with deduplication: 2762.13

### Deduplication Experiment — Interpretation

The experiment compared market-price records with and without deduplication.

Without deduplication, the dataset contained 317 records, while enabling deduplication reduced this to 300 unique events. Therefore, 17 duplicate records were identified and removed.

The sum of prices decreased from 880,444 to 828,638 after deduplication. Similarly, the mean price decreased from 2,777.43 to 2,762.13.

These findings demonstrate that duplicate events can distort analytical results by inflating event counts and totals and potentially changing calculated averages.

**Conclusion:** Deduplication improves data reliability by ensuring that each event contributes only once to the analytical calculations.

### Failure and Recovery Experiment

**Objective**

To investigate how a streaming consumer behaves when interrupted and restarted, and to determine whether its processing state is preserved.

**Procedure**

1. Started the streaming consumer and producer.
2. Interrupted the consumer using Ctrl + C while the producer was generating events.
3. Allowed the producer to finish writing events to the JSONL event log.
4. Restarted the consumer to observe how it handled the existing records.

**Observations**

The producer continued writing records to the event log after the consumer was interrupted. This demonstrated that event generation and consumption were independent processes.

When the consumer restarted, its in-memory variables, including `offset`, `seen_ids`, `windows`, and `finalised`, were initialised again.

Since the consumer did not persist its processing state, it started reading the event log from the beginning rather than resuming from its previous position.

Previously processed events could therefore be processed again. However, because the implementation uses wall-clock-based lateness checks, old events could also be rejected as late during replay.

**Conclusion**

The experiment demonstrates that retaining events in a broker does not automatically guarantee correct recovery after a consumer failure.

A more reliable streaming system should persist consumer offsets, maintain checkpoints for window state, and preserve deduplication information across restarts.

These mechanisms would allow processing to resume more consistently after failures and reduce the risk of duplicate processing or lost analytical state.

### Streaming Architecture

The implemented streaming system consists of four main components:

**1. Producer:** Reads the market-price Parquet dataset and generates events containing an event ID, market, commodity, price, and event timestamp.

**2. Event log (simulated broker):** Stores generated events in a JSONL file. This separates event production from consumption and allows events to remain available after the consumer stops.

**3. Consumer:** Reads new records from the event log, detects duplicates, applies lateness checks, and groups accepted events into 10-second tumbling windows.

**4. Analytical output:** Calculates and prints the event count and mean market price for each finalised window.

The system demonstrates basic event-driven processing, event-time windowing, duplicate handling, and failure-recovery limitations.

Unlike a production message broker such as Apache Kafka, the JSONL file does not provide built-in offset management, consumer coordination, or fault-tolerant state recovery.