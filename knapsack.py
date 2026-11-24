"""0/1 Knapsack using Dynamic Programming (bottom-up).

table[i][c] = best total value using only the first i parcels with capacity c.
    table[i][c] = table[i-1][c]                                  (skip parcel i)
    table[i][c] = max(that, table[i-1][c-w_i] + v_i)  if w_i<=c  (take parcel i)

Time : O(n * W)      Space: O(n * W)  (full table kept so we can trace back)
"""


def knapsack(weights, values, capacity):
    """Return (best_value, chosen_indices, table)."""
    n = len(weights)
    table = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w, v = weights[i - 1], values[i - 1]
        prev, cur = table[i - 1], table[i]
        for c in range(capacity + 1):
            cur[c] = prev[c]                       # option 1: skip
            if w <= c and prev[c - w] + v > cur[c]:
                cur[c] = prev[c - w] + v           # option 2: take

    # trace back to find WHICH parcels were taken
    chosen = []
    c = capacity
    for i in range(n, 0, -1):
        if table[i][c] != table[i - 1][c]:
            chosen.append(i - 1)
            c -= weights[i - 1]
    chosen.reverse()
    return table[n][capacity], chosen, table


def format_table(table, weights, labels, step=1):
    """Pretty-print the DP table (columns = capacity 0..W, every `step`)."""
    cols = list(range(0, len(table[0]), step))
    lines = ["cap       " + "".join(f"{c:>4}" for c in cols)]
    for i, row in enumerate(table):
        name = "none" if i == 0 else f"{labels[i-1]}(w{weights[i-1]})"
        lines.append(f"{name:<10}" + "".join(f"{row[c]:>4}" for c in cols))
    return "\n".join(lines)
