import sys
from collections import deque


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        self.g[u].append([v, cap, len(self.g[v])])
        self.g[v].append([u, 0, len(self.g[u]) - 1])

    def max_flow(self, s, t, limit):
        flow = 0
        n = self.n

        while flow < limit:
            level = [-1] * n
            level[s] = 0
            q = deque([s])
            while q:
                v = q.popleft()
                for to, cap, rev in self.g[v]:
                    if cap > 0 and level[to] < 0:
                        level[to] = level[v] + 1
                        q.append(to)

            if level[t] < 0:
                break

            it = [0] * n

            def dfs(v, pushed):
                if v == t:
                    return pushed
                while it[v] < len(self.g[v]):
                    e = self.g[v][it[v]]
                    to, cap, rev = e
                    if cap > 0 and level[to] == level[v] + 1:
                        got = dfs(to, min(pushed, cap))
                        if got:
                            e[1] -= got
                            self.g[to][rev][1] += got
                            return got
                    it[v] += 1
                return 0

            while flow < limit:
                pushed = dfs(s, limit - flow)
                if not pushed:
                    break
                flow += pushed

        return flow


def main():
    input = sys.stdin.readline
    n, m, k = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v = map(int, input().split())
        edges.append((u - 1, v - 1))

    def feasible(d):
        if d == 0:
            return True

        # Node (v, i) means x_v >= i, for 1 <= i <= d.
        layers = n * d
        source = layers
        sink = layers + 1
        dinic = Dinic(layers + 2)
        inf = k + 1

        def node(v, i):
            return v * d + (i - 1)

        # Enforce x_v >= i+1 => x_v >= i.
        for v in range(n):
            for i in range(1, d):
                dinic.add_edge(node(v, i + 1), node(v, i), inf)

        # For every original edge u -> v:
        # x_v >= i+1 => x_u >= i, expressing x_v <= x_u + 1.
        # Also charge a unit when x_u < i <= x_v.
        for u, v in edges:
            for i in range(1, d):
                dinic.add_edge(node(v, i + 1), node(u, i), inf)
            for i in range(1, d + 1):
                dinic.add_edge(node(v, i), node(u, i), 1)

        # x_1 = 0: all threshold variables of vertex 1 are false.
        for i in range(1, d + 1):
            dinic.add_edge(node(0, i), sink, inf)

        # x_N >= d: all threshold variables of vertex N are true.
        for i in range(1, d + 1):
            dinic.add_edge(source, node(n - 1, i), inf)

        return dinic.max_flow(source, sink, k + 1) <= k

    lo, hi = 0, n
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    main()