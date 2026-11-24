"""Create the sample datasets in ./datasets  (run once: python generate_data.py)."""
import random
from parcels import Parcel, save_parcels
from graph import Graph, generate_random_graph

SMALL_PARCELS = [
    Parcel("P01", 8, 7, 12, "C3"), Parcel("P02", 15, 9, 6, "C1"),
    Parcel("P03", 5, 4, 24, "C2"), Parcel("P04", 12, 8, 8, "C5"),
    Parcel("P05", 7, 5, 18, "C4"), Parcel("P06", 10, 6, 10, "C6"),
    Parcel("P07", 6, 3, 30, "C7"), Parcel("P08", 9, 7, 6, "C2"),
    Parcel("P09", 14, 9, 14, "C3"), Parcel("P10", 4, 2, 20, "C1"),
]
SMALL_EDGES = [("D", "C1", 4), ("D", "C2", 7), ("D", "C3", 6), ("C1", "C2", 3),
               ("C1", "C4", 8), ("C2", "C5", 5), ("C3", "C5", 4), ("C3", "C6", 9),
               ("C4", "C5", 2), ("C5", "C7", 6), ("C6", "C7", 3)]


def random_parcels(n, num_customers, seed):
    rng = random.Random(seed)
    return [Parcel(f"P{i:04d}", rng.randint(1, 20), rng.randint(1, 10),
                   rng.randint(2, 48), f"C{rng.randint(1, num_customers)}")
            for i in range(1, n + 1)]


def random_dataset(n, seed=1):
    customers = max(5, n // 5)
    return random_parcels(n, customers, seed), generate_random_graph(customers, seed)


if __name__ == "__main__":
    save_parcels(SMALL_PARCELS, "datasets/parcels_small.csv")
    g = Graph("D")
    for u, v, w in SMALL_EDGES:
        g.add_edge(u, v, w)
    g.save("datasets/graph_small.json")
    for n in (50, 200, 1000):
        parcels, graph = random_dataset(n)
        save_parcels(parcels, f"datasets/parcels_{n}.csv")
        graph.save(f"datasets/graph_{n}.json")
    print("datasets written to ./datasets")
