import sys
from collections import deque

sys.setrecursionlimit(100000)


def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    edges = []
    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        edges.append((u, v))

    INF = K + 1  # > K, so any cut using an "infinite" edge exceeds K

    class Dinic:
        def __init__(self, n):
            self.n = n
            self.g = [[] for _ in range(n)]

        def add_edge(self, fr, to, cap):
            self.g[fr].append([to, cap, len(self.g[to])])
            self.g[to].append([fr, 0, len(self.g[fr]) - 1])

        def bfs(self, s, t):
            self.level = [-1] * self.n
            self.level[s] = 0
            q = deque([s])
            while q:
                v = q.popleft()
                lv = self.level[v] + 1
                for to, cap, rev in self.g[v]:
                    if cap > 0 and self.level[to] < 0:
                        self.level[to] = lv
                        q.append(to)
            return self.level[t] >= 0

        def dfs(self, v, t, f):
            if v == t:
                return f
            g = self.g
            level = self.level
            it = self.it
            while it[v] < len(g[v]):
                e = g[v][it[v]]
                to = e[0]
                cap = e[1]
                if cap > 0 and level[v] < level[to]:
                    d = self.dfs(to, t, f if f < cap else cap)
                    if d:
                        e[1] -= d
                        g[to][e[2]][1] += d
                        return d
                it[v] += 1
            return 0

        def max_flow(self, s, t):
            flow = 0
            while self.bfs(s, t):
                self.it = [0] * self.n
                while True:
                    f = self.dfs(s, t, float('inf'))
                    if not f:
                        break
                    flow += f
            return flow

    def feasible(d):
        # d == 0 : labelling h(v)=0 works, cost 0 <= K, always feasible
        if d == 0:
            return True
        D = d
        # node (v,i) -> index (v-1)*D + (i-1);  meaning (v,i) in S <=> h(v) < i
        total = N * D
        S = total
        T = total + 1
        din = Dinic(total + 2)

        # force h(1) = 0 and h(N) = d
        din.add_edge(S, (1 - 1) * D + (1 - 1), INF)
        din.add_edge((N - 1) * D + (D - 1), T, INF)

        # chain: (v,i) -> (v,i+1) forbids h(v)<i and h(v)>=i+1
        for v in range(1, N + 1):
            base = (v - 1) * D
            for i in range(1, D):
                din.add_edge(base + (i - 1), base + i, INF)

        for (u, v) in edges:
            ub = (u - 1) * D
            vb = (v - 1) * D
            # enforce h(v) <= h(u)+1 : (u,i-1)->(v,i) INF
            for i in range(2, D + 1):
                din.add_edge(ub + (i - 2), vb + (i - 1), INF)
            # cost 1 iff h(v)=h(u)+1 : edge (u,i)->(v,i) cap 1
            for i in range(1, D + 1):
                din.add_edge(ub + (i - 1), vb + (i - 1), 1)

        return din.max_flow(S, T) <= K

    for d in range(N - 1, -1, -1):
        if feasible(d):
            print(d)
            return


main()