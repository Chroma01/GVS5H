import sys
from collections import deque

sys.setrecursionlimit(1000000)


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]
        self.level = []
        self.it = []

    def add_edge(self, fr, to, cap):
        if fr == to:
            fwd_index = len(self.g[fr])
            rev_index = fwd_index + 1
            self.g[fr].append([to, cap, rev_index])
            self.g[fr].append([fr, 0, fwd_index])
        else:
            fwd = [to, cap, len(self.g[to])]
            rev = [fr, 0, len(self.g[fr])]
            self.g[fr].append(fwd)
            self.g[to].append(rev)

    def bfs(self, s, t):
        level = [-1] * self.n
        level[s] = 0
        q = deque([s])
        g = self.g
        while q:
            v = q.popleft()
            for to, cap, rev in g[v]:
                if cap > 0 and level[to] < 0:
                    level[to] = level[v] + 1
                    q.append(to)
        self.level = level
        return level[t] >= 0

    def dfs(self, v, t, f):
        if v == t:
            return f
        g = self.g
        level = self.level
        it = self.it
        while it[v] < len(g[v]):
            e = g[v][it[v]]
            to, cap, rev = e
            if cap > 0 and level[to] == level[v] + 1:
                ret = self.dfs(to, t, f if f < cap else cap)
                if ret:
                    e[1] -= ret
                    g[to][rev][1] += ret
                    return ret
            it[v] += 1
        return 0

    def max_flow(self, s, t, limit):
        flow = 0
        while flow < limit and self.bfs(s, t):
            self.it = [0] * self.n
            while flow < limit:
                f = self.dfs(s, t, limit - flow)
                if f == 0:
                    break
                flow += f
        return flow


def solve():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    N, M, K = data[0], data[1], data[2]
    edges = []
    adj = [[] for _ in range(N)]

    pos = 3
    for _ in range(M):
        u = data[pos] - 1
        v = data[pos + 1] - 1
        pos += 2
        edges.append((u, v))
        adj[u].append(v)

    # Unweighted shortest path length from 1 to N.
    dist = [-1] * N
    dist[0] = 0
    q = deque([0])
    while q:
        v = q.popleft()
        for to in adj[v]:
            if dist[to] < 0:
                dist[to] = dist[v] + 1
                q.append(to)

    L = dist[N - 1]
    if L < 0:
        print(0)
        return

    upper = min(K, L)

    def feasible(D):
        if D == 0:
            return True

        V = N * D + 2
        s = N * D
        t = s + 1
        dinic = Dinic(V)
        INF = K + 1

        # Monotonicity: x_{v,i} => x_{v,i-1}
        for v in range(N):
            base = v * D
            for i in range(2, D + 1):
                dinic.add_edge(base + i - 1, base + i - 2, INF)

        for u, v in edges:
            ub = u * D
            vb = v * D

            # Edge constraint: p_v <= p_u + 1
            # x_{v,i} => x_{u,i-1}
            for i in range(2, D + 1):
                dinic.add_edge(vb + i - 1, ub + i - 2, INF)

            # Cost: charge once when p_v = p_u + 1
            for i in range(1, D + 1):
                dinic.add_edge(vb + i - 1, ub + i - 1, 1)

        # Force p_1 = 0 and p_N = D
        last_base = (N - 1) * D
        for i in range(1, D + 1):
            dinic.add_edge(i - 1, t, INF)
            dinic.add_edge(s, last_base + i - 1, INF)

        return dinic.max_flow(s, t, K + 1) <= K

    lo = 0
    hi = upper + 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid

    print(lo)


if __name__ == "__main__":
    solve()