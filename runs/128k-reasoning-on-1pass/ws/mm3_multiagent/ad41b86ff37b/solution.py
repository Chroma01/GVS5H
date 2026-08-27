import sys

def solve() -> None:
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    n = int(next(it))

    adj = [[] for _ in range(n + 1)]
    for _ in range(n - 1):
        u = int(next(it))
        v = int(next(it))
        adj[u].append(v)
        adj[v].append(u)

    # degree of each vertex in the original tree
    deg = [0] * (n + 1)
    for v in range(1, n + 1):
        deg[v] = len(adj[v])

    max_total = 0  # maximum number of vertices that can stay in a snowflake

    for r in range(1, n + 1):
        # neighbours of r that can become blue vertices (must have degree >= 2)
        cand = [deg[nb] for nb in adj[r] if deg[nb] >= 2]
        if not cand:
            continue  # r cannot be the red vertex
        cand.sort(reverse=True)

        best = 0
        # i = number of chosen blue vertices (1‑based)
        for i, d in enumerate(cand, start=1):
            val = i * d  # i * minimal degree among the i chosen neighbours
            if val > best:
                best = val
        size_r = 1 + best  # Lemma 1: 1 (red) + |B| * min_deg
        if size_r > max_total:
            max_total = size_r

    answer = n - max_total
    sys.stdout.write(str(answer))

if __name__ == "__main__":
    solve()