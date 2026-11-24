"""Phase 4 - performance testing.  Run:  python benchmark.py

Produces (in ./results):
    runtime_results.csv   runtime of every pipeline step for each input size
    runtime_chart.png     runtime vs number of parcels (log-log)
    runtime_breakdown.png share of the total runtime per step (largest size)
    sort_comparison.png   Merge Sort vs Quick Sort vs Python's built-in sort
"""
import csv
import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from generate_data import random_dataset, random_parcels
from pipeline import run_pipeline
from sorting import merge_sort, quick_sort, parcel_sort_key

SIZES = [10, 50, 100, 200, 500, 1000]
STEPS = ["sorting", "knapsack", "dijkstra", "nearest_neighbor"]
REPEATS = 3


def benchmark_pipeline():
    rows = []
    for n in SIZES:
        parcels, graph = random_dataset(n)
        capacity = min(int(0.3 * sum(p.weight for p in parcels)), 1000)
        best = None
        for _ in range(REPEATS):                       # keep the fastest run (least noise)
            res = run_pipeline(parcels, graph, capacity)
            t = res["timings"]
            best = t if best is None else {k: min(best[k], t[k]) for k in t}
        row = {"parcels": n, "capacity": capacity, "selected": len(res["selected"]),
               "stops": len(res["stops"]), "route_km": res["route_length"]}
        row.update({k: round(best[k] * 1000, 4) for k in STEPS + ["total"]})   # ms
        rows.append(row)
        print(f"n={n:<5} cap={capacity:<5} selected={row['selected']:<4} stops={row['stops']:<4} "
              f"total={row['total']:.2f} ms")
    return rows


def benchmark_sorting():
    sizes = [1000, 2000, 5000, 10000, 20000, 50000]
    results = {"Merge Sort": [], "Quick Sort": [], "Python sorted() (Timsort)": []}
    for n in sizes:
        data = random_parcels(n, 100, seed=5)
        random.seed(0)
        for name, fn in (("Merge Sort", lambda: merge_sort(data, parcel_sort_key)),
                         ("Quick Sort", lambda: quick_sort(data, parcel_sort_key)),
                         ("Python sorted() (Timsort)", lambda: sorted(data, key=parcel_sort_key))):
            best = float("inf")
            for _ in range(REPEATS):
                t = time.perf_counter()
                fn()
                best = min(best, time.perf_counter() - t)
            results[name].append(best * 1000)
        print(f"sort n={n:<6} " + "  ".join(f"{k.split()[0]}={v[-1]:.1f}ms" for k, v in results.items()))
    return sizes, results


def make_charts(rows, sort_sizes, sort_results):
    ns = [r["parcels"] for r in rows]

    plt.figure(figsize=(8, 5))
    for step in STEPS:
        plt.plot(ns, [r[step] for r in rows], marker="o", label=step)
    plt.plot(ns, [r["total"] for r in rows], marker="s", linestyle="--", color="black", label="total")
    plt.xscale("log"); plt.yscale("log")
    plt.xlabel("Number of parcels (n)"); plt.ylabel("Runtime (ms, log scale)")
    plt.title("Runtime of each pipeline step vs input size")
    plt.grid(True, which="both", alpha=0.3); plt.legend(); plt.tight_layout()
    plt.savefig("results/runtime_chart.png", dpi=150); plt.close()

    last = rows[-1]
    plt.figure(figsize=(7, 4.5))
    vals = [last[s] for s in STEPS]
    bars = plt.bar(STEPS, vals, color=["#4C78A8", "#F58518", "#54A24B", "#B279A2"])
    for b, v in zip(bars, vals):
        plt.text(b.get_x() + b.get_width() / 2, v, f"{v:.2f} ms", ha="center", va="bottom", fontsize=9)
    plt.ylabel("Runtime (ms)"); plt.title(f"Where the time goes (n = {last['parcels']} parcels)")
    plt.tight_layout(); plt.savefig("results/runtime_breakdown.png", dpi=150); plt.close()

    plt.figure(figsize=(8, 5))
    for name, vals in sort_results.items():
        plt.plot(sort_sizes, vals, marker="o", label=name)
    plt.xlabel("Number of parcels (n)"); plt.ylabel("Runtime (ms)")
    plt.title("Sorting comparison: Merge Sort vs Quick Sort")
    plt.grid(True, alpha=0.3); plt.legend(); plt.tight_layout()
    plt.savefig("results/sort_comparison.png", dpi=150); plt.close()


if __name__ == "__main__":
    rows = benchmark_pipeline()
    with open("results/runtime_results.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)
    sort_sizes, sort_results = benchmark_sorting()
    make_charts(rows, sort_sizes, sort_results)
    print("\nSaved: results/runtime_results.csv, runtime_chart.png, runtime_breakdown.png, sort_comparison.png")
