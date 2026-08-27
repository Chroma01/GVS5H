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
        self.g[fr].append([to, len(self.g[to]), cap])
        self.g[to].append([fr, len(self.g[fr]) - 1, 0])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])
        while q:
            v = q.popleft()
            for e in self.g[v]:
                if e[2] > 0 and self.level[e[0]] == -1:
                    self.level[e[0]] = self.level[v] + 1
                    q.append(e[0])
        return self.level[t] != -1

    def dfs(self, v, t, f):
        if v == t:
            return f
        for i in range(self.it[v], len(self.g[v])):
            self.it[v] = i
            e = self.g[v][i]
            if e[2] > 0 and self.level[v] + 1 == self.level[e[0]]:
                d = self.dfs(e[0], t, min(f, e[2]))
                if d:
                    e[2] -= d
                    self.g[e[0]][e[1]][2] += d
                    return d
        self.it[v] = len(self.g[v])
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


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, K = data[0], data[1], data[2]
    edges = []
    p = 3
    for _ in range(M):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        edges.append((u, v))

    def feasible(D):
        if D == 0:
            return True

        total = N * D
        S = total
        T = total + 1
        dinic = Dinic(total + 2)
        INF = 10 ** 9

        def idx(v, i):
            return v * D + (i - 1)

        add = dinic.add_edge

        for i in range(1, D + 1):
            add(S, idx(N - 1, i), INF)
            add(idx(0, i), T, INF)

        for v in range(N):
            for i in range(2, D + 1):
                add(idx(v, i), idx(v, i - 1), INF)

        for u, v in edges:
            for i in range(1, D + 1):
                add(idx(v, i), idx(u, i), 1)
            for i in range(2, D + 1):
                add(idx(v, i), idx(u, i - 1), INF)

        return dinic.max_flow(S, T, K + 1) <= K

    lo = 0
    hi = min(N - 1, K) + 1
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    main()