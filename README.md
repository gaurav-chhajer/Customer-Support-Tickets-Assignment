# Customer Support Tickets Assignment

- `solution.py` and `tickets.json`: Part A - data cleaning and ticket statistics.
- `evaluation.md`: Part B1 - summary scores and justifications.
- `graph.cypher`: Part B2 - Neo4j graph and query.

## Part A

Requires Python 3. Run from this folder:

```bash
python solution.py
```

Expected results: each product has 1 open and 1 resolved ticket; average resolution time is 13.5 hours.

The first occurrence of each ticket ID is kept. Invalid records/IDs are skipped;
missing text becomes `Unknown`. Invalid statuses are excluded from counts, and
missing, invalid, negative, or ambiguously zoned durations are excluded from the average.
Processing takes expected O(n) time and O(u + p) extra space, where `u` is the number
of unique ticket IDs and `p` is the number of distinct products (4 and 2 in this dataset);
loading the JSON array itself takes O(n) space.

## Part B2

In Neo4j Browser, run the `CREATE` statement in `graph.cypher` once on an empty database, then run the `MATCH` query.

Expected result: **Asha Rao - 2 distinct products**.
