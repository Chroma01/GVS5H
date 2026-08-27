import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    ptr = 0
    N = int(input_data[ptr]); ptr += 1
    M = int(input_data[ptr]); ptr += 1
    K = int(input_data[ptr]); ptr += 1
    edges = []
    for _ in range(M):
        u = int(input_data[ptr]); ptr += 1
        v = int(input_data[ptr]); ptr += 1
        edges.append((u, v))

    class Dinic:
        def __init__(self, n):
            self.n = n
            self.graph = [[] for _ in range(n)]
        
        def add_edge(self, fr, to, cap):
            forward = [to, cap, None]
            backward = [fr, 0, None]
            forward[2] = backward
            backward[2] = forward
            self.graph[fr].append(forward)
            self.graph[to].append(backward)
        
        def bfs(self, s, t):
            self.level = [-1] * self.n
            q = deque([s])
            self.level[s] = 0
            while q:
                v = q.popleft()
                for e in self.graph[v]:
                    if e[1] > 0 and self.level[e[0]] < 0:
                        self.level[e[0]] = self.level[v] + 1
                        q.append(e[0])
            return self.level[t] >= 0
        
        def dfs(self, v, t, f):
            if v == t:
                return f
            for i in range(self.it[v], len(self.graph[v])):
                self.it[v] = i
                e = self.graph[v][i]
                if e[1] > 0 and self.level[v] < self.level[e[0]]:
                    d = self.dfs(e[0], t, min(f, e[1]))
                    if d > 0:
                        e[1] -= d
                        e[2][1] += d
                        return d
            return 0
        
        def max_flow(self, s, t):
            flow = 0
            INF = float('inf')
            while self.bfs(s, t):
                self.it = [0] * self.n
                while True:
                    f = self.dfs(s, t, INF)
                    if f == 0:
                        break
                    flow += f
            return flow

    def check(D):
        # Check if we can make shortest path >= D using at most K edges
        # Layered graph: nodes are (v, l) for v in 1..N, l in 0..D-1
        # Node id: (v-1)*D + l
        num_nodes = N * D + 2
        S = N * D
        T = N * D + 1
        dinic = Dinic(num_nodes)
        INF = K + 1  # Capacity larger than K is effectively infinite
        
        for u, v in edges:
            u -= 1
            v -= 1
            for l in range(D):
                id_u = u * D + l
                # Option 1: don't set weight to 1, stay in same layer (cost 0 to use, but cut cost 1)
                dinic.add_edge(id_u, v * D + l, 1)
                # Option 2: set weight to 1, move to next layer (cost 1 to use, cut cost INF)
                if l + 1 < D:
                    dinic.add_edge(id_u, v * D + (l + 1), INF)
        
        # Connect all layers of N to sink
        for l in range(D):
            dinic.add_edge((N - 1) * D + l, T, INF)
        
        return dinic.max_flow(S, T) <= K

    # Binary search for the maximum D
    # The answer is at most N-1 (since N <= 30, any simple path has at most N-1 edges)
    # But with multi-edges and cycles, it could be larger? No, shortest path never uses cycles.
    # So max possible is N-1.
    lo, hi = 0, N  # hi is exclusive
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if check(mid):
            lo = mid
        else:
            hi = mid
    
    print(lo)

if __name__ == "__main__":
    solve()