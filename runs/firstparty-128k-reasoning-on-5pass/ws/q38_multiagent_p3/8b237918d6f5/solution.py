import sys
from collections import deque


class Dinic:
    def __init__(self, n):
        self.n = n
        self.g = [[] for _ in range(n)]

    def add_edge(self, fr, to, cap):
        fwd = [to, len(self.g[to]), cap]
        rev = [fr, len(self.g[fr]), 0]
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
                    if e[2] > 0 and level[e[0]] < 0:
                        level[e[0]] = level[v] + 1
                        q.append(e[0])

            if level[t] < 0:
                break

            it = [0] * n

            def dfs(v, f):
                if v == t:
                    return f
                i = it[v]
                while i < len(g[v]):
                    e = g[v][i]
                    if e[2] > 0 and level[e[0]] == level[v] + 1:
                        d = dfs(e[0], f if f < e[2] else e[2])
                        if d:
                            e[2] -= d
                            g[e[0]][e[1]][2] += d
                            return d
                    i += 1
                    it[v] = i
                return 0

            while flow < limit:
                f = dfs(s, limit - flow)
                if not f:
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

    idx = 3
    for _ in range(M):
        u = data[idx] - 1
        v = data[idx + 1] - 1
        idx += 2
        edges.append((u, v))
        adj[u].append(v)

    dist = [-1] * N
    dist[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        if u == N - 1:
            break
        for v in adj[u]:
            if dist[v] < 0:
                dist[v] = dist[u] + 1
                q.append(v)

    L = dist[N - 1]
    INF = K + 1
    LIMIT = K + 1

    def feasible(D):
        if D == 0:
            return True

        total = N * D + 2
        S = N * D
        T = S + 1
        dinic = Dinic(total)

        for i in range(D):
            dinic.add_edge(S, (N - 1) * D + i, INF)
            dinic.add_edge(i, T, INF)

        for u, v in edges:
            base_u = u * D
            base_v = v * D
            for i in range(D - 1):
                dinic.add_edge(base_v + i + 1, base_u + i, INF)
            for i in range(D):
                dinic.add_edge(base_v + i, base_u + i, 1)

        for v in range(N):
            base = v * D
            for i in range(D - 1):
                dinic.add_edge(base + i + 1, base + i, INF)

        return dinic.max_flow(S, T, LIMIT) <= K

    lo, hi = 0, min(L, K)
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1

    print(ans)


if __name__ == "__main__":
    sys.setrecursionlimit(1000000)
    solve()