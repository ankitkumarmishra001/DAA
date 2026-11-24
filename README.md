# Mini-Courier Planner (DAA Capstone)

An integrated Python prototype that, given parcels and delivery points, produces a
**packing plan** and an **ordered delivery route**.

| Stage | Algorithm | Complexity | File |
|---|---|---|---|
| Prioritise parcels | Merge Sort (Quick Sort for comparison) | O(n log n) | `sorting.py` |
| Choose parcels for one trip | 0/1 Knapsack (Dynamic Programming) | O(n·W) | `knapsack.py` |
| Shortest distances | Dijkstra with a min-heap | O((V+E) log V) | `graph.py` |
| Visiting order | Nearest-Neighbor TSP approximation | O(k²) | `route_planner.py` |

Pipeline: `Parcels (CSV) -> Sort by deadline -> Knapsack -> Dijkstra -> Nearest-Neighbor route`
(`pipeline.py` joins the steps and times each one).

## How to run
```
pip install -r requirements.txt     # only matplotlib, for the charts
python generate_data.py             # writes sample datasets to ./datasets
python tests.py                     # correctness checks
python main.py                      # small sample run (10 parcels, 40 kg truck)
python main.py --parcels datasets/parcels_200.csv --graph datasets/graph_200.json --capacity 300
python benchmark.py                 # runtime table + charts in ./results
```

## Data formats
* Parcels CSV: `parcel_id,weight,priority,deadline,destination`
  (weight = kg, priority 1-10, deadline = hours left, destination = graph node)
* Graph JSON: `{"depot": "D", "edges": [["D","C1",4], ...]}` (undirected, km)

## Design decisions
* Sort key: smallest deadline first, ties -> higher priority first (Merge Sort is stable).
* Knapsack value = priority, plus a bonus of 3 if the deadline is <= 8 hours (`parcels.py`),
  so urgent parcels are favoured when the truck is full.
* Route: Dijkstra gives true road distances between stops; Nearest-Neighbor then orders them.
  Nearest-Neighbor is not optimal (TSP is NP-hard) - see tests/report for the gap.

## Folder layout
`datasets/` input data - `results/` saved outputs, runtime CSV and charts - `tests.py` correctness evidence.
