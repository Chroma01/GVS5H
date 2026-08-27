import sys

# Increase recursion depth to handle deep recursion in DSU find if path compression isn't enough
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
    # We will flatten the grid to 0..H*W-1
    # Block (i, j) -> index i*W + j (0-based)
    F = []
    for r in range(H):
        row = []
        for c in range(W):
            row.append(int(next(iterator)))
        F.append(row)

    # Read Q
    try:
        Q = int(next(iterator))
    except StopIteration:
        Q = 0
    
    queries = []
    for i in range(Q):
        A = int(next(iterator)) - 1
        B = int(next(iterator)) - 1
        Y = int(next(iterator))
        C = int(next(iterator)) - 1
        D = int(next(iterator)) - 1
        Z = int(next(iterator))
        queries.append((A, B, Y, C, D, Z, i))

    # Flatten coordinates
    def get_id(r, c):
        return r * W + c
    
    total_blocks = H * W
    
    # DSU structures
    parent = list(range(total_blocks))
    rank = [0] * total_blocks
    
    def find_root(i):
        path = []
        while i != parent[i]:
            path.append(i)
            i = parent[i]
        for node in path:
            parent[node] = i
        return i
    
    # Store queries in components
    # queries_in_comp[root] = list of query indices where one endpoint is 'root' (or in this component)
    # We store each query in BOTH its start and end components to ensure we catch the merge regardless of direction.
    comp_queries = [[] for _ in range(total_blocks)]
    
    query_details = [] # To store (start_node, end_node) for each query index
    
    for q_idx, (A, B, Y, C, D, Z, orig_idx) in enumerate(queries):
        start_node = get_id(A, B)
        end_node = get_id(C, D)
        query_details.append((start_node, end_node))
        
        comp_queries[start_node].append(q_idx)
        comp_queries[end_node].append(q_idx)
        
    ans = [0] * Q
    
    # Collect unique heights and sort descending
    unique_heights = sorted(list(set(F[r][c] for r in range(H) for c in range(W))), reverse=True)
    
    # Precompute edges and their activation height
    # Edge (u, v) activates when height <= min(F[u], F[v])
    # We process heights descending, so we add edges when h == min(F[u], F[v])
    edges = []
    for r in range(H):
        for c in range(W):
            u = get_id(r, c)
            # Check neighbors
            if r > 0:
                v = get_id(r-1, c)
                act_h = min(F[r][c], F[r-1][c])
                if u < v:
                    edges.append((act_h, u, v))
            if r < H-1:
                v = get_id(r+1, c)
                act_h = min(F[r][c], F[r+1][c])
                if u < v:
                    edges.append((act_h, u, v))
            if c > 0:
                v = get_id(r, c-1)
                act_h = min(F[r][c], F[r][c-1])
                if u < v:
                    edges.append((act_h, u, v))
            if c < W-1:
                v = get_id(r, c+1)
                act_h = min(F[r][c], F[r][c+1])
                if u < v:
                    edges.append((act_h, u, v))
    
    # Sort edges descending by activation height
    edges.sort(key=lambda x: x[0], reverse=True)
    
    edge_idx = 0
    num_edges = len(edges)
    
    # Process heights
    for h in unique_heights:
        # Add edges with activation height == h
        while edge_idx < num_edges and edges[edge_idx][0] == h:
            _, u, v = edges[edge_idx]
            edge_idx += 1
            
            root_u = find_root(u)
            root_v = find_root(v)
            
            if root_u != root_v:
                # Ensure root_u is the larger component (for small-to-large merging)
                if rank[root_u] < rank[root_v]:
                    root_u, root_v = root_v, root_u
                
                # Process queries in the smaller component (root_v)
                # We iterate through queries stored in root_v.
                # For each query, if it's not answered yet, we check if its other endpoint is in root_u.
                # If so, the query is resolved at height h.
                # If not, we move the query to root_u's list to be checked later.
                
                for q_idx in comp_queries[root_v]:
                    if ans[q_idx] == 0:
                        start, end = query_details[q_idx]
                        
                        # Determine which endpoint is in root_v
                        # Since q_idx is in comp_queries[root_v], at least one is.
                        # We need to find the one that is NOT in root_v to check if it's in root_u.
                        # Actually, we just need to check if the OTHER endpoint is in root_u.
                        # If start is in root_v, other is end.
                        # If end is in root_v, other is start.
                        # Note: It's possible both are in root_v (already connected), but then ans would be set?
                        # No, if both are in root_v, they are already connected, so this edge wouldn't merge them.
                        # So exactly one is in root_v and the other is elsewhere (or in root_u).
                        
                        if find_root(start) == root_v:
                            other = end
                        else:
                            other = start
                        
                        if find_root(other) == root_u:
                            ans[q_idx] = h
                        else:
                            # Move to root_u
                            comp_queries[root_u].append(q_idx)
                
                # Merge components
                parent[root_v] = root_u
                if rank[root_u] == rank[root_v]:
                    rank[root_u] += 1

    # Output results
    for i in range(Q):
        print(ans[i])

if __name__ == '__main__':
    solve()