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
        n = self.n

        while flow <= limit:
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
                break

            it = [0] * n

            def dfs(v, f):
                if v == t:
                    return f
                while it[v] < len(self.g[v]):
                    e = self.g[v][it[v]]
                    to, cap, rev = e
                    if cap > 0 and level[v] < level[to]:
                        ret = dfs(to, min(f, cap))
                        if ret:
                            e[1] -= ret
                            self.g[to][rev][1] += ret
                            return ret
                    it[v] += 1
                return 0

            while flow <= limit:
                pushed = dfs(s, limit + 1 - flow)
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

    INF = m + 1

    def feasible(d):
        # Node (v, i), where 1 <= i <= d, means label[v] >= i.
        def node(v, i):
            return v * d + (i - 1)

        source = n * d
        sink = source + 1
        dinic = Dinic(sink + 1)

        # Threshold variables for a vertex must be downward-closed.
        for v in range(n):
            for i in range(2, d + 1):
                dinic.add_edge(node(v, i), node(v, i - 1), INF)

        # label[v] <= label[u] + 1 for every original edge u -> v.
        # A cut arc from (v,i) to (u,i-1) forbids v >= i and u < i-1.
        for u, v in edges:
            for i in range(2, d + 1):
                dinic.add_edge(node(v, i), node(u, i - 1), INF)

            # Cost 1 iff label[v] >= i and label[u] < i.
            # Under the implication constraints, this happens for at most one i.
            for i in range(1, d + 1):
                dinic.add_edge(node(v, i), node(u, i), 1)

        # Force label[0] = 0: every threshold node is on the sink side.
        for i in range(1, d + 1):
            dinic.add_edge(node(0, i), sink, INF)

        # Force label[n-1] = d: every threshold node is on the source side.
        for i in range(1, d + 1):
            dinic.add_edge(source, node(n - 1, i), INF)

        return dinic.max_flow(source, sink, k) <= k

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