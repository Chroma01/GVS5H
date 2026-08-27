import sys
import array

# Increase recursion depth just in case, though we use iterative approaches
sys.setrecursionlimit(10**6)

def solve():
    # Fast I/O
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return
    
    # Read F
    F = []
    for _ in range(H):
        row = [int(next(iterator)) for _ in range(W)]
        F.append(row)
    
    try:
        Q_val = int(next(iterator))
    except StopIteration:
        Q_val = 0
    
    queries = []
    for _ in range(Q_val):
        A = int(next(iterator))
        B = int(next(iterator))
        Y = int(next(iterator))
        C = int(next(iterator))
        D = int(next(iterator))
        Z = int(next(iterator))
        queries.append((A, B, Y, C, D, Z))
    
    # Edges
    # We only need to store edges for Kruskal's
    # Store as (weight, u, v)
    edges = []
    # Iterate over cells
    for r in range(H):
        row_f = F[r]
        next_row_f = F[r+1] if r + 1 < H else None
        
        for c in range(W):
            u = r * W + c
            f_u = row_f[c]
            
            # Right neighbor
            if c + 1 < W:
                v = u + 1
                f_v = row_f[c+1]
                w = f_u if f_u < f_v else f_v
                edges.append((w, u, v))
            
            # Down neighbor
            if r + 1 < H:
                v = u + W
                f_v = next_row_f[c]
                w = f_u if f_u < f_v else f_v
                edges.append((w, u, v))
    
    # Sort edges descending by weight
    edges.sort(reverse=True)
    
    # Free F memory
    del F
    
    # DSU
    N = H * W
    parent = list(range(N))
    
    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        curr = i
        while curr != root:
            nxt = parent[curr]
            parent[curr] = root
            curr = nxt
        return root
    
    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        if root_i != root_j:
            parent[root_i] = root_j
            return True
        return False
    
    # MST Adjacency List
    adj = [[] for _ in range(N)]
    edges_count = 0
    for w, u, v in edges:
        if union(u, v):
            adj[u].append((v, w))
            adj[v].append((u, w))
            edges_count += 1
            if edges_count == N - 1:
                break
    
    # Free edges and DSU memory
    del edges
    del parent
    
    # LCA Preprocessing
    LOG = 19
    INF = 10**9 + 7
    
    # Using array for memory efficiency
    # up[k][u] stores the 2^k-th ancestor of u
    up = [array.array('I', [0] * N) for _ in range(LOG)]
    # min_edge_table[k][u] stores the min edge weight on the path from u to its 2^k-th ancestor
    min_edge_table = [array.array('I', [INF] * N) for _ in range(LOG)]
    
    # BFS to compute depth, parent (up[0]), and min_edge_to_parent (min_edge_table[0])
    root = 0
    depth = [-1] * N
    depth[root] = 0
    
    queue = [root]
    idx = 0
    
    up[0][root] = root
    # min_edge_table[0][root] is already INF
    
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        
        d_u = depth[u]
        for v, w in adj[u]:
            if depth[v] == -1:
                depth[v] = d_u + 1
                up[0][v] = u
                min_edge_table[0][v] = w
                queue.append(v)
    
    # Free adj memory
    del adj
    
    # Build binary lifting table
    for k in range(1, LOG):
        prev_up = up[k-1]
        curr_up = up[k]
        prev_min = min_edge_table[k-1]
        curr_min = min_edge_table[k]
        
        for u in range(N):
            mid = prev_up[u]
            curr_up[u] = prev_up[mid]
            m1 = prev_min[u]
            m2 = prev_min[mid]
            curr_min[u] = m1 if m1 < m2 else m2
    
    # Query processing
    results = []
    
    for A, B, Y, C, D, Z in queries:
        u = (A - 1) * W + (B - 1)
        v = (C - 1) * W + (D - 1)
        
        if u == v:
            results.append(str(abs(Y - Z)))
        else:
            # Find min edge on path between u and v
            if depth[u] < depth[v]:
                u, v = v, u
            
            res = INF
            
            # Lift u to depth of v
            diff = depth[u] - depth[v]
            for k in range(LOG):
                if (diff >> k) & 1:
                    m = min_edge_table[k][u]
                    if m < res:
                        res = m
                    u = up[k][u]
            
            if u != v:
                # Lift both u and v until they are just below LCA
                for k in range(LOG-1, -1, -1):
                    if up[k][u] != up[k][v]:
                        m1 = min_edge_table[k][u]
                        m2 = min_edge_table[k][v]
                        if m1 < res: res = m1
                        if m2 < res: res = m2
                        u = up[k][u]
                        v = up[k][v]
                
                # Now u and v are children of LCA
                m1 = min_edge_table[0][u]
                m2 = min_edge_table[0][v]
                if m1 < res: res = m1
                if m2 < res: res = m2
            
            H_max = res
            
            min_YZ = Y if Y < Z else Z
            if H_max >= min_YZ:
                ans = abs(Y - Z)
            else:
                ans = abs(Y - H_max) + abs(Z - H_max)
            results.append(str(ans))
    
    sys.stdout.write('\n'.join(results) + '\n')

if __name__ == '__main__':
    solve()