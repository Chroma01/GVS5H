import sys
from collections import deque

class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        self.g[fr].append([to, len(self.g[to]), cap])
        self.g[to].append([fr, len(self.g[fr]) - 1, 0])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        q = deque([s])
        self.level[s] = 0
        while q:
            v = q.popleft()
            for e in self.g[v]:
                if e[2] > 0 and self.level[e[0]] < 0:
                    self.level[e[0]] = self.level[v] + 1
                    q.append(e[0])
        return self.level[t] >= 0

    def dfs(self, v, t, f):
        if v == t:
            return f
        while self.it[v] < len(self.g[v]):
            e = self.g[v][self.it[v]]
            to, rev, cap = e
            if cap > 0 and self.level[v] + 1 == self.level[to]:
                d = self.dfs(to, t, min(f, cap))
                if d > 0:
                    e[2] -= d
                    self.g[to][rev][2] += d
                    return d
            self.it[v] += 1
        return 0

    def max_flow(self, s, t):
        flow = 0
        INF_FLOW = 10**18
        while self.bfs(s, t):
            self.it = [0] * self.n
            while True:
                f = self.dfs(s, t, INF_FLOW)
                if f == 0:
                    break
                flow += f
        return flow


def solve():
    sys.setrecursionlimit(1000000)
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    K = int(data[2])
    edges = []
    idx = 3
    for _ in range(M):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        edges.append((u, v))

    INF = 10**9

    for D in range(N - 1, -1, -1):
        if D == 0:
            print(0)
            return

        V = 2 + N * D
        S0 = 0
        T0 = 1

        def node(v, i):
            return 2 + (v - 1) * D + (i - 1)

        dinic = Dinic(V)

        # Force t(N) = D  <=>  x_{N,i} = 1 for all i
        for i in range(1, D + 1):
            dinic.add_edge(S0, node(N, i), INF)

        # Force t(1) = 0  <=>  x_{1,i} = 0 for all i
        for i in range(1, D + 1):
            dinic.add_edge(node(1, i), T0, INF)

        # Monotonicity: x_{v,i+1} => x_{v,i}
        for v in range(1, N + 1):
            for i in range(1, D):
                dinic.add_edge(node(v, i + 1), node(v, i), INF)

        # Edge constraints and costs
        for u, v in edges:
            # t(v) <= t(u) + 1  <=>  for i>=2, x_{v,i} => x_{u,i-1}
            for i in range(2, D + 1):
                dinic.add_edge(node(v, i), node(u, i - 1), INF)
            # cost 1 if t(v) = t(u) + 1
            for i in range(1, D + 1):
                dinic.add_edge(node(v, i), node(u, i), 1)

        flow = dinic.max_flow(S0, T0)
        if flow <= K:
            print(D)
            return

    print(0)


if __name__ == "__main__":
    solve()