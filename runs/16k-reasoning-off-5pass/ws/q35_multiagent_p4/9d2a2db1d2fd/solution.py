import sys

# Increase recursion depth just in case, though we use iterative DSU or small depth
sys.setrecursionlimit(2000000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = next(iterator)
        W = int(W)
    except StopIteration:
        return

    # Read grid F
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
    for i in range(Q):
        A = int(next(iterator))
        B = int(next(iterator))
        Y = int(next(iterator))
        C = int(next(iterator))
        D = int(next(iterator))
        Z = int(next(iterator))
        # Convert to 0-indexed
        queries.append({
            'id': i,
            'u': (A-1, B-1),
            'v': (C-1, D-1),
            'Y': Y,
            'Z': Z
        })

    # If Q is 0, just exit
    if Q == 0:
        return

    # Map (r, c) to node index
    def get_node(r, c):
        return r * W + c

    # Initialize DSU
    parent = list(range(H * W))
    # Size for small-to-large merging of query lists
    # We will store query lists in a separate structure attached to roots
    # query_lists[root] = dict { query_id: endpoint_node_in_this_component }
    # Actually, we just need to know if a query is in the component.
    # But we need to know which endpoint is in this component to merge correctly.
    # Let's store: query_lists[root] = { query_id: endpoint_node }
    
    # Initialize query lists
    # Each node initially has its own list.
    # For a query (u, v), we will initially add it to u's list and v's list?
    # No, standard technique:
    # Each component maintains a set of pending queries that have ONE endpoint in this component.
    # When merging A and B, we iterate over the smaller list.
    # For each query in smaller list:
    #   If query is also in larger list, then the query is now connected.
    #   The current edge weight is the answer for H_max.
    #   Otherwise, add query to larger list with the endpoint being the one in the smaller component.
    
    # To implement this efficiently:
    # query_lists[i] is a dict mapping query_id -> node_index (the endpoint in component i)
    query_lists = [{} for _ in range(H * W)]
    
    # Add queries to the lists of their start and end nodes
    for q in queries:
        qid = q['id']
        u_node = get_node(*q['u'])
        v_node = get_node(*q['v'])
        
        # Add to u's list
        query_lists[u_node][qid] = u_node
        # Add to v's list
        query_lists[v_node][qid] = v_node

    # Prepare edges
    # Edges are between adjacent cells. Weight is min(F[u], F[v])
    edges = []
    for r in range(H):
        for c in range(W):
            u = get_node(r, c)
            # Right neighbor
            if c + 1 < W:
                v = get_node(r, c + 1)
                w = min(F[r][c], F[r][c+1])
                edges.append((w, u, v))
            # Down neighbor
            if r + 1 < H:
                v = get_node(r + 1, c)
                w = min(F[r][c], F[r+1][c])
                edges.append((w, u, v))
    
    # Sort edges descending by weight
    edges.sort(key=lambda x: x[0], reverse=True)
    
    # DSU find with path compression
    def find(i):
        root = i
        while parent[root] != root:
            root = parent[root]
        
        # Path compression
        curr = i
        while curr != root:
            nxt = parent[curr]
            parent[curr] = root
            curr = nxt
        return root

    # Array to store H_max for each query
    h_max = [-1] * Q
    
    # Process edges
    for w, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Merge smaller list into larger list
            list_u = query_lists[root_u]
            list_v = query_lists[root_v]
            
            if len(list_u) < len(list_v):
                # Merge u into v
                # Iterate over list_u
                for qid, node in list_u.items():
                    if qid in list_v:
                        # Query qid is now connected!
                        # The bottleneck is the current edge weight w
                        h_max[qid] = w
                    else:
                        # Add to list_v with the node from u's component
                        list_v[qid] = node
                
                # Clear list_u to save memory (optional but good practice)
                query_lists[root_u] = {}
                parent[root_u] = root_v
            else:
                # Merge v into u
                for qid, node in list_v.items():
                    if qid in list_u:
                        h_max[qid] = w
                    else:
                        list_u[qid] = node
                
                query_lists[root_v] = {}
                parent[root_v] = root_u

    # Handle queries that were never connected by an edge?
    # This happens if start and end were already in the same component initially?
    # But initially each node is its own component. So if u != v, they are not connected.
    # However, if u == v, they are connected. But constraints say distinct locations.
    # What if the grid is disconnected even at height 1?
    # The problem implies connectivity via walkways. If two buildings are not connected
    # even at height 1, then it's impossible? But the problem asks for minimum stairs.
    # Assuming the grid is connected at height 1 (which is true if all F >= 1 and grid is rectangular).
    # If h_max[qid] is still -1, it means they are never connected.
    # In a rectangular grid with F >= 1, all nodes are connected at height 1.
    # So h_max should be >= 1 for all queries.
    # Let's double check: if h_max is -1, it means the loop finished and they weren't merged.
    # This implies they are in different components even after all edges.
    # This should not happen for a connected grid.
    
    # Calculate answers
    results = [0] * Q
    for i in range(Q):
        q = queries[i]
        Y = q['Y']
        Z = q['Z']
        Hm = h_max[i]
        
        # If Hm is -1, it means disconnected. This shouldn't happen.
        # But if it does, we can't reach. Let's assume valid input.
        if Hm == -1:
            # Fallback: should not happen
            # If disconnected, technically infinite cost? Or maybe we can't move?
            # Given constraints, we assume connectivity.
            # Let's set Hm to 0 as a safe lower bound? No, F >= 1.
            # We'll just use 0.
            Hm = 0
            
        if Hm >= min(Y, Z):
            ans = abs(Y - Z)
        else:
            ans = Y + Z - 2 * Hm
            
        results[i] = ans

    # Print results
    for res in results:
        print(res)

solve()