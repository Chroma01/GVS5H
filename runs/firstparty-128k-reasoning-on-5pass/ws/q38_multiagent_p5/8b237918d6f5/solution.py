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
        if fr == to:
            return
        self.g[fr].append([to, cap, len(self.g[to])])
        self.g[to].append([fr, 0, len(self.g[fr]) - 1])

    def bfs(self, s, t):
        level = [-1] * self.n
        level[s] = 0
        q = deque([s])
        g = self.g
        while q:
            v = q.popleft()
            for to, cap, rev in g[v]:
                if cap > 0 and level[to] < 0:
                    level[to] = level[v] + 1
                    q.append(to)
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
            if e[1] > 0 and level[v] + 1 == level[e[0]]:
                d = self.dfs(e[0], t, f if f < e[1] else e[1])
                if d:
                    e[1] -= d
                    g[e[0]][e[2]][1] += d
                    return d
            it[v] += 1
        return 0

    def max_flow(self, s, t, limit):
        flow = 0
        while flow < limit and self.bfs(s, t):
            self.it = [0] * self.n
            while flow < limit:
                f = self.dfs(s, t, limit - flow)
                if not f:
                    break
                flow += f
        return flow


def main():
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

    def feasible(D):
        if D == 0:
            return True

        V = N * D
        s = V
        t = V + 1
        dinic = Dinic(V + 2)
        INF = K + 1

        def idx(v, i):
            return v * D + i

        for i in range(D):
            dinic.add_edge(s, idx(N - 1, i), INF)
            dinic.add_edge(idx(0, i), t, INF)

        for v in range(N):
            for i in range(1, D):
                dinic.add_edge(idx(v, i), idx(v, i - 1), INF)

        for u, v in edges:
            for i in range(D):
                dinic.add_edge(idx(v, i), idx(u, i), 1)
            for i in range(1, D):
                dinic.add_edge(idx(v, i), idx(u, i - 1), INF)

        return dinic.max_flow(s, t, K + 1) <= K

    low = 0
    high = min(K, N - 1)

    while low < high:
        mid = (low + high + 1) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid - 1

    print(low)


if __name__ == "__main__":
    main()