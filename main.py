"""Mini-Courier Planner - run the full pipeline and print/save a readable trace.

Usage:
    python main.py                                   # small sample dataset, capacity 40
    python main.py --parcels datasets/parcels_200.csv --graph datasets/graph_200.json --capacity 300
"""
import argparse
import os

from parcels import load_parcels, parcel_value
from graph import Graph
from knapsack import format_table
from pipeline import run_pipeline


def main():
    ap = argparse.ArgumentParser(description="Mini-Courier Planner")
    ap.add_argument("--parcels", default="datasets/parcels_small.csv")
    ap.add_argument("--graph", default="datasets/graph_small.json")
    ap.add_argument("--capacity", type=int, default=40, help="truck capacity in kg")
    ap.add_argument("--name", default=None, help="label for the results file")
    args = ap.parse_args()

    parcels = load_parcels(args.parcels)
    graph = Graph.load(args.graph)
    res = run_pipeline(parcels, graph, args.capacity)

    lines = []
    out = lines.append
    out("=" * 70)
    out("MINI-COURIER PLANNER")
    out("=" * 70)
    out(f"Parcels loaded : {len(parcels)}   Truck capacity : {args.capacity} kg")
    out(f"Graph          : {len(graph.nodes())} nodes, {graph.edge_count()} roads, depot = {graph.depot}")

    out("\n--- PHASE 2a: parcels sorted by urgency (Merge Sort) ---")
    out(f"{'ID':<7}{'Weight':>7}{'Priority':>9}{'Deadline':>9}{'Value':>7}  Dest")
    for p in res["ordered"][:25]:
        out(f"{p.parcel_id:<7}{p.weight:>7}{p.priority:>9}{p.deadline:>9}{parcel_value(p):>7}  {p.destination}")
    if len(res["ordered"]) > 25:
        out(f"... ({len(res['ordered']) - 25} more parcels not shown)")

    out("\n--- PHASE 2b: 0/1 Knapsack (Dynamic Programming) ---")
    if len(res["ordered"]) <= 15 and args.capacity <= 60:
        out("DP table (rows = parcels in sorted order, columns = capacity in kg):")
        step = max(1, args.capacity // 10)   # show ~10 capacity columns so it fits on screen
        out(format_table(res["table"], res["weights"], [p.parcel_id for p in res["ordered"]], step))
    out(f"\nBest total value : {res['best_value']}")
    out(f"Total weight     : {res['total_weight']} / {args.capacity} kg")
    out(f"Selected parcels ({len(res['selected'])}): " + ", ".join(p.parcel_id for p in res["selected"]))
    chosen = {p.parcel_id for p in res["selected"]}
    left = [p.parcel_id for p in res["ordered"] if p.parcel_id not in chosen]
    out(f"Left for later trips ({len(left)}): " + (", ".join(left[:30]) + (" ..." if len(left) > 30 else "")))

    out("\n--- PHASE 3a: Dijkstra shortest distances (km) between depot and stops ---")
    nodes = [graph.depot] + res["stops"]
    out(f"{'':<5}" + "".join(f"{n:>6}" for n in nodes[:20]))
    for a in nodes[:20]:
        out(f"{a:<5}" + "".join(f"{res['dist'][a][b]:>6}" for b in nodes[:20]))
    if len(nodes) > 20:
        out(f"... (matrix truncated to first 20 of {len(nodes)} nodes)")

    out("\n--- PHASE 3b: Nearest-Neighbor delivery route ---")
    out("Stop order  : " + " -> ".join(res["route"]))
    out("Road path   : " + " -> ".join(res["full_path"]))
    out(f"Route length: {res['route_length']} km")

    out("\n--- Runtime of each step ---")
    for k, v in res["timings"].items():
        out(f"{k:<18}{v * 1000:>10.3f} ms")

    text = "\n".join(lines)
    print(text)
    name = args.name or os.path.splitext(os.path.basename(args.parcels))[0]
    os.makedirs("results", exist_ok=True)
    with open(f"results/output_{name}.txt", "w") as f:
        f.write(text + "\n")
    print(f"\n[saved to results/output_{name}.txt]")


if __name__ == "__main__":
    main()
