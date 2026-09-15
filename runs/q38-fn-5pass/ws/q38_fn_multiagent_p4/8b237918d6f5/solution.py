import sys
from collections import deque

sys.setrecursionlimit(1_000_000)


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        if cap <= 0:
            return
        fwd = [to, cap, len(self.g[to])]
        rev = [fr, 0, len(self.g[fr])]
        self.g[fr].append(fwd)
        self.g[to].append(rev)

    def max_flow(self, s, t, limit):
        flow = 0
        n = self.n
        g = self.g

        while flow < limit:
            level = [-1] * n
            level[s] = 0
            q = deque([s])

            while q:
                v = q.popleft()
                for e in g[v]:
                    if e[1] > 0 and level[e[0]] < 0:
                        level[e[0]] = level[v] + 1
                        q.append(e[0])

            if level[t] < 0:
                break

            it = [0] * n

            def dfs(v, f):
                if v == t:
                    return f

                while it[v] < len(g[v]):
                    e = g[v][it[v]]
                    if e[1] > 0 and level[e[0]] == level[v] + 1:
                        ret = dfs(e[0], f if f < e[1] else e[1])
                        if ret:
                            e[1] -= ret
                            g[e[0]][e[2]][1] += ret
                            return ret
                    it[v] += 1

                return 0

            while flow < limit:
                pushed = dfs(s, limit - flow)
                if pushed == 0:
                    break
                flow += pushed

        return flow


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, K = data[0], data[1], data[2]
    edges = []
    adj = [[] for _ in range(N)]

    p = 3
    for _ in range(M):
        u = data[p] - 1
        v = data[p + 1] - 1
        p += 2
        edges.append((u, v))
        adj[u].append(v)

    # Unweighted shortest path length from 1 to N.
    dist = [-1] * N
    dist[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                q.append(v)

    L = dist[N - 1]
    hi = min(K, L)

    if hi <= 0:
        print(0)
        return

    INF = K + 1

    def feasible(D):
        if D == 0:
            return True

        # Node (v, level) is represented by v * D + (level - 1),
        # where level is 1..D and means h(v) >= level.
        V = N * D
        s = V
        t = V + 1
        dinic = Dinic(V + 2)

        # Source side means True.
        # h(N) = D: all (N, level) must be True.
        nbase = (N - 1) * D
        for i in range(D):
            dinic.add_edge(s, nbase + i, INF)

        # h(1) = 0: all (1, level) must be False.
        for i in range(D):
            dinic.add_edge(i, t, INF)

        # Monotonicity: h(v) >= level+1 => h(v) >= level.
        for v in range(N):
            base = v * D
            for i in range(D - 1):
                dinic.add_edge(base + i + 1, base + i, INF)

        for u, v in edges:
            ubase = u * D
            vbase = v * D

            # Count original edge u->v when h(v) = h(u) + 1.
            # This is h(v) >= level and h(u) < level.
            for i in range(D):
                dinic.add_edge(vbase + i, ubase + i, 1)

            # Constraint h(v) <= h(u) + 1:
            # h(v) >= level => h(u) >= level-1, for level >= 2.
            for i in range(1, D):
                dinic.add_edge(vbase + i, ubase + i - 1, INF)

        return dinic.max_flow(s, t, K + 1) <= K

    lo = 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    print(lo)


if __name__ == "__main__":
    solve()