"""The integrated courier pipeline: Sort -> Knapsack -> Dijkstra -> Nearest-Neighbor."""
import time

from parcels import parcel_value
from sorting import merge_sort, parcel_sort_key
from knapsack import knapsack
from route_planner import build_distance_matrix, nearest_neighbor_route, expand_route


def run_pipeline(parcels, graph, capacity):
    depot = graph.depot
    for p in parcels:
        if p.destination not in graph.adj:
            raise ValueError(f"{p.parcel_id}: destination {p.destination} not in graph")

    timings = {}

    # 1) prioritise parcels (most urgent first)
    t = time.perf_counter()
    ordered = merge_sort(parcels, key=parcel_sort_key)
    timings["sorting"] = time.perf_counter() - t

    # 2) choose the best set of parcels for ONE trip
    t = time.perf_counter()
    weights = [p.weight for p in ordered]
    values = [parcel_value(p) for p in ordered]
    best_value, chosen_idx, table = knapsack(weights, values, capacity)
    timings["knapsack"] = time.perf_counter() - t
    selected = [ordered[i] for i in chosen_idx]

    # 3) shortest distances between depot and every delivery stop
    stops = sorted({p.destination for p in selected})
    t = time.perf_counter()
    dist, prevs = build_distance_matrix(graph, [depot] + stops)
    timings["dijkstra"] = time.perf_counter() - t

    # 4) visiting order
    t = time.perf_counter()
    route, length = nearest_neighbor_route(dist, depot, stops)
    timings["nearest_neighbor"] = time.perf_counter() - t

    timings["total"] = sum(timings.values())
    return {
        "ordered": ordered, "weights": weights, "values": values,
        "best_value": best_value, "table": table, "selected": selected,
        "total_weight": sum(p.weight for p in selected),
        "stops": stops, "dist": dist, "route": route, "route_length": length,
        "full_path": expand_route(route, prevs), "timings": timings,
    }
