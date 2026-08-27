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
        INF_FLOW = 10**18

        while True:
            level = [-1] * self.n
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

            it = [0] * self.n

            def dfs(v, f):
                if v == t:
                    return f

                while it[v] < len(self.g[v]):
                    i = it[v]
                    to, cap, rev = self.g[v][i]

                    if cap > 0 and level[v] + 1 == level[to]:
                        pushed = dfs(to, min(f, cap))
                        if pushed:
                            self.g[v][i][1] -= pushed
                            self.g[to][rev][1] += pushed
                            return pushed

                    it[v] += 1

                return 0

            while True:
                pushed = dfs(s, INF_FLOW)
                if pushed == 0:
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

        source = n * d
        sink = source + 1
        dinic = Dinic(sink + 1)
        inf = k + 1

        def node(v, level):
            return v * d + level - 1

        # Force x_1 = 0 and x_N >= d.
        for level in range(1, d + 1):
            dinic.add_edge(node(0, level), sink, inf)
            dinic.add_edge(source, node(n - 1, level), inf)

        # Label consistency:
        # y[v][level] => y[v][level - 1].
        for v in range(n):
            for level in range(2, d + 1):
                dinic.add_edge(node(v, level), node(v, level - 1), inf)

        for u, v in edges:
            # Difference constraint x_v <= x_u + 1:
            # y[v][level] => y[u][level - 1].
            for level in range(2, d + 1):
                dinic.add_edge(node(v, level), node(u, level - 1), inf)

            # Charge one unit exactly when x_v = x_u + 1.
            for level in range(1, d + 1):
                dinic.add_edge(node(v, level), node(u, level), 1)

        return dinic.max_flow(source, sink) <= k

    # A simple path has at most n-1 edges, so distance n is impossible.
    low, high = 0, min(n, k + 1)

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    main()