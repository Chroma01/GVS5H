import sys
from collections import deque


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

        while flow < limit:
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
                    ei = it[v]
                    to, cap, rev = self.g[v][ei]
                    if cap > 0 and level[v] < level[to]:
                        got = dfs(to, min(f, cap))
                        if got:
                            self.g[v][ei][1] -= got
                            self.g[to][rev][1] += got
                            return got
                    it[v] += 1
                return 0

            while flow < limit:
                pushed = dfs(s, limit - flow)
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

        # Threshold node (v, i) means label[v] >= i, for 1 <= i <= d.
        def node(v, i):
            return v * d + (i - 1)

        source = n * d
        sink = source + 1
        dinic = Dinic(sink + 1)
        inf = m + 1

        # Fix label[0] = 0 and label[n-1] = d.
        for i in range(1, d + 1):
            dinic.add_edge(node(0, i), sink, inf)
            dinic.add_edge(source, node(n - 1, i), inf)

        # A higher threshold implies every lower threshold.
        for v in range(n):
            for i in range(1, d):
                dinic.add_edge(node(v, i + 1), node(v, i), inf)

        for u, v in edges:
            # Enforce label[v] <= label[u] + 1:
            # label[v] >= i implies label[u] >= i-1.
            for i in range(2, d + 1):
                dinic.add_edge(node(v, i), node(u, i - 1), inf)

            # Cost one iff label[v] = label[u] + 1.
            # Under the preceding constraint, this is the only possible
            # strictly increasing difference. This arc crosses the cut then.
            for i in range(1, d + 1):
                dinic.add_edge(node(v, i), node(u, i), 1)

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
    main()