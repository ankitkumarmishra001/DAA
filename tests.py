"""Correctness evidence for every algorithm.  Run:  python tests.py"""
import itertools
import random

from generate_data import random_parcels
from graph import generate_random_graph, dijkstra, INF
from knapsack import knapsack
from route_planner import build_distance_matrix, nearest_neighbor_route
from sorting import merge_sort, quick_sort, parcel_sort_key


def test_sorting():
    for seed in range(20):
        parcels = random_parcels(200, 20, seed)
        expected = sorted(parcels, key=parcel_sort_key)
        assert merge_sort(parcels, parcel_sort_key) == expected, "merge sort wrong/unstable"
        qs = quick_sort(parcels, parcel_sort_key)
        assert [parcel_sort_key(p) for p in qs] == [parcel_sort_key(p) for p in expected], "quick sort wrong"
    assert merge_sort([]) == [] and quick_sort([5]) == [5]
    print("PASS  sorting: merge sort (stable) and quick sort match Python's sorted()")


def test_knapsack():
    rng = random.Random(7)
    for _ in range(50):
        n = rng.randint(1, 10)
        w = [rng.randint(1, 12) for _ in range(n)]
        v = [rng.randint(1, 15) for _ in range(n)]
        cap = rng.randint(0, 40)
        best, chosen, _ = knapsack(w, v, cap)
        brute = max(sum(v[i] for i in combo)
                    for r in range(n + 1) for combo in itertools.combinations(range(n), r)
                    if sum(w[i] for i in combo) <= cap)
        assert best == brute, (w, v, cap, best, brute)
        assert sum(w[i] for i in chosen) <= cap and sum(v[i] for i in chosen) == best
    # the classic case where greedy-by-ratio fails but DP succeeds
    best, chosen, _ = knapsack([6, 5, 5], [7, 5, 5], 10)
    assert best == 10 and chosen == [1, 2]
    print("PASS  knapsack: equals brute force on 50 random cases; beats greedy on the classic example")


def test_dijkstra():
    for seed in range(10):
        g = generate_random_graph(14, seed)
        nodes = g.nodes()
        fw = {a: {b: (0 if a == b else g.adj[a].get(b, INF)) for b in nodes} for a in nodes}
        for k in nodes:                       # Floyd-Warshall as an independent check
            for i in nodes:
                for j in nodes:
                    if fw[i][k] + fw[k][j] < fw[i][j]:
                        fw[i][j] = fw[i][k] + fw[k][j]
        for a in nodes:
            d, _ = dijkstra(g, a)
            assert d == fw[a], f"Dijkstra mismatch from {a}"
    print("PASS  dijkstra: matches Floyd-Warshall on 10 random graphs")


def test_route():
    g = generate_random_graph(12, 3)
    stops = ["C2", "C5", "C7", "C9", "C11"]
    dist, _ = build_distance_matrix(g, ["D"] + stops)
    route, length = nearest_neighbor_route(dist, "D", stops)
    assert route[0] == route[-1] == "D" and sorted(route[1:-1]) == sorted(stops)
    assert length == sum(dist[a][b] for a, b in zip(route, route[1:]))
    best = min(sum(dist[a][b] for a, b in zip(("D",) + p, p + ("D",)))
               for p in itertools.permutations(stops))
    assert length >= best
    print(f"PASS  route: visits every stop once, starts/ends at depot "
          f"(NN length {length} vs optimal {best})")


if __name__ == "__main__":
    test_sorting(); test_knapsack(); test_dijkstra(); test_route()
    print("\nAll tests passed.")
