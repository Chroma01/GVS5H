import sys
from collections import deque

sys.setrecursionlimit(1_000_000)


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, u, v, cap):
        self.g[u].append([v, len(self.g[v]), cap])
        self.g[v].append([u, len(self.g[u]) - 1, 0])

    def max_flow(self, s, t):
        flow = 0
        INF = 10**9

        while True:
            level = [-1] * self.n
            level[s] = 0
            q = deque([s])
            while q:
                u = q.popleft()
                for v, rev, cap in self.g[u]:
                    if cap > 0 and level[v] < 0:
                        level[v] = level[u] + 1
                        q.append(v)

            if level[t] < 0:
                return flow

            it = [0] * self.n

            def dfs(u, pushed):
                if u == t:
                    return pushed
                while it[u] < len(self.g[u]):
                    e = self.g[u][it[u]]
                    v, rev, cap = e
                    if cap > 0 and level[v] == level[u] + 1:
                        got = dfs(v, min(pushed, cap))
                        if got:
                            e[2] -= got
                            self.g[v][rev][2] += got
                            return got
                    it[u] += 1
                return 0

            while True:
                pushed = dfs(s, INF)
                if pushed == 0:
                    break
                flow += pushed


def feasible(target, n, edges, k):
    if target == 0:
        return True

    layer_count = n * target
    source = layer_count
    sink = source + 1
    dinic = Dinic(sink + 1)
    INF = 10**9

    def node(v, level):
        return (v - 1) * target + (level - 1)

    # If d_v >= i+1, then d_v >= i.
    for v in range(1, n + 1):
        for i in range(1, target):
            dinic.add_edge(node(v, i + 1), node(v, i), INF)

    # Force d_1 = 0.
    for i in range(1, target + 1):
        dinic.add_edge(node(1, i), sink, INF)

    # Force d_N >= target.
    dinic.add_edge(source, node(n, target), INF)

    # For every original edge u -> v:
    # d_v >= i and d_u < i incurs cost 1.
    # Also enforce d_v <= d_u + 1.
    for u, v in edges:
        for i in range(1, target + 1):
            dinic.add_edge(node(v, i), node(u, i), 1)
        for i in range(1, target):
            dinic.add_edge(node(v, i + 1), node(u, i), INF)

    return dinic.max_flow(source, sink) <= k


def main():
    input = sys.stdin.readline
    n, m, k = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]

    low, high = 0, n
    while high - low > 1:
        mid = (low + high) // 2
        if feasible(mid, n, edges, k):
            low = mid
        else:
            high = mid

    print(low)


if __name__ == "__main__":
    main()