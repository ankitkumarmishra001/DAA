"""Weighted undirected graph (adjacency list) + Dijkstra's algorithm."""
import heapq
import json
import random

INF = float("inf")


class Graph:
    def __init__(self, depot="D"):
        self.adj = {}          # {"D": {"C1": 4, "C2": 7}, "C1": {"D": 4}, ...}
        self.depot = depot

    def add_edge(self, u, v, w):
        self.adj.setdefault(u, {})[v] = w
        self.adj.setdefault(v, {})[u] = w

    def nodes(self):
        return list(self.adj)

    def edge_count(self):
        return sum(len(nb) for nb in self.adj.values()) // 2

    def save(self, path):
        edges = [[u, v, w] for u in self.adj for v, w in self.adj[u].items() if u < v]
        with open(path, "w") as f:
            json.dump({"depot": self.depot, "edges": edges}, f)

    @staticmethod
    def load(path):
        with open(path) as f:
            data = json.load(f)
        g = Graph(data.get("depot", "D"))
        for u, v, w in data["edges"]:
            g.add_edge(u, v, w)
        return g


def dijkstra(graph, source):
    """Single-source shortest paths using a min-heap (priority queue).

    Works only for NON-NEGATIVE edge weights (distances are never negative).
    Time : O((V + E) log V)
    Returns (dist, prev): dist[node] = shortest distance, prev[node] = parent on that path.
    """
    dist = {node: INF for node in graph.adj}
    prev = {}
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:                # stale entry, a shorter path was already found
            continue
        for v, w in graph.adj[u].items():
            nd = d + w
            if nd < dist[v]:
                dist[v] = nd
                prev[v] = u
                heapq.heappush(heap, (nd, v))
    return dist, prev


def build_path(prev, source, target):
    """Rebuild the node sequence source -> target from the prev map."""
    path = [target]
    while path[-1] != source:
        path.append(prev[path[-1]])
    return path[::-1]


def generate_random_graph(num_customers, seed=42, max_w=20, extra_factor=2):
    """Connected random graph: depot D + customers C1..Cn.

    First a random spanning tree (guarantees connectivity), then extra random edges.
    """
    rng = random.Random(seed)
    names = ["D"] + [f"C{i}" for i in range(1, num_customers + 1)]
    g = Graph("D")
    for i in range(1, len(names)):
        g.add_edge(names[i], names[rng.randrange(i)], rng.randint(1, max_w))
    for _ in range(extra_factor * num_customers):
        u, v = rng.sample(names, 2)
        if v not in g.adj[u]:
            g.add_edge(u, v, rng.randint(1, max_w))
    return g
