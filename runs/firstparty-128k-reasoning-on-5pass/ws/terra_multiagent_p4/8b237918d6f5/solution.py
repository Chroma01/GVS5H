import sys
from collections import deque


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        fwd = [to, cap, None]
        rev = [fr, 0, None]
        fwd[2] = len(self.g[to])
        rev[2] = len(self.g[fr])
        self.g[fr].append(fwd)
        self.g[to].append(rev)

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
                    to, cap, rev_idx = e
                    if cap > 0 and level[v] < level[to]:
                        got = dfs(to, min(f, cap))
                        if got:
                            e[1] -= got
                            self.g[to][rev_idx][1] += got
                            return got
                    it[v] += 1
                return 0

            while True:
                pushed = dfs(s, 10**18)
                if pushed == 0:
                    break
                flow += pushed


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, m, k = data[:3]
    edges = []
    pos = 3
    for _ in range(m):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        edges.append((u, v))

    INF = 10**9

    def feasible(d):
        # Node (v, i) represents x[v][i] = [p(v) >= i], for 1 <= i <= d.
        count = n * d
        source = count
        sink = count + 1
        mf = Dinic(count + 2)

        def node(v, i):
            return v * d + (i - 1)

        # Labels must be monotone: x[v][i+1] => x[v][i].
        for v in range(n):
            for i in range(1, d):
                mf.add_edge(node(v, i + 1), node(v, i), INF)

        # Fix p(1) = 0 and p(N) = d.
        for i in range(1, d + 1):
            mf.add_edge(node(0, i), sink, INF)
            mf.add_edge(source, node(n - 1, i), INF)

        for u, v in edges:
            # Enforce p(v) <= p(u) + 1:
            # x[v][i] => x[u][i-1] for i >= 2.
            for i in range(2, d + 1):
                mf.add_edge(node(v, i), node(u, i - 1), INF)

            # This cut edge is paid exactly when x[v][i]=1 and x[u][i]=0.
            # Under the above constraint, at most one such threshold exists,
            # exactly when p(v) > p(u).
            for i in range(1, d + 1):
                mf.add_edge(node(v, i), node(u, i), 1)

        return mf.max_flow(source, sink) <= k

    lo, hi = 0, n - 1
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)


if __name__ == "__main__":
    main()