import sys

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
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
    # Flattened index: (r, c) -> r * W + c
    F = []
    for _ in range(H):
        row = []
        for _ in range(W):
            row.append(int(next(iterator)))
        F.append(row)

    N = H * W
    
    # Build edges for Maximum Spanning Tree
    # Nodes are 0 to N-1.
    # Edge between u and v has weight min(F[u], F[v])
    edges = []
    
    # Directions: right, down (to avoid duplicates)
    # We iterate through the grid and add edges to right and down neighbors
    for r in range(H):
        for c in range(W):
            u = r * W + c
            height_u = F[r][c]
            
            # Right neighbor
            if c + 1 < W:
                v = u + 1
                weight = height_u if height_u < F[r][c+1] else F[r][c+1]
                edges.append((weight, u, v))
            
            # Down neighbor
            if r + 1 < H:
                v = u + W
                weight = height_u if height_u < F[r+1][c] else F[r+1][c]
                edges.append((weight, u, v))
    
    # Sort edges by weight descending for Kruskal's
    edges.sort(reverse=True)
    
    # Union-Find data structure
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
    mst_adj = [[] for _ in range(N)]
    edges_count = 0
    
    for w, u, v in edges:
        if union(u, v):
            mst_adj[u].append((v, w))
            mst_adj[v].append((u, w))
            edges_count += 1
            if edges_count == N - 1:
                break
    
    # Preprocess for LCA and Min-Edge Query
    # We use BFS to avoid recursion depth issues and compute depths/parents
    depth = [-1] * N
    parent_node = [-1] * N
    min_edge_to_parent = [0] * N
    
    # BFS starting from node 0
    queue = [0]
    depth[0] = 0
    parent_node[0] = -1
    min_edge_to_parent[0] = float('inf')
    
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        
        for v, w in mst_adj[u]:
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                parent_node[v] = u
                min_edge_to_parent[v] = w
                queue.append(v)
    
    # Binary Lifting Precomputation
    LOG = 20 # 2^19 > 250,000
    up = [[-1] * LOG for _ in range(N)]
    min_val = [[float('inf')] * LOG for _ in range(N)]
    
    # Initialize for direct parents
    for i in range(N):
        if parent_node[i] != -1:
            up[i][0] = parent_node[i]
            min_val[i][0] = min_edge_to_parent[i]
    
    # Fill the tables
    for j in range(1, LOG):
        for i in range(N):
            if up[i][j-1] != -1:
                up[i][j] = up[up[i][j-1]][j-1]
                min_val[i][j] = min(min_val[i][j-1], min_val[up[i][j-1]][j-1])
            else:
                up[i][j] = -1
                min_val[i][j] = float('inf')
    
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
        if u == v:
            return float('inf')
        
        lca = get_lca(u, v)
        
        # Path u -> lca
        curr = u
        res = float('inf')
        diff = depth[u] - depth[lca]
        for j in range(LOG):
            if (diff >> j) & 1:
                res = min(res, min_val[curr][j])
                curr = up[curr][j]
        
        # Path v -> lca
        curr = v
        diff = depth[v] - depth[lca]
        for j in range(LOG):
            if (diff >> j) & 1:
                res = min(res, min_val[curr][j])
                curr = up[curr][j]
        
        return res

    # Process Queries
    try:
        Q_str = next(iterator)
        Q = int(Q_str)
    except StopIteration:
        return

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
        
        if u == v:
            # Same building
            ans = abs(Y - Z)
        else:
            # Different buildings
            bottleneck = query_min_edge(u, v)
            # bottleneck is the max floor level we can maintain across the path
            # If bottleneck >= min(Y, Z), we can effectively go directly (cost |Y-Z|)
            # Otherwise, we must drop to bottleneck level
            if bottleneck >= min(Y, Z):
                ans = abs(Y - Z)
            else:
                ans = (Y - bottleneck) + (Z - bottleneck)
        
        results.append(str(ans))
    
    print('\n'.join(results))

if __name__ == '__main__':
    solve()