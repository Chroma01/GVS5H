import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read grid F
    # Flattened index: (i, j) -> i * W + j
    # 0-based indexing for internal logic
    F = []
    for _ in range(H):
        row = []
        for _ in range(W):
            row.append(int(next(iterator)))
        F.append(row)
    
    # Total nodes
    N = H * W
    
    # Build edges
    # Edge between u and v has weight min(F[u], F[v])
    # We will store edges as (weight, u, v)
    edges = []
    
    # Directions: up, down, left, right
    # We only add edges to avoid duplicates (e.g., only right and down)
    # But for Kruskal's, order doesn't matter, just need all unique edges.
    # Let's iterate i from 0 to H-1, j from 0 to W-1
    # Add edge to (i+1, j) if exists
    # Add edge to (i, j+1) if exists
    
    for r in range(H):
        for c in range(W):
            u = r * W + c
            val_u = F[r][c]
            
            # Down
            if r + 1 < H:
                v = (r + 1) * W + c
                val_v = F[r+1][c]
                w = val_u if val_u < val_v else val_v
                edges.append((w, u, v))
            
            # Right
            if c + 1 < W:
                v = r * W + (c + 1)
                val_v = F[r][c+1]
                w = val_u if val_u < val_v else val_v
                edges.append((w, u, v))
    
    # Sort edges by weight descending for Maximum Spanning Tree
    edges.sort(key=lambda x: x[0], reverse=True)
    
    # DSU for Kruskal's
    parent = list(range(N))
    def find(i):
        path = []
        while parent[i] != i:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False
    
    # Build MST adjacency list
    # adj[u] = [(v, weight), ...]
    adj = [[] for _ in range(N)]
    edges_count = 0
    for w, u, v in edges:
        if union(u, v):
            adj[u].append((v, w))
            adj[v].append((u, w))
            edges_count += 1
            if edges_count == N - 1:
                break
    
    # Preprocess for LCA and Min Edge on Path
    # Binary lifting
    LOG = 19 # 2^18 = 262144 > 250000
    up = [[-1] * LOG for _ in range(N)]
    min_edge = [[float('inf')] * LOG for _ in range(N)]
    depth = [0] * N
    
    # BFS to set depths and 2^0 parent
    # Start BFS from node 0 (arbitrary root)
    queue = [0] 
    visited = [False] * N
    visited[0] = True
    depth[0] = 0
    
    # Using a list as a queue
    q_idx = 0
    while q_idx < len(queue):
        u = queue[q_idx]
        q_idx += 1
        
        for v, w in adj[u]:
            if not visited[v]:
                visited[v] = True
                depth[v] = depth[u] + 1
                up[v][0] = u
                min_edge[v][0] = w
                queue.append(v)
    
    # Build binary lifting tables
    for j in range(1, LOG):
        for i in range(N):
            if up[i][j-1] != -1:
                up[i][j] = up[up[i][j-1]][j-1]
                min_edge[i][j] = min(min_edge[i][j-1], min_edge[up[i][j-1]][j-1])
            else:
                up[i][j] = -1
                min_edge[i][j] = float('inf')
    
    def get_lca(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        
        # Lift u to same depth as v
        diff = depth[u] - depth[v]
        for j in range(LOG):
            if (diff >> j) & 1:
                u = up[u][j]
        
        if u == v:
            return u
        
        # Lift both until just below LCA
        for j in range(LOG - 1, -1, -1):
            if up[u][j] != up[v][j]:
                u = up[u][j]
                v = up[v][j]
        
        return up[u][0]
    
    def query_min_edge(u, v):
        lca = get_lca(u, v)
        res = float('inf')
        
        # Path u -> lca
        curr = u
        diff = depth[curr] - depth[lca]
        for j in range(LOG):
            if (diff >> j) & 1:
                res = min(res, min_edge[curr][j])
                curr = up[curr][j]
        
        # Path v -> lca
        curr = v
        diff = depth[curr] - depth[lca]
        for j in range(LOG):
            if (diff >> j) & 1:
                res = min(res, min_edge[curr][j])
                curr = up[curr][j]
        
        return res

    try:
        Q_str = next(iterator)
        Q = int(Q_str)
    except StopIteration:
        Q = 0
        
    results = []
    for _ in range(Q):
        A = int(next(iterator)) - 1
        B = int(next(iterator)) - 1
        Y = int(next(iterator))
        C = int(next(iterator)) - 1
        D = int(next(iterator)) - 1
        Z = int(next(iterator))
        
        u = A * W + B
        v = C * W + D
        
        # H_opt is the max-min height on the path
        # If u == v, H_opt is effectively infinity (or max possible), but problem says distinct
        # However, if they are in same component, we get a value.
        # If graph is disconnected (impossible here as we built MST of connected component? 
        # Wait, the grid is connected, so MST is connected.
        
        if u == v:
            # Should not happen based on constraints, but handle gracefully
            h_opt = float('inf')
        else:
            h_opt = query_min_edge(u, v)
        
        # Cost calculation
        # If h_opt >= max(Y, Z), cost is |Y - Z|
        # Formula: max(|Y-Z|, Y + Z - 2*h_opt)
        # Note: if h_opt is inf, Y+Z-2*inf is -inf, max takes |Y-Z|. Correct.
        
        ans = max(abs(Y - Z), Y + Z - 2 * h_opt)
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()