import sys

# Increase recursion depth just in case, though we use iterative LCA or BFS/DFS for depth
sys.setrecursionlimit(300000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    F = []
    for _ in range(H):
        row = []
        for _ in range(W):
            row.append(int(next(iterator)))
        F.append(row)

    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0

    queries = []
    for _ in range(Q):
        a = int(next(iterator))
        b = int(next(iterator))
        y = int(next(iterator))
        c = int(next(iterator))
        d = int(next(iterator))
        z = int(next(iterator))
        queries.append((a, b, y, c, d, z))

    # Flatten grid to 1D index: (r, c) -> r * W + c
    # Nodes are 0 to H*W - 1
    
    num_nodes = H * W
    
    # Build edges for the grid graph
    # Edge between (r, c) and (r', c') has weight min(F[r][c], F[r'][c'])
    edges = []
    
    # Directions: right and down to avoid duplicates
    # Right: (r, c) -> (r, c+1)
    # Down: (r, c) -> (r+1, c)
    
    for r in range(H):
        for c in range(W):
            u = r * W + c
            val_u = F[r][c]
            
            # Right neighbor
            if c + 1 < W:
                v = r * W + (c + 1)
                val_v = F[r][c + 1]
                weight = val_u if val_u < val_v else val_v
                edges.append((weight, u, v))
            
            # Down neighbor
            if r + 1 < H:
                v = (r + 1) * W + c
                val_v = F[r + 1][c]
                weight = val_u if val_u < val_v else val_v
                edges.append((weight, u, v))
    
    # Sort edges by weight descending for Maximum Spanning Tree
    edges.sort(key=lambda x: x[0], reverse=True)
    
    # Union-Find data structure
    parent = list(range(num_nodes))
    rank = [0] * num_nodes
    
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
            if rank[root_i] < rank[root_j]:
                parent[root_i] = root_j
            elif rank[root_i] > rank[root_j]:
                parent[root_j] = root_i
            else:
                parent[root_j] = root_i
                rank[root_i] += 1
            return True
        return False
    
    # Kruskal's algorithm to build MST
    # Adjacency list for the MST: adj[u] = [(v, weight), ...]
    adj = [[] for _ in range(num_nodes)]
    edges_count = 0
    
    for weight, u, v in edges:
        if union(u, v):
            adj[u].append((v, weight))
            adj[v].append((u, weight))
            edges_count += 1
            if edges_count == num_nodes - 1:
                break
    
    # Preprocess LCA with binary lifting
    # LOG = ceil(log2(num_nodes))
    LOG = 19
    up = [[-1] * LOG for _ in range(num_nodes)]
    min_edge = [[0] * LOG for _ in range(num_nodes)]
    depth = [0] * num_nodes
    
    # BFS to set depths and immediate parents (up[u][0])
    # Since the graph is a tree (MST), we can start from node 0
    # But the tree might not be connected if H*W=1? No, grid is connected.
    # However, if H=1, W=1, no edges.
    
    if num_nodes > 0:
        queue = [0]
        visited = [False] * num_nodes
        visited[0] = True
        depth[0] = 0
        up[0][0] = 0 # Parent of root is itself for convenience in LCA logic, or handle separately
        # Actually, standard LCA: parent of root is root or -1. Let's use -1 and handle carefully.
        # Let's set up[0][0] = 0 and min_edge[0][0] = infinity? 
        # Better: up[root][0] = root, min_edge[root][0] = infinity.
        # But min_edge on path to self is infinity.
        
        # Let's use a large number for infinity
        INF = 10**9 + 7
        
        # Re-initialize up and min_edge for root
        for k in range(LOG):
            up[0][k] = 0
            min_edge[0][k] = INF
            
        # BFS
        import collections
        dq = collections.deque([0])
        
        while dq:
            u = dq.popleft()
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    depth[v] = depth[u] + 1
                    up[v][0] = u
                    min_edge[v][0] = w
                    dq.append(v)
        
        # Fill binary lifting table
        for k in range(1, LOG):
            for i in range(num_nodes):
                mid = up[i][k-1]
                if mid != -1 and mid != 0: # If mid is not root's parent (which is root itself in our setup)
                    # If up[i][k-1] is 0, then up[0][k-1] is 0.
                    # We want up[i][k] = up[mid][k-1]
                    up[i][k] = up[mid][k-1]
                    # min_edge[i][k] = min(min_edge[i][k-1], min_edge[mid][k-1])
                    me1 = min_edge[i][k-1]
                    me2 = min_edge[mid][k-1]
                    min_edge[i][k] = me1 if me1 < me2 else me2
                elif mid == 0:
                    # If mid is root, then up[i][k] should be root
                    up[i][k] = 0
                    me1 = min_edge[i][k-1]
                    me2 = min_edge[0][k-1] # This is INF
                    min_edge[i][k] = me1 if me1 < me2 else me2
                else:
                    up[i][k] = -1
                    min_edge[i][k] = INF

    def get_min_edge_on_path(u, v):
        if u == v:
            return INF
        
        if depth[u] < depth[v]:
            u, v = v, u
        
        # Lift u to same depth as v
        diff = depth[u] - depth[v]
        res = INF
        
        for k in range(LOG):
            if (diff >> k) & 1:
                res = min(res, min_edge[u][k])
                u = up[u][k]
        
        if u == v:
            return res
        
        # Lift both until just below LCA
        for k in range(LOG - 1, -1, -1):
            if up[u][k] != up[v][k]:
                res = min(res, min_edge[u][k])
                res = min(res, min_edge[v][k])
                u = up[u][k]
                v = up[v][k]
        
        # Now u and v are children of LCA
        res = min(res, min_edge[u][0])
        res = min(res, min_edge[v][0])
        
        return res

    results = []
    
    for a, b, y, c, d, z in queries:
        # Convert to 0-based
        u = (a - 1) * W + (b - 1)
        v = (c - 1) * W + (d - 1)
        
        if u == v:
            # Same block, just vertical movement
            ans = abs(y - z)
            results.append(str(ans))
            continue
        
        h_max = get_min_edge_on_path(u, v)
        
        # Calculate answer
        min_yz = y if y < z else z
        if h_max >= min_yz:
            ans = abs(y - z)
        else:
            ans = y + z - 2 * h_max
            
        results.append(str(ans))
        
    print('\n'.join(results))

solve()