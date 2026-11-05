
# Lab 04 Notes

# Step 4 description

The fact table sits in the centre and stores one row per price observation.

It links to dim_market via market_id and to dim_commodity via commodity_id

# Step 6 – Architecture Justification

**Is a star schema worth the added complexity at the current data size?**

From the Step 5 performance comparison, the flat Parquet query took **0.0056 seconds** while the same query against the star schema took **0.0041 seconds**. The difference is tiny.

At this data size (only 889 rows), the extra join and the need to maintain dimension tables do not give any meaningful speed advantage. Both versions finish in a few milliseconds, so performance alone does not justify the star schema.

Even so, I still think the star schema is worth the small extra complexity. It keeps the data cleaner by separating market and commodity names from the numeric facts. The queries also become clearer and more consistent. Most importantly, the design is already prepared for growth — if the dataset later becomes much larger, the same structure can be partitioned or indexed without a complete redesign.

In short, although the performance gain is currently negligible, the structural benefits outweigh the modest increase in complexity, so I would keep the star schema.
