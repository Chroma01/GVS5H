import sys
from collections import deque


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        self.g[fr].append([to, cap, len(self.g[to])])
        self.g[to].append([fr, 0, len(self.g[fr]) - 1])

    def max_flow(self, s, t, limit=None):
        flow = 0
        n = self.n

        while limit is None or flow < limit:
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

            def dfs(v, f):
                if v == t:
                    return f
                while it[v] < len(self.g[v]):
                    e = self.g[v][it[v]]
                    to, cap, rev = e
                    if cap > 0 and level[v] + 1 == level[to]:
                        pushed = dfs(to, min(f, cap))
                        if pushed:
                            e[1] -= pushed
                            self.g[to][rev][1] += pushed
                            return pushed
                    it[v] += 1
                return 0

            while limit is None or flow < limit:
                pushed = dfs(s, (limit - flow) if limit is not None else 10**18)
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

        variable_count = n * d
        source = variable_count
        sink = variable_count + 1
        dinic = Dinic(variable_count + 2)

        inf = m + 1

        def node(v, level):
            return v * d + level

        # Enforce d_v >= i+2 => d_v >= i+1.
        for v in range(n):
            for i in range(d - 1):
                dinic.add_edge(node(v, i + 1), node(v, i), inf)

        # For every original edge u -> v:
        # d_v >= i+2 implies d_u >= i+1.
        for u, v in edges:
            for i in range(d - 1):
                dinic.add_edge(node(v, i + 1), node(u, i), inf)

        # A finite cut edge counts an original edge crossing upward
        # at the corresponding level.
        for u, v in edges:
            for i in range(d):
                dinic.add_edge(node(v, i), node(u, i), 1)

        # d_1 = 0: all positive-level variables of vertex 1 are false.
        for i in range(d):
            dinic.add_edge(node(0, i), sink, inf)

        # d_N >= d: all level variables of vertex N are true.
        for i in range(d):
            dinic.add_edge(source, node(n - 1, i), inf)

        return dinic.max_flow(source, sink, k + 1) <= k

    low, high = 0, n
    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    main()