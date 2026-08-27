import sys
from collections import deque

def solve():
    input = sys.stdin.readline
    N, M, K = map(int, input().split())
    edges = []
    for _ in range(M):
        u, v = map(int, input().split())
        edges.append((u-1, v-1))  # 0-indexed

    # Dinic's max flow
    class Dinic:
        def __init__(self, N):
            self.N = N
            self.graph = [[] for _ in range(N)]

        def add_edge(self, fr, to, cap):
            forward = [to, cap, None]
            backward = [fr, 0, forward]
            forward[2] = backward
            self.graph[fr].append(forward)
            self.graph[to].append(backward)

        def bfs_level(self, s, t):
            level = [-1] * self.N
            q = deque([s])
            level[s] = 0
            while q:
                v = q.popleft()
                for e in self.graph[v]:
                    if e[1] > 0 and level[e[0]] < 0:
                        level[e[0]] = level[v] + 1
                        q.append(e[0])
            self.level = level
            return level[t] >= 0

        def dfs_flow(self, v, t, f):
            if v == t:
                return f
            for i in range(self.it[v], len(self.graph[v])):
                e = self.graph[v][i]
                if e[1] > 0 and self.level[v] < self.level[e[0]]:
                    ret = self.dfs_flow(e[0], t, min(f, e[1]))
                    if ret > 0:
                        e[1] -= ret
                        e[2][1] += ret
                        return ret
                self.it[v] += 1
            return 0

        def max_flow(self, s, t):
            flow = 0
            INF = 10**9
            while self.bfs_level(s, t):
                self.it = [0] * self.N
                while True:
                    f = self.dfs_flow(s, t, INF)
                    if f == 0:
                        break
                    flow += f
            return flow

    # Check if we can achieve shortest distance >= d
    def can(d):
        if d == 0:
            return True
        # Build layered graph with d+1 layers (0..d)
        num_layers = d + 1
        V = num_layers * N
        source = 0  # (0, 0)
        sink = (N-1) * num_layers + d  # (N-1, d)
        dinic = Dinic(V)
        INF = M + 1  # capacity for 0-edges (always present)
        for u, v in edges:
            # 0-edges: within same layer (always present)
            for i in range(num_layers):
                dinic.add_edge(u * num_layers + i, v * num_layers + i, INF)
            # 1-edges: to next layer (these can be "removed" to disconnect)
            for i in range(d):
                dinic.add_edge(u * num_layers + i, v * num_layers + i + 1, 1)
        # Compute min cut (max flow) between source and sink
        min_cut = dinic.max_flow(source, sink)
        # We need to remove at most M-K 1-edges to disconnect
        # i.e., min_cut <= M - K
        return min_cut <= M - K

    # Binary search on the answer
    lo, hi = 0, K
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if can(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)

solve()