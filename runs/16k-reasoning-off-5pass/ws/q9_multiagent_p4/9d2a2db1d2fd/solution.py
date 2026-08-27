import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read
    data = input_data().split()
    iterator = iter(data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read grid F
    # F is H x W
    F = []
    for _ in range(H):
        row = []
        for _ in range(W):
            row.append(int(next(iterator)))
        F.append(row)

    # Read Q
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0

    # Prepare edges for MST
    # Nodes are (r, c) mapped to r * W + c
    # Edges connect adjacent cells with weight min(F[r][c], F[nr][nc])
    edges = []
    for r in range(H):
        for c in range(W):
            u = r * W + c
            # Right neighbor
            if c + 1 < W:
                v = r * W + (c + 1)
                w = min(F[r][c], F[r][c+1])
                edges.append((w, u, v))
            # Down neighbor
            if r + 1 < H:
                v = (r + 1) * W + c
                w = min(F[r][c], F[r+1][c])
                edges.append((w, u, v))
    
    # Sort edges by weight descending for Kruskal's
    edges.sort(reverse=True)
    
    # Union-Find data structure
    parent = list(range(H * W))
    rank = [0] * (H * W)
    
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
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            if rank[root_i] == rank[root_j]:
                rank[root_i] += 1
            return True
        return False

    # Build MST (Adjacency list)
    adj = [[] for _ in range(H * W)]
    edges_count = 0
    for w, u, v in edges:
        if union(u, v):
            adj[u].append((v, w))
            adj[v].append((u, w))
            edges_count += 1
    
    # Precompute LCA and Min Edge on Path
    # We root the tree at node 0.
    parent_node = [-1] * (H * W)
    depth = [0] * (H * W)
    min_edge_to_parent = [0] * (H * W)
    
    queue = [0]
    visited = [False] * (H * W)
    visited[0] = True
    
    # BFS to build tree structure
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        for v, w in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent_node[v] = u
                depth[v] = depth[u] + 1
                min_edge_to_parent[v] = w
                queue.append(v)
    
    # Binary Lifting Table
    # up[u][i] stores the 2^i-th ancestor of u
    # min_up[u][i] stores the min edge weight on the path from u to up[u][i]
    LOG = 19 # 2^18 = 262144 > 250000
    up = [[-1] * LOG for _ in range(H * W)]
    min_up = [[0] * LOG for _ in range(H * W)]
    
    # Initialize level 0
    for i in range(H * W):
        if parent_node[i] != -1:
            up[i][0] = parent_node[i]
            min_up[i][0] = min_edge_to_parent[i]
        else:
            up[i][0] = i
            min_up[i][0] = 0 
            
    # Fill table
    for j in range(1, LOG):
        for i in range(H * W):
            if up[i][j-1] != -1:
                up[i][j] = up[up[i][j-1]][j-1]
                min_up[i][j] = min(min_up[i][j-1], min_up[up[i][j-1]][j-1])
            else:
                up[i][j] = -1
                min_up[i][j] = 0 

    def get_min_on_path(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        
        # Lift u to same depth as v
        res = 0
        diff = depth[u] - depth[v]
        for j in range(LOG):
            if (diff >> j) & 1:
                res = min(res, min_up[u][j])
                u = up[u][j]
        
        if u == v:
            return res
        
        # Lift both until just below LCA
        for j in range(LOG - 1, -1, -1):
            if up[u][j] != up[v][j]:
                res = min(res, min_up[u][j])
                res = min(res, min_up[v][j])
                u = up[u][j]
                v = up[v][j]
        
        # One more step to LCA
        res = min(res, min_up[u][0])
        res = min(res, min_up[v][0])
        return res

    results = []
    for _ in range(Q):
        A = int(next(iterator)) - 1
        B = int(next(iterator)) - 1
        Y = int(next(iterator))
        C = int(next(iterator)) - 1
        D = int(next(iterator)) - 1
        Z = int(next(iterator))
        
        start_node = A * W + B
        end_node = C * W + D
        
        # Find max bottleneck path in MST
        bottleneck = get_min_on_path(start_node, end_node)
        
        min_yz = Y if Y < Z else Z
        if bottleneck >= min_yz:
            ans = abs(Y - Z)
        else:
            ans = Y + Z - 2 * bottleneck
        
        results.append(str(ans))
    
    print('\n'.join(results))

if __name__ == '__main__':
    solve()