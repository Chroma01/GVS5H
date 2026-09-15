import sys
from collections import deque

sys.setrecursionlimit(1000000)


class Dinic:
    __slots__ = ("n", "g", "level", "it")

    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.level = []
        self.it = []

    def add_edge(self, fr, to, cap):
        if fr == to:
            fwd = [to, cap, len(self.g[to]) + 1]
            rev = [fr, 0, len(self.g[fr])]
            self.g[fr].append(fwd)
            self.g[to].append(rev)
        else:
            fwd = [to, cap, len(self.g[to])]
            rev = [fr, 0, len(self.g[fr])]
            self.g[fr].append(fwd)
            self.g[to].append(rev)

    def bfs(self, s, t):
        level = [-1] * self.n
        level[s] = 0
        q = deque([s])
        g = self.g

        while q:
            v = q.popleft()
            for e in g[v]:
                if e[1] > 0 and level[e[0]] < 0:
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
            if e[1] > 0 and level[e[0]] == level[v] + 1:
                ret = self.dfs(e[0], t, f if f < e[1] else e[1])
                if ret:
                    e[1] -= ret
                    g[e[0]][e[2]][1] += ret
                    return ret
            it[v] += 1

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

    p = 3
    for _ in range(M):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        edges.append((u, v))
        adj[u].append(v)

    dist = [-1] * N
    dist[0] = 0
    q = deque([0])

    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    if dist[N - 1] == -1:
        print(0)
        return

    upper = min(K, dist[N - 1])
    INF = 10 ** 9

    def feasible(D):
        if D == 0:
            return True

        total = N * D
        s = total
        t = total + 1
        dinic = Dinic(total + 2)
        add = dinic.add_edge

        for v in range(N):
            base = v * D

            if v == 0:
                for i in range(D):
                    add(base + i, t, INF)

            if v == N - 1:
                for i in range(D):
                    add(s, base + i, INF)

            for i in range(1, D):
                add(base + i, base + i - 1, INF)

        for u, v in edges:
            bu = u * D
            bv = v * D

            for i in range(1, D):
                add(bv + i, bu + i - 1, INF)

            for i in range(D):
                add(bv + i, bu + i, 1)

        return dinic.max_flow(s, t, K + 1) <= K

    for D in range(upper, -1, -1):
        if feasible(D):
            print(D)
            return


if __name__ == "__main__":
    solve()