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

    # Binary search for the maximum shortest path length L
    # Range of L: [0, M]
    low = 0
    high = M
    ans = 0

    while low <= high:
        mid = (low + high) // 2
        
        if mid == 0:
            # Distance 0 is always achievable if a path exists (guaranteed by problem statement)
            ans = max(ans, 0)
            low = mid + 1
            continue

        # Check if it's possible to make shortest path >= mid
        # We need to block all paths that have < mid edges of weight 1.
        # Construct layered graph: nodes (u, d) where 0 <= d < mid
        # Source: (1, 0)
        # Sinks: (N, 0), (N, 1), ..., (N, mid-1)
        
        num_layers = mid
        # Node mapping: (u, d) -> (u-1) * num_layers + d
        # Vertices 1..N mapped to 0..N-1
        
        source = 0 # (1, 0) -> 0 * mid + 0
        
        # Identify sink nodes in the layered graph
        sink_nodes = []
        for d in range(mid):
            sink_nodes.append((N - 1) * mid + d)
        
        # Create Dinic instance
        # Nodes are 0 to (N-1)*mid + (mid-1)
        # Total nodes = N * mid
        dinic = Dinic(N * mid)
        
        # Add edges
        # For each original edge u -> v
        for u, v in edges:
            u_idx = u - 1
            v_idx = v - 1
            
            # Option 1: Edge is weight 0. Transition (u, d) -> (v, d)
            # Capacity 1. If we cut this, we force the edge to be weight 1.
            for d in range(mid):
                u_node = u_idx * mid + d
                v_node = v_idx * mid + d
                dinic.add_edge(u_node, v_node, 1)
            
            # Option 2: Edge is weight 1. Transition (u, d) -> (v, d+1)
            # Capacity infinity. This represents the path accumulating cost.
            # We only add this if d+1 < mid because we only care about paths staying within layers < mid.
            # If a path reaches layer 'mid', it has >= mid ones, which is acceptable (not a sink).
            for d in range(mid - 1):
                u_node = u_idx * mid + d
                v_node = v_idx * mid + (d + 1)
                dinic.add_edge(u_node, v_node, float('inf'))
        
        # Calculate max flow from source to all sink nodes
        # Add a super-sink to handle multiple destination nodes
        super_sink = N * mid
        dinic.graph.append([]) # Extend graph list to include super_sink
        
        for s_node in sink_nodes:
            dinic.add_edge(s_node, super_sink, float('inf'))
            
        flow = dinic.max_flow(source, super_sink)
        
        if flow <= K:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    print(ans)

if __name__ == '__main__':
    solve()