import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it)); M = int(next(it)); K = int(next(it))
    edges = [(int(next(it)) - 1, int(next(it)) - 1) for _ in range(M)]

    # ---------- Dinic ----------
    class Dinic:
        __slots__ = ('n', 'g', 'level', 'it')
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]
        def add(self, fr, to, cap):
            f = [to, cap, None]
            b = [fr, 0, f]
            f[2] = b
            self.g[fr].append(f)
            self.g[to].append(b)
        def bfs(self, s, t):
            level = [-1] * self.n
            q = deque([s])
            level[s] = 0
            while q:
                v = q.popleft()
                for e in self.g[v]:
                    if e[1] > 0 and level[e[0]] < 0:
                        level[e[0]] = level[v] + 1
                        q.append(e[0])
            self.level = level
            return level[t] >= 0
        def dfs(self, v, t, f):
            if v == t:
                return f
            for i in range(self.it[v], len(self.g[v])):
                self.it[v] = i
                e = self.g[v][i]
                if e[1] > 0 and self.level[v] < self.level[e[0]]:
                    d = self.dfs(e[0], t, min(f, e[1]))
                    if d > 0:
                        e[1] -= d
                        e[2][1] += d
                        return d
            return 0
        def flow(self, s, t, limit):
            res = 0
            while res < limit and self.bfs(s, t):
                self.it = [0] * self.n
                while res < limit:
                    f = self.dfs(s, t, limit - res)
                    if f == 0:
                        break
                    res += f
            return res

    INF = K + 1  # any cut value > K is "infeasible"; cap flow at K+1

    def ok(D):
        # Can we choose <= K edges so every 1->N path uses >= D chosen edges?
        if D == 0:
            return True
        # Layered graph: node (v, i), i in 0..D-1
        # id = v * D + i ; plus sink
        nn = N * D
        S = 0 * D + 0          # (vertex 1, layer 0)
        T = nn
        din = Dinic(nn + 1)
        for i in range(D):
            din.add((N - 1) * D + i, T, INF)
        for (u, v) in edges:
            for i in range(D):
                # not choosing this edge: stay in same layer; cutting costs 1 (= choose it)
                din.add(u * D + i, v * D + i, 1)
                # choosing it: move up a layer (free, uncuttable)
                if i + 1 < D:
                    din.add(u * D + i, v * D + i + 1, INF)
        return din.flow(S, T, INF) <= K

    lo, hi = 0, M  # answer in [0, M]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if ok(mid):
            lo = mid
        else:
            hi = mid - 1
    print(lo)

solve()