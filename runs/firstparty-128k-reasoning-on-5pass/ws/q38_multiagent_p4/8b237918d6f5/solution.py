import sys
from collections import deque

sys.setrecursionlimit(1_000_000)


class Edge:
    __slots__ = ("to", "cap", "rev")

    def __init__(self, to, cap, rev):
        self.to = to
        self.cap = cap
        self.rev = rev


class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.level = [0] * n
        self.it = [0] * n

    def add_edge(self, fr, to, cap):
        self.graph[fr].append(Edge(to, cap, len(self.graph[to])))
        self.graph[to].append(Edge(fr, 0, len(self.graph[fr]) - 1))

    def bfs(self, s, t):
        self.level = [-1] * self.n
        self.level[s] = 0
        q = deque([s])

        while q:
            v = q.popleft()
            for e in self.graph[v]:
                if e.cap > 0 and self.level[e.to] < 0:
                    self.level[e.to] = self.level[v] + 1
                    q.append(e.to)

        return self.level[t] >= 0

    def dfs(self, v, t, f):
        if v == t:
            return f

        while self.it[v] < len(self.graph[v]):
            e = self.graph[v][self.it[v]]
            if e.cap > 0 and self.level[e.to] == self.level[v] + 1:
                d = self.dfs(e.to, t, min(f, e.cap))
                if d > 0:
                    e.cap -= d
                    self.graph[e.to][e.rev].cap += d
                    return d
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

    def feasible(d):
        if d == 0:
            return True

        total_nodes = 2 + N * d
        dinic = Dinic(total_nodes)
        source = 0
        sink = 1
        INF = 10**9

        def idx(v, i):
            return 2 + v * d + (i - 1)

        for i in range(1, d + 1):
            dinic.add_edge(source, idx(N - 1, i), INF)
            dinic.add_edge(idx(0, i), sink, INF)

        for v in range(N):
            for i in range(1, d):
                dinic.add_edge(idx(v, i + 1), idx(v, i), INF)

        for u, v in edges:
            for j in range(1, d + 1):
                dinic.add_edge(idx(v, j), idx(u, j), 1)

            for j in range(2, d + 1):
                dinic.add_edge(idx(v, j), idx(u, j - 1), INF)

        return dinic.max_flow(source, sink, K + 1) <= K

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