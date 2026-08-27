import sys
from collections import deque


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        self.g[fr].append([to, cap, len(self.g[to])])
        self.g[to].append([fr, 0, len(self.g[fr]) - 1])

    def max_flow(self, s, t):
        flow = 0
        n = self.n

        while True:
            level = [-1] * n
            level[s] = 0
            q = deque([s])

            while q:
                v = q.popleft()
                for to, cap, _ in self.g[v]:
                    if cap > 0 and level[to] < 0:
                        level[to] = level[v] + 1
                        q.append(to)

            if level[t] < 0:
                return flow

            it = [0] * n

            def dfs(v, f):
                if v == t:
                    return f

                while it[v] < len(self.g[v]):
                    e = self.g[v][it[v]]
                    to, cap, rev = e

                    if cap > 0 and level[v] < level[to]:
                        got = dfs(to, min(f, cap))
                        if got:
                            e[1] -= got
                            self.g[to][rev][1] += got
                            return got

                    it[v] += 1

                return 0

            while True:
                pushed = dfs(s, 10**18)
                if pushed == 0:
                    break
                flow += pushed


def solve():
    input = sys.stdin.readline
    n, m, k = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))

    INF = m + 1

    def feasible(d):
        if d == 0:
            return True

        # Node (v, i) represents y[v][i] = [x[v] >= i], for 1 <= i <= d.
        # Source side means y=1, sink side means y=0.
        source = n * d
        sink = source + 1
        dinic = Dinic(sink + 1)

        def node(v, i):
            return v * d + (i - 1)

        for v in range(n):
            # x_v >= i+1 implies x_v >= i.
            for i in range(1, d):
                dinic.add_edge(node(v, i + 1), node(v, i), INF)

        for u, v in edges:
            # Constraint x_v <= x_u + 1:
            # x_v >= i implies x_u >= i-1, for i >= 2.
            for i in range(2, d + 1):
                dinic.add_edge(node(v, i), node(u, i - 1), INF)

            # Cut cost is sum_i [x_v >= i and x_u < i] = max(x_v-x_u, 0).
            # Under the above constraint, this is exactly 1 iff x_v=x_u+1.
            for i in range(1, d + 1):
                dinic.add_edge(node(v, i), node(u, i), 1)

        # x_1 = 0: every threshold variable must be 0.
        for i in range(1, d + 1):
            dinic.add_edge(node(0, i), sink, INF)

        # x_N = d: every threshold variable must be 1.
        for i in range(1, d + 1):
            dinic.add_edge(source, node(n - 1, i), INF)

        return dinic.max_flow(source, sink) <= k

    lo, hi = 0, n
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    solve()