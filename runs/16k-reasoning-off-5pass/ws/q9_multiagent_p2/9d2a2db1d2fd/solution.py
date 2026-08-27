import sys
import heapq

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(2000000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read
    if input_data is None:
        return
    data = input_data().split()
    iterator = iter(data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read grid F
    F = []
    for _ in range(H):
        row = []
        for _ in range(W):
            row.append(int(next(iterator)))
        F.append(row)

    # Flatten grid to 1D index: (r, c) -> r * W + c
    num_nodes = H * W
    
    # We need to build the Maximum Spanning Tree (MST) of the grid graph.
    # Edge weight between adjacent cells u, v is min(F[u], F[v]).
    # We use Prim's algorithm.
    
    # max_edge[u] stores the max weight edge connecting u to the current tree
    max_edge = [-1] * num_nodes
    parent = [-1] * num_nodes
    in_tree = [False] * num_nodes
    
    # Start from node 0 (0,0)
    start_node = 0
    max_edge[start_node] = float('inf') 
    
    # Priority queue stores (-weight, u) to simulate max-heap
    pq = [(-float('inf'), start_node)]
    
    while pq:
        neg_w, u = heapq.heappop(pq)
        w = -neg_w
        
        if in_tree[u]:
            continue
        
        in_tree[u] = True
        
        # If u is not the start node, add edge to MST
        if parent[u] != -1:
            p = parent[u]
            # The edge weight is w
            pass
        
        # Explore neighbors
        r, c = divmod(u, W)
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < H and 0 <= nc < W:
                v = nr * W + nc
                if not in_tree[v]:
                    weight = min(F[r][c], F[nr][nc])
                    # We want max weight, so push -weight
                    if weight > max_edge[v]:
                        max_edge[v] = weight
                        parent[v] = u
                        heapq.heappush(pq, (-weight, v))
    
    # Build LCA structure (Binary Lifting)
    # up[u][i] = 2^i-th ancestor of u
    # min_val[u][i] = min edge weight on path from u to up[u][i]
    
    LOG = 20 # Sufficient for 500*500 = 250,000 nodes (2^18 > 250k)
    up = [[-1] * LOG for _ in range(num_nodes)]
    min_val = [[0] * LOG for _ in range(num_nodes)]
    
    # Initialize depth
    depth = [-1] * num_nodes
    depth[0] = 0
    
    # Build tree adjacency list from parent pointers (Prim's builds a tree rooted at 0)
    tree_adj = [[] for _ in range(num_nodes)]
    for u in range(1, num_nodes):
        p = parent[u]
        w = max_edge[u]
        tree_adj[p].append((u, w))
        up[u][0] = p
        min_val[u][0] = w
    
    # BFS to set depths and verify tree structure
    bfs_q = [0]
    head = 0
    while head < len(bfs_q):
        u = bfs_q[head]
        head += 1
        
        for v, w in tree_adj[u]:
            depth[v] = depth[u] + 1
            bfs_q.append(v)
            
    # Fill the table
    for j in range(1, LOG):
        for u in range(num_nodes):
            if up[u][j-1] != -1:
                p = up[u][j-1]
                up[u][j] = up[p][j-1]
                if up[p][j-1] != -1:
                    min_val[u][j] = min(min_val[u][j-1], min_val[p][j-1])
                else:
                    min_val[u][j] = min_val[u][j-1]
            else:
                up[u][j] = -1
                min_val[u][j] = min_val[u][j-1]

    def get_bottleneck(u, v):
        if depth[u] < depth[v]:
            u, v = v, u
        
        # Lift u to same depth as v
        diff = depth[u] - depth[v]
        res = float('inf')
        
        for j in range(LOG):
            if (diff >> j) & 1:
                res = min(res, min_val[u][j])
                u = up[u][j]
        
        if u == v:
            return res
        
        # Lift both until just below LCA
        for j in range(LOG - 1, -1, -1):
            if up[u][j] != up[v][j]:
                res = min(res, min_val[u][j])
                res = min(res, min_val[v][j])
                u = up[u][j]
                v = up[v][j]
        
        # Now u and v are children of LCA
        res = min(res, min_val[u][0])
        res = min(res, min_val[v][0])
        
        return res

    # Process Queries
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
        
        # Bottleneck height of the path in the grid
        h_star = get_bottleneck(u, v)
        
        # If h_star is infinity (should not happen in connected grid), handle gracefully
        if h_star == float('inf'):
            h_star = 10**9 # Effectively infinite
        
        min_floor = min(Y, Z)
        
        if h_star >= min_floor:
            ans = abs(Y - Z)
        else:
            ans = abs(Y - Z) + 2 * (min_floor - h_star)
        
        results.append(str(ans))
        
    print('\n'.join(results))

if __name__ == '__main__':
    solve()