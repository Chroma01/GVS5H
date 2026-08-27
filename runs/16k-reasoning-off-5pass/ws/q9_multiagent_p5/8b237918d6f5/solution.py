import sys
from collections import deque

# Increase recursion depth just in case
sys.setrecursionlimit(2000)

class Dinic:
    def __init__(self, n):
        self.n = n
        self.graph = [[] for _ in range(n)]
        self.level = []

    def add_edge(self, u, v, capacity):
        # Forward edge with capacity
        # Store as [v, capacity, rev_index]
        self.graph[u].append([v, capacity, len(self.graph[v])])
        # Backward edge with 0 capacity
        self.graph[v].append([u, 0, len(self.graph[u]) - 1])

    def bfs(self, s, t):
        self.level = [-1] * self.n
        self.level[s] = 0
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v, cap, rev_idx in self.graph[u]:
                if cap > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
        return self.level[t] >= 0

    def dfs(self, u, t, flow, ptr):
        if u == t or flow == 0:
            return flow
        for i in range(ptr[u], len(self.graph[u])):
            ptr[u] = i
            v, cap, rev_idx = self.graph[u][i]
            if self.level[v] == self.level[u] + 1 and cap > 0:
                pushed = self.dfs(v, t, min(flow, cap), ptr)
                if pushed > 0:
                    self.graph[u][i][1] -= pushed
                    self.graph[v][rev_idx][1] += pushed
                    return pushed
        return 0

    def max_flow(self, s, t):
        max_f = 0
        while self.bfs(s, t):
            ptr = [0] * self.n
            while True:
                pushed = self.dfs(s, t, float('inf'), ptr)
                if pushed == 0:
                    break
                max_f += pushed
        return max_f

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    edges = []
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        edges.append((u, v))

    # Step 1: BFS for L (shortest path length in unweighted graph)
    # This represents the physical limit: even if all edges on the shortest path 
    # are set to weight 1, the distance is L.
    min_path_len = float('inf')
    dist = [-1] * (N + 1)
    dist[1] = 0
    queue = deque([1])
    
    while queue:
        u = queue.popleft()
        if u == N:
            min_path_len = dist[u]
            break
        for v, _ in edges:
            if dist[v] == -1:
                dist[v] = dist[u] + 1
                queue.append(v)
    
    # If N is not reachable (though constraints say it is), answer is 0
    if min_path_len == float('inf'):
        print(0)
        return
    
    # Step 2: Max Flow for P (max number of edge-disjoint paths)
    # This represents the bottleneck capacity. To ensure every path has a weight 
    # of at least W, we must select at least W edges on each of the P disjoint paths.
    # Since these paths are edge-disjoint, this requires W * P edges.
    source = 1
    sink = N
    dinic = Dinic(N + 1)
    
    for u, v in edges:
        dinic.add_edge(u, v, 1)
    
    max_disjoint_paths = dinic.max_flow(source, sink)
    
    # If no paths exist (contradicts constraints, but handle gracefully)
    if max_disjoint_paths == 0:
        print(0)
        return
        
    # Step 3: Calculate Answer
    # The maximum possible shortest distance is min(L, floor(K / P))
    ans = min(min_path_len, K // max_disjoint_paths)
    print(ans)

if __name__ == '__main__':
    solve()