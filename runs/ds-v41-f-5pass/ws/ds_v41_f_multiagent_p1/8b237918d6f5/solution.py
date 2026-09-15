import sys
from collections import deque

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    edges = []
    for _ in range(M):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        edges.append((u, v))

    INF = M + 1                       # > K and > any finite cut (|S| <= M)
    sys.setrecursionlimit(1 << 20)

    class Dinic:
        __slots__ = ('n', 'g', 'level', 'it')
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]
            self.level = [0] * n
            self.it = [0] * n

        def add_edge(self, u, v, c):
            self.g[u].append([v, c, len(self.g[v])])
            self.g[v].append([u, 0, len(self.g[u]) - 1])

        def bfs(self, s, t):
            level = [-1] * self.n
            level[s] = 0
            q = deque([s])
            g = self.g
            while q:
                u = q.popleft()
                lu = level[u]
                for e in g[u]:
                    if e[1] > 0 and level[e[0]] < 0:
                        level[e[0]] = lu + 1
                        q.append(e[0])
            self.level = level
            return level[t] >= 0

        def dfs(self, u, t, f):
            if u == t:
                return f
            g = self.g; level = self.level; it = self.it
            while it[u] < len(g[u]):
                e = g[u][it[u]]
                if e[1] > 0 and level[e[0]] == level[u] + 1:
                    d = self.dfs(e[0], t, f if f < e[1] else e[1])
                    if d > 0:
                        e[1] -= d
                        g[e[0]][e[2]][1] += d
                        return d
                it[u] += 1
            return 0

        def maxflow_limited(self, s, t, limit):
            flow = 0
            while flow <= limit and self.bfs(s, t):
                self.it = [0] * self.n
                while flow <= limit:
                    f = self.dfs(s, t, 1 << 60)
                    if f == 0:
                        break
                    flow += f
            return flow

    def feasible(d):
        # Can we mark <= K edges so every 1->N path has >= d marked edges?
        if d == 0:
            return True
        total = N * d
        S = total; T = total + 1
        din = Dinic(total + 2)

        def node(v, k):              # k in 1..d, y_{v,k} = [L(v) >= k]
            return v * d + (k - 1)

        for k in range(1, d + 1):
            din.add_edge(S, node(N - 1, k), INF)   # force L(N) = d
            din.add_edge(node(0, k), T, INF)       # force L(1) = 0
        for v in range(N):
            for k in range(1, d):
                din.add_edge(node(v, k + 1), node(v, k), INF)   # monotone

        for (u, v) in edges:
            for k in range(1, d + 1):
                din.add_edge(node(v, k), node(u, k), 1)         # cost of a step up
            for k in range(2, d + 1):
                din.add_edge(node(v, k), node(u, k - 1), INF)   # L(v) <= L(u)+1

        return din.maxflow_limited(S, T, K) <= K

    ans = 0
    for d in range(1, N):            # shortest path is simple -> <= N-1 edges
        if feasible(d):
            ans = d
        else:
            break                    # feasibility is downward-closed in d
    print(ans)

main()