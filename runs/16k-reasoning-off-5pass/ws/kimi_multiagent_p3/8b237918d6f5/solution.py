import sys
from collections import deque

def main():
    data = sys.stdin.read().split()
    idx = 0
    N = int(data[idx]); idx += 1
    M = int(data[idx]); idx += 1
    K = int(data[idx]); idx += 1
    edges = []
    for _ in range(M):
        u = int(data[idx]); idx += 1
        v = int(data[idx]); idx += 1
        edges.append((u, v))

    # BFS layers from vertex 1 (unweighted, directed)
    INF = float('inf')
    dist = [INF] * (N + 1)
    dist[1] = 0
    adj = [[] for _ in range(N + 1)]
    for u, v in edges:
        adj[u].append(v)
    q = deque([1])
    while q:
        u = q.popleft()
        for v in adj[u]:
            if dist[v] == INF:
                dist[v] = dist[u] + 1
                q.append(v)

    D = dist[N]  # guaranteed reachable

    # Dinic max flow on forward edges (dist[v] == dist[u] + 1), unit capacities.
    # F = max number of edge-disjoint 1->N paths in the layered DAG.
    class Dinic:
        __slots__ = ('n', 'graph', 'level', 'it')
        def __init__(self, n):
            self.n = n
            self.graph = [[] for _ in range(n + 1)]  # edge: [to, cap, rev_index]

        def add_edge(self, fr, to, cap):
            self.graph[fr].append([to, cap, len(self.graph[to])])
            self.graph[to].append([fr, 0, len(self.graph[fr]) - 1])

        def bfs(self, s, t):
            self.level = [-1] * (self.n + 1)
            self.level[s] = 0
            dq = deque([s])
            while dq:
                u = dq.popleft()
                for e in self.graph[u]:
                    if e[1] > 0 and self.level[e[0]] < 0:
                        self.level[e[0]] = self.level[u] + 1
                        dq.append(e[0])
            return self.level[t] >= 0

        def dfs(self, u, t, f):
            if u == t:
                return f
            while self.it[u] < len(self.graph[u]):
                e = self.graph[u][self.it[u]]
                if e[1] > 0 and self.level[e[0]] == self.level[u] + 1:
                    d = self.dfs(e[0], t, min(f, e[1]))
                    if d > 0:
                        e[1] -= d
                        self.graph[e[0]][e[2]][1] += d
                        return d
                self.it[u] += 1
            return 0

        def max_flow(self, s, t):
            flow = 0
            while self.bfs(s, t):
                self.it = [0] * (self.n + 1)
                while True:
                    f = self.dfs(s, t, float('inf'))
                    if f == 0:
                        break
                    flow += f
            return flow

    dinic = Dinic(N)
    for u, v in edges:
        if dist[u] != INF and dist[v] == dist[u] + 1:
            dinic.add_edge(u, v, 1)

    F = dinic.max_flow(1, N)

    # Answer = min(D, floor(K / F))
    # Upper bound: F edge-disjoint length-D paths => some path gets <= K/F flips;
    # distance <= D always. Achievable: s-t path clutter is Mengerian, so d*F
    # forward edges suffice to hit every path >= d times; d*F <= K <= #forward edges.
    print(min(D, K // F))

main()