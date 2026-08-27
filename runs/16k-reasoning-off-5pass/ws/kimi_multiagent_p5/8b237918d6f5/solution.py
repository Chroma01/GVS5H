import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    edges = []
    for _ in range(M):
        u = int(data[idx]) - 1; idx += 1
        v = int(data[idx]) - 1; idx += 1
        edges.append((u, v))

    INF = 10**9

    class Dinic:
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]

        def add_edge(self, fr, to, cap):
            self.g[fr].append([to, cap, len(self.g[to])])
            self.g[to].append([fr, 0, len(self.g[fr]) - 1])

        def bfs(self, s, t):
            self.level = [-1] * self.n
            q = deque([s])
            self.level[s] = 0
            while q:
                v = q.popleft()
                for to, cap, rev in self.g[v]:
                    if cap > 0 and self.level[to] < 0:
                        self.level[to] = self.level[v] + 1
                        q.append(to)
            return self.level[t] >= 0

        def dfs(self, v, t, f):
            if v == t:
                return f
            while self.it[v] < len(self.g[v]):
                e = self.g[v][self.it[v]]
                to, cap, rev = e
                if cap > 0 and self.level[v] + 1 == self.level[to]:
                    d = self.dfs(to, t, min(f, cap))
                    if d > 0:
                        e[1] -= d
                        self.g[to][rev][1] += d
                        return d
                self.it[v] += 1
            return 0

        def max_flow(self, s, t):
            flow = 0
            while self.bfs(s, t):
                self.it = [0] * self.n
                while True:
                    f = self.dfs(s, t, INF)
                    if f == 0:
                        break
                    flow += f
            return flow

    def min_cut(D):
        # Minimum number of edges to set to weight 1 so that every 1->N path
        # uses at least D weighted edges (i.e., shortest distance >= D).
        # Layers 0..D-1 represent "weighted edges used so far" (< D).
        # Free arcs stay in the same layer; unit arcs advance a layer and
        # correspond to choosing that edge to be weight 1.
        # Sink is reachable from (N, i) for any layer i < D via INF arcs,
        # so any path reaching N with < D weighted edges gives an INF-capacity
        # s-t connection unless cut by unit arcs.
        if D == 0:
            return 0
        L = D  # layers 0..D-1
        t = N * L
        din = Dinic(N * L + 1)
        for (u, v) in edges:
            for i in range(D - 1):
                din.add_edge(u * L + i, v * L + i + 1, 1)   # weight this edge
            for i in range(D):
                din.add_edge(u * L + i, v * L + i, INF)     # free traversal
        for i in range(D):
            din.add_edge((N - 1) * L + i, t, INF)
        s = 0  # (vertex 1, layer 0)
        return din.max_flow(s, t)

    # Binary search the largest D in [0, M] with min_cut(D) <= K.
    # Monotonicity: feasible(D) implies feasible(D-1).
    ans = 0
    lo, hi = 0, M
    while lo <= hi:
        mid = (lo + hi) // 2
        if min_cut(mid) <= K:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)

solve()