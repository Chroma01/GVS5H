import sys
from collections import deque

sys.setrecursionlimit(1_000_000)


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.level = []
        self.it = []

    def add_edge(self, fr, to, cap):
        fwd = [to, len(self.g[to]), cap]
        rev = [fr, len(self.g[fr]), 0]
        self.g[fr].append(fwd)
        self.g[to].append(rev)

    def bfs(self, s, t):
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            for to, rev, cap in self.g[v]:
                if cap > 0 and self.level[to] < 0:
                    self.level[to] = self.level[v] + 1
                    q.append(to)
        return self.level[t] >= 0

    def dfs(self, v, t, f):
        if v == t:
            return f
        while self.it[v] < len(self.g[v]):
            e = self.g[v][self.it[v]]
            to = e[0]
            if e[2] > 0 and self.level[v] + 1 == self.level[to]:
                ret = self.dfs(to, t, f if f < e[2] else e[2])
                if ret:
                    e[2] -= ret
                    self.g[to][e[1]][2] += ret
                    return ret
            self.it[v] += 1
        return 0

    def max_flow(self, s, t, limit):
        flow = 0
        while flow < limit and self.bfs(s, t):
            self.it = [0] * self.n
            while flow < limit:
                f = self.dfs(s, t, limit - flow)
                if f == 0:
                    break
                flow += f
        return flow


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, K = data[0], data[1], data[2]
    edges = []
    adj = [[] for _ in range(N)]

    idx = 3
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        edges.append((u, v))
        adj[u].append(v)

    # Upper bound: the original unweighted shortest path length.
    dist = [-1] * N
    dist[0] = 0
    q = deque([0])
    while q:
        v = q.popleft()
        for to in adj[v]:
            if dist[to] == -1:
                dist[to] = dist[v] + 1
                q.append(to)

    if dist[N - 1] == -1:
        print(0)
        return

    upper = min(K, dist[N - 1])
    INF = 10**9

    def check(d):
        if d == 0:
            return True

        # Nodes (v, i), 1 <= i <= d, are represented by v*d + (i-1).
        V = N * d + 2
        s = N * d
        t = s + 1
        dinic = Dinic(V)

        def node(v, i):
            return v * d + (i - 1)

        # Force vertex 1 to have level 0 and vertex N to have level d.
        for i in range(1, d + 1):
            dinic.add_edge(s, node(N - 1, i), INF)
            dinic.add_edge(node(0, i), t, INF)

        # Nesting: level(v) >= i implies level(v) >= i-1.
        for v in range(N):
            for i in range(2, d + 1):
                dinic.add_edge(node(v, i), node(v, i - 1), INF)

        # For each original edge u -> v:
        # level(v) >= i implies level(u) >= i-1.
        # Also, unit cost when level(v) >= i > level(u).
        for u, v in edges:
            for i in range(2, d + 1):
                dinic.add_edge(node(v, i), node(u, i - 1), INF)
            for i in range(1, d + 1):
                dinic.add_edge(node(v, i), node(u, i), 1)

        return dinic.max_flow(s, t, K + 1) <= K

    lo, hi = 0, upper + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    solve()