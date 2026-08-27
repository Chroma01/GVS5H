import sys
from collections import deque

sys.setrecursionlimit(1_000_000)


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        self.g[fr].append([to, cap, len(self.g[to])])
        self.g[to].append([fr, 0, len(self.g[fr]) - 1])

    def max_flow(self, s, t, limit):
        flow = 0

        while flow < limit:
            level = [-1] * self.n
            level[s] = 0
            q = deque([s])

            while q:
                v = q.popleft()
                for to, cap, _ in self.g[v]:
                    if cap > 0 and level[to] == -1:
                        level[to] = level[v] + 1
                        q.append(to)

            if level[t] == -1:
                break

            it = [0] * self.n

            def dfs(v, f):
                if v == t:
                    return f

                while it[v] < len(self.g[v]):
                    e = self.g[v][it[v]]
                    to, cap, rev = e

                    if cap > 0 and level[v] < level[to]:
                        pushed = dfs(to, min(f, cap))
                        if pushed:
                            e[1] -= pushed
                            self.g[to][rev][1] += pushed
                            return pushed

                    it[v] += 1

                return 0

            while flow < limit:
                pushed = dfs(s, limit - flow)
                if pushed == 0:
                    break
                flow += pushed

        return flow


def solve():
    input = sys.stdin.readline
    n, m, k = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))

    def feasible(d):
        if d == 0:
            return True

        # Node (v, i) represents X[v, i] = (label[v] >= i), 1 <= i <= d.
        def node(v, i):
            return (i - 1) * n + v

        var_count = n * d
        source = var_count
        sink = var_count + 1
        inf = m + 1

        dinic = Dinic(var_count + 2)

        # X[v, i+1] => X[v, i].
        for v in range(n):
            for i in range(1, d):
                dinic.add_edge(node(v, i + 1), node(v, i), inf)

        for u, v in edges:
            # label[v] <= label[u] + 1.
            for i in range(2, d + 1):
                dinic.add_edge(node(v, i), node(u, i - 1), inf)

            # Cost one precisely when this edge raises the label by one.
            for i in range(1, d + 1):
                dinic.add_edge(node(v, i), node(u, i), 1)

        # label[0] = 0.
        for i in range(1, d + 1):
            dinic.add_edge(node(0, i), sink, inf)

        # label[n - 1] = d.
        for i in range(1, d + 1):
            dinic.add_edge(source, node(n - 1, i), inf)

        return dinic.max_flow(source, sink, k + 1) <= k

    lo, hi = 0, k + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    solve()