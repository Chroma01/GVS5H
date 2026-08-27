import sys

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
        queue = [s]
        while queue:
            u = queue.pop(0)
            for v, cap, rev in self.graph[u]:
                if cap > 0 and self.level[v] < 0:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)
        return self.level[t] >= 0

    def dfs(self, u, t, flow, ptr):
        if u == t or flow == 0:
            return flow
        for i in range(ptr[u], len(self.graph[u])):
            ptr[u] = i
            v, cap, rev = self.graph[u][i]
            if self.level[v] == self.level[u] + 1 and cap > 0:
                pushed = self.dfs(v, t, min(flow, cap), ptr)
                if pushed > 0:
                    self.graph[u][i][1] -= pushed
                    self.graph[v][rev][1] += pushed
                    return pushed
        return 0

    def max_flow(self, s, t):
        flow = 0
        while self.bfs(s, t):
            ptr = [0] * self.n
            while True:
                pushed = self.dfs(s, t, float('inf'), ptr)
                if pushed == 0:
                    break
                flow += pushed
        return flow

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
        
        edges = []
        for _ in range(M):
            u = int(next(iterator))
            v = int(next(iterator))
            edges.append((u, v))
    except StopIteration:
        return

    # Binary search for the maximum shortest distance D
    # Range of D: 0 to N. 
    # If we can block all paths of length < D, then the shortest path is >= D.
    # The maximum possible shortest path with 0/1 weights is bounded by N (actually N-1 for simple paths).
    
    low = 0
    high = N
    ans = 0

    while low <= high:
        mid = (low + high) // 2
        
        if mid == 0:
            # Shortest distance >= 0 is always true.
            ans = max(ans, mid)
            low = mid + 1
            continue

        # We need to check if we can block all paths of length < mid using at most K edges.
        # Construct a flow network where nodes are (u, dist) for 0 <= dist < mid.
        # Edges exist from (u, d) to (v, d+1) if there is an edge u->v in original graph.
        # We want to find the min-cut to disconnect (1, 0) from any (N, d) where d < mid.
        
        num_layers = mid
        # Nodes: (u, d) -> u * mid + d (using 0-based indexing for u: 0..N-1)
        # Total nodes: N * mid
        # Source is (1, 0) -> index 0
        # Sinks are all (N, d) for d in 0..mid-1
        
        num_nodes = N * num_layers
        source_idx = 0 # (1-1)*mid + 0
        
        # Create Dinic instance
        dinic = Dinic(num_nodes + 1) # +1 for super sink
        
        # Add edges
        # For each original edge u->v, add edge from (u, d) to (v, d+1) if d+1 < mid
        # Capacity is 1 for each original edge instance.
        
        for u, v in edges:
            u_idx = u - 1
            v_idx = v - 1
            
            for d in range(num_layers - 1):
                # Edge from (u, d) to (v, d+1)
                u_node = u_idx * num_layers + d
                v_node = v_idx * num_layers + (d + 1)
                
                # Add edge with capacity 1
                dinic.add_edge(u_node, v_node, 1)
        
        # Identify source and sinks
        # Source is always (1, 0)
        # Sinks are all (N, d) for d in 0..mid-1
        
        super_sink = num_nodes
        
        # Connect all (N, d) to super_sink with infinite capacity
        for d in range(num_layers):
            sink_node = (N - 1) * num_layers + d
            dinic.add_edge(sink_node, super_sink, float('inf'))
            
        min_cut = dinic.max_flow(source_idx, super_sink)
        
        if min_cut <= K:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    print(ans)

if __name__ == '__main__':
    solve()