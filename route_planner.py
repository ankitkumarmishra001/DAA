"""Delivery route planning: distance matrix (via Dijkstra) + Nearest-Neighbor TSP."""
from graph import dijkstra, build_path


def build_distance_matrix(graph, nodes):
    """Run Dijkstra from every node in `nodes`.

    Returns (dist, prevs):
        dist[a][b]  - shortest road distance a -> b
        prevs[a]    - prev map of the Dijkstra run from a (to rebuild real road paths)
    """
    dist, prevs = {}, {}
    for a in nodes:
        d, p = dijkstra(graph, a)
        dist[a] = {b: d[b] for b in nodes}
        prevs[a] = p
    return dist, prevs


def nearest_neighbor_route(dist, depot, stops):
    """Nearest-Neighbor approximation for the Travelling Salesman Problem.

    Start at the depot, always go to the closest unvisited stop, finally return.
    Time : O(k^2) for k stops.  NOT guaranteed optimal (TSP is NP-hard).
    Returns (route, total_length).
    """
    unvisited = set(stops)
    route = [depot]
    current, total = depot, 0
    while unvisited:
        nxt = min(unvisited, key=lambda s: (dist[current][s], s))   # name breaks ties
        total += dist[current][nxt]
        route.append(nxt)
        unvisited.remove(nxt)
        current = nxt
    total += dist[current][depot]
    route.append(depot)
    return route, total


def expand_route(route, prevs):
    """Turn the stop sequence into the full list of road nodes actually driven."""
    full = [route[0]]
    for a, b in zip(route, route[1:]):
        full.extend(build_path(prevs[a], a, b)[1:])
    return full
