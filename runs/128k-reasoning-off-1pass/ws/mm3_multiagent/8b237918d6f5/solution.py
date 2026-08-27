import sys
from collections import deque

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    M = int(next(it))
    K = int(next(it))
    edges = []
    adj = [[] for _ in range(N)]
    for _ in range(M):
        u = int(next(it)) - 1
        v = int(next(it)) - 1
        edges.append((u, v))
        adj[u].append(v)
    
    # BFS to find unweighted shortest path length L from 0 to N-1
    INF = 10**9
    dist = [INF] * N
    dist[0] = 0
    q = deque([0])
    while q:
        u = q.popleft()
        if u == N - 1:
            break
        for v in adj[u]:
            if dist[v] == INF:
                dist[v] = dist[u] + 1
                q.append(v)
    L = dist[N-1]
    if L == INF:
        # Should not happen as per constraints
        print(0)
        return
    
    # Dinic's max flow
    class Dinic:
        def __init__(self, n):
            self.n = n
            self.adj = [[] for _ in range(n)]
        def add_edge(self, u, v, c):
            self.adj[u].append([v, c, len(self.adj[v])])
            self.adj[v].append([u, 0, len(self.adj[u]) - 1])
        def bfs(self, s, t):
            self.level = [-1] * self.n
            q = deque([s])
            self.level[s] = 0
            while q:
                u = q.popleft()
                for e in self.adj[u]:
                    v, cap, rev = e
                    if cap > 0 and self.level[v] == -1:
                        self.level[v] = self.level[u] + 1
                        q.append(v)
            return self.level[t] != -1
        def dfs(self, u, t, f):
            if u == t:
                return f
            for i in range(self.it[u], len(self.adj[u])):
                self.it[u] = i
                e = self.adj[u][i]
                v, cap, rev = e
                if cap > 0 and self.level[v] == self.level[u] + 1:
                    ret = self.dfs(v, t, min(f, cap))
                    if ret > 0:
                        e[1] -= ret
                        self.adj[v][rev][1] += ret
                        return ret
            return 0
        def max_flow(self, s, t):
            flow = 0
            INF_FLOW = 10**9
            while self.bfs(s, t):
                self.it = [0] * self.n
                while True:
                    f = self.dfs(s, t, INF_FLOW)
                    if f == 0:
                        break
                    flow += f
            return flow
    
    # Check if we can achieve distance >= D
    def check(D):
        if D == 0:
            return True
        # Graph: D+1 layers, each original vertex has D+1 copies
        # node id: v * (D+1) + i, for i in 0..D
        # Source: 0 * (D+1) + 0 = 0
        # Sink: (N-1) * (D+1) + D
        # Edges from original u->v: for i=0..D-1, u_i -> v_{i+1} with capacity 1
        num_nodes = N * (D + 1)
        source = 0
        sink = (N - 1) * (D + 1) + D
        dinic = Dinic(num_nodes)
        for (u, v) in edges:
            for i in range(D):
                u_id = u * (D + 1) + i
                v_id = v * (D + 1) + (i + 1)
                dinic.add_edge(u_id, v_id, 1)
        return dinic.max_flow(source, sink) <= K
    
    # Binary search on D
    lo = 0
    hi = L
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if check(mid):
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    print(ans)

if __name__ == "__main__":
    solve()