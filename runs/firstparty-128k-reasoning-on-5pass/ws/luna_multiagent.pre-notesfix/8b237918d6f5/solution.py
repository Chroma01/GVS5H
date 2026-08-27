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
                    edge = self.g[v][it[v]]
                    to, cap, rev = edge

                    if cap > 0 and level[to] == level[v] + 1:
                        amount = dfs(to, min(pushed, cap))
                        if amount:
                            edge[1] -= amount
                            self.g[to][rev][1] += amount
                            return amount

                    it[v] += 1

                return 0

            while flow < limit:
                pushed = dfs(s, limit - flow)
                if pushed == 0:
                    break
                flow += pushed

        return flow


def main():
    input = sys.stdin.buffer.readline
    n, m, k = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]

    def feasible(d):
        if d == 0:
            return True

        variable_count = n * d
        source = variable_count
        sink = variable_count + 1
        dinic = Dinic(variable_count + 2)

        inf = m + 1

        def node(v, level):
            return (v - 1) * d + (level - 1)

        # Threshold monotonicity:
        # x[v][i+1] => x[v][i]
        for v in range(1, n + 1):
            for level in range(1, d):
                dinic.add_edge(node(v, level + 1), node(v, level), inf)

        # Fix d_1 = 0 and d_N = d.
        for level in range(1, d + 1):
            dinic.add_edge(node(1, level), sink, inf)
            dinic.add_edge(source, node(n, level), inf)

        for u, v in edges:
            # Constraint d_v - d_u <= 1:
            # x[v][i] => x[u][i-1], for i >= 2.
            for level in range(2, d + 1):
                dinic.add_edge(node(v, level), node(u, level - 1), inf)

            # Cost for a one-level rise:
            # x[v][i] = 1 and x[u][i] = 0.
            for level in range(1, d + 1):
                dinic.add_edge(node(v, level), node(u, level), 1)

        return dinic.max_flow(source, sink, k + 1) <= k

    low = 0
    high = n  # Distance n is impossible when all edges have weight at most 1.

    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    main()