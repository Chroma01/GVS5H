import sys
from collections import deque

sys.setrecursionlimit(1000000)


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.level = []
        self.it = []

    def add_edge(self, fr, to, cap):
        if fr == to:
            return
        self.g[fr].append([to, len(self.g[to]), cap])
        self.g[to].append([fr, len(self.g[fr]) - 1, 0])

    def bfs(self, s, t):
        level = [-1] * self.n
        level[s] = 0
        q = deque([s])
        g = self.g
        while q:
            v = q.popleft()
            for e in g[v]:
                if e[2] > 0 and level[e[0]] < 0:
                    level[e[0]] = level[v] + 1
                    q.append(e[0])
        self.level = level
        return level[t] >= 0

    def dfs(self, v, t, f):
        if v == t:
            return f
        g = self.g
        level = self.level
        it = self.it
        while it[v] < len(g[v]):
            e = g[v][it[v]]
            if e[2] > 0 and level[e[0]] == level[v] + 1:
                d = self.dfs(e[0], t, min(f, e[2]))
                if d:
                    e[2] -= d
                    g[e[0]][e[1]][2] += d
                    return d
            it[v] += 1
        return 0

    def max_flow(self, s, t, limit=10**18):
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
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))

    edges = []
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        edges.append((u, v))

    maxD = min(K, N - 1)
    INF = 10**9

    def feasible(D):
        if D == 0:
            return True

        total = N * D
        s = total
        t = total + 1
        dinic = Dinic(total + 2)

        def node(v, i):
            return v * D + i

        # Force d_1 = 0 and d_N = D.
        for v in range(N):
            for i in range(D):
                nid = node(v, i)
                if v == 0:
                    dinic.add_edge(nid, t, INF)
                if v == N - 1:
                    dinic.add_edge(s, nid, INF)

        # Monotonicity: x_{v,i+1} => x_{v,i}.
        for v in range(N):
            for i in range(D - 1):
                dinic.add_edge(node(v, i + 1), node(v, i), INF)

        # Transition constraints and costs.
        for u, v in edges:
            # x_{v,i+1} => x_{u,i}, enforcing d_v <= d_u + 1.
            for i in range(D - 1):
                dinic.add_edge(node(v, i + 1), node(u, i), INF)

            # Cost 1 when x_{v,i} is true and x_{u,i} is false.
            for i in range(D):
                dinic.add_edge(node(v, i), node(u, i), 1)

        return dinic.max_flow(s, t, K + 1) <= K

    lo, hi = 0, maxD + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    solve()