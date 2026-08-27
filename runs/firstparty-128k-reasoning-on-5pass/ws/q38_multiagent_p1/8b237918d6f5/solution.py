import sys
from collections import deque


class Edge:
    __slots__ = ("to", "rev", "cap")

    def __init__(self, to, rev, cap):
        self.to = to
        self.rev = rev
        self.cap = cap


def add_edge(g, fr, to, cap):
    f = Edge(to, len(g[to]), cap)
    r = Edge(fr, len(g[fr]), 0)
    g[fr].append(f)
    g[to].append(r)


def max_flow(g, s, t, limit):
    n = len(g)
    flow = 0
    level = [-1] * n
    it = [0] * n

    def bfs():
        for i in range(n):
            level[i] = -1
        level[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            for e in g[v]:
                if e.cap > 0 and level[e.to] < 0:
                    level[e.to] = level[v] + 1
                    q.append(e.to)
        return level[t] >= 0

    def dfs(v, f):
        if v == t:
            return f
        while it[v] < len(g[v]):
            e = g[v][it[v]]
            if e.cap > 0 and level[e.to] == level[v] + 1:
                d = dfs(e.to, f if f < e.cap else e.cap)
                if d:
                    e.cap -= d
                    g[e.to][e.rev].cap += d
                    return d
            it[v] += 1
        return 0

    while flow < limit and bfs():
        for i in range(n):
            it[i] = 0
        while flow < limit:
            f = dfs(s, limit - flow)
            if f == 0:
                break
            flow += f
    return flow


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, K = data[0], data[1], data[2]
    edges = []
    adj = [[] for _ in range(N)]

    p = 3
    for _ in range(M):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        edges.append((u, v))
        adj[u].append(v)

    # Unweighted shortest path length from 1 to N is a safe upper bound.
    dist = [-1] * N
    dist[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    L = dist[N - 1]
    if L == -1:
        print(0)
        return

    hi = min(K, N - 1, L)
    sys.setrecursionlimit(1000000)

    def feasible(D):
        if D == 0:
            return True

        total = 2 + N * D
        s = 0
        t = 1
        g = [[] for _ in range(total)]
        INF = K + 1

        def idx(v, i):
            # v is 0-based, i is 1..D
            return 2 + v * D + (i - 1)

        # Chain edges enforce threshold monotonicity:
        # if label >= i+1 then label >= i.
        for v in range(N):
            base = 2 + v * D
            for i in range(1, D):
                add_edge(g, base + i, base + i - 1, INF)

        # Force vertex N to label D and vertex 1 to label 0.
        for i in range(1, D + 1):
            add_edge(g, s, idx(N - 1, i), INF)
            add_edge(g, idx(0, i), t, INF)

        # For each original directed edge u -> v:
        # unit edges charge one when label(v) = label(u) + 1,
        # infinite edges forbid label(v) >= label(u) + 2.
        for u, v in edges:
            for i in range(1, D + 1):
                add_edge(g, idx(v, i), idx(u, i), 1)
            for i in range(2, D + 1):
                add_edge(g, idx(v, i), idx(u, i - 1), INF)

        flow = max_flow(g, s, t, K + 1)
        return flow <= K

    lo = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)


if __name__ == "__main__":
    main()