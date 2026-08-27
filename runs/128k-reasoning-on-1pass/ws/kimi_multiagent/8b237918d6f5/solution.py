import sys
from collections import deque

def solve():
    data = sys.stdin.buffer.read().split()
    it = iter(data)
    N = int(next(it)); M = int(next(it)); K = int(next(it))
    edges = [(int(next(it)), int(next(it))) for _ in range(M)]

    sys.setrecursionlimit(1 << 20)

    class Dinic:
        __slots__ = ('n', 'g', 'level', 'ptr')
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]
        def add(self, fr, to, cap):
            self.g[fr].append([to, cap, len(self.g[to])])
            self.g[to].append([fr, 0, len(self.g[fr]) - 1])
        def bfs(self, s, t):
            self.level = [-1] * self.n
            self.level[s] = 0
            q = deque([s])
            g, level = self.g, self.level
            while q:
                v = q.popleft()
                lv = level[v] + 1
                for to, cap, _ in g[v]:
                    if cap > 0 and level[to] < 0:
                        level[to] = lv
                        q.append(to)
            return level[t] >= 0
        def dfs(self, v, t, f):
            if v == t:
                return f
            g, level, ptr = self.g, self.level, self.ptr
            while ptr[v] < len(g[v]):
                e = g[v][ptr[v]]
                to, cap, rev = e
                if cap > 0 and level[to] == level[v] + 1:
                    d = self.dfs(to, t, f if f < cap else cap)
                    if d > 0:
                        e[1] -= d
                        g[to][rev][1] += d
                        return d
                ptr[v] += 1
            return 0
        def maxflow(self, s, t):
            flow = 0
            INF = 1 << 60
            while self.bfs(s, t):
                self.ptr = [0] * self.n
                while True:
                    f = self.dfs(s, t, INF)
                    if f == 0:
                        break
                    flow += f
            return flow

    INF = M + 1  # any constraint-respecting cut costs <= M, so M+1 acts as infinity

    def feasible(D):
        # Can we choose <= K edges of weight 1 so dist(1, N) >= D?
        # Equivalent to potentials p[v] in {0..D}, p[1]=0, p[N]=D,
        # p[v] <= p[u]+1 per edge u->v, with <= K edges having p[v] = p[u]+1.
        # Minimizing that count is an s-t min cut on threshold nodes x[v][i] = [p[v] >= i].
        if D == 0:
            return True
        s, t = 0, 1
        din = Dinic(N * D + 2)
        def nid(v, i):  # node for "p[v] >= i", i in 1..D
            return 2 + (v - 1) * D + (i - 1)
        # monotonicity: x[v][i+1] => x[v][i]
        for v in range(1, N + 1):
            for i in range(1, D):
                din.add(nid(v, i + 1), nid(v, i), INF)
        # fix p[1] = 0 and p[N] = D
        for i in range(1, D + 1):
            din.add(nid(1, i), t, INF)
            din.add(s, nid(N, i), INF)
        for (u, v) in edges:
            # unit cost: charged iff x[v][i]=1 and x[u][i]=0, i.e. p[v] > p[u]
            for i in range(1, D + 1):
                din.add(nid(v, i), nid(u, i), 1)
            # Lipschitz p[v] <= p[u]+1: x[v][i+1] => x[u][i]
            for i in range(1, D):
                din.add(nid(v, i + 1), nid(u, i), INF)
        return din.maxflow(s, t) <= K

    lo, hi = 0, min(K, N - 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

solve()