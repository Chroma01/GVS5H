import sys

# Increase recursion depth just in case, though we use iterative find
sys.setrecursionlimit(10**6)

def solve():
    # Fast I/O
    input = sys.stdin.read
    data = input().split()
    
    iterator = iter(data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    F = []
    for i in range(H):
        row = []
        for j in range(W):
            row.append(int(next(iterator)))
        F.append(row)
        
    Q_count = int(next(iterator))
    
    queries = []
    for i in range(Q_count):
        A = int(next(iterator)) - 1
        B = int(next(iterator)) - 1
        Y = int(next(iterator))
        C = int(next(iterator)) - 1
        D = int(next(iterator)) - 1
        Z = int(next(iterator))
        queries.append((A, B, Y, C, D, Z, i))
        
    # Map (r, c) to index
    def get_idx(r, c):
        return r * W + c
        
    # Create edges
    # Edge: (u_idx, v_idx, weight)
    # weight = min(F[u], F[v])
    edges = []
    
    # Directions: right and down to avoid duplicates
    # Right: (r, c) -> (r, c+1)
    # Down: (r, c) -> (r+1, c)
    
    for r in range(H):
        for c in range(W):
            u = get_idx(r, c)
            fu = F[r][c]
            
            # Right neighbor
            if c + 1 < W:
                v = get_idx(r, c + 1)
                fv = F[r][c + 1]
                w = fu if fu < fv else fv
                edges.append((w, u, v))
                
            # Down neighbor
            if r + 1 < H:
                v = get_idx(r + 1, c)
                fv = F[r + 1][c]
                w = fu if fu < fv else fv
                edges.append((w, u, v))
                
    # Sort edges in descending order of weight
    edges.sort(key=lambda x: x[0], reverse=True)
    
    # Union-Find data structure
    parent = list(range(H * W))
    # Size for union by size
    size = [1] * (H * W)
    
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

    def union(i, j):
        root_i = find(i)
        root_j = find(j)
        
        if root_i != root_j:
            # Union by size
            if size[root_i] < size[root_j]:
                root_i, root_j = root_j, root_i
            parent[root_j] = root_i
            size[root_i] += size[root_j]
            return root_i, root_j
        return None, None

    # For each component, store a list of queries associated with it.
    # Each query is stored as (query_index, endpoint_node)
    # When merging, we check if the other endpoint of a query is in the other component.
    
    # Initialize query lists
    # query_lists[root] = list of (query_index, node)
    query_lists = [[] for _ in range(H * W)]
    
    # Answers array
    answers = [0] * Q_count
    
    # Add queries to the lists of their start and end nodes
    for q_idx, (r1, c1, Y, r2, c2, Z, original_idx) in enumerate(queries):
        u = get_idx(r1, c1)
        v = get_idx(r2, c2)
        
        # If start and end are the same building, the bottleneck is just the building's height
        # But the problem says (A,B,Y) != (C,D,Z), so they could be same building but different floors.
        # If same building, we just move vertically. Cost is |Y-Z|.
        # The bottleneck logic still holds: B* = F[r1][c1].
        # If B* >= max(Y,Z), cost |Y-Z|. Else |Y-B*| + |Z-B*|.
        # Since B* = F[r1][c1] >= Y and >= Z (given constraints), B* >= max(Y,Z) is always true.
        # So cost is |Y-Z|.
        # We can handle this separately or let the algorithm handle it.
        # If u == v, they are already connected. We need to set the answer.
        # However, our offline process starts with no edges.
        # So we should pre-process queries where u == v.
        
        if u == v:
            # Same building
            ans = abs(Y - Z)
            answers[original_idx] = ans
        else:
            query_lists[u].append((original_idx, v))
            query_lists[v].append((original_idx, u))
            
    # Process edges
    for w, u, v in edges:
        root_u = find(u)
        root_v = find(v)
        
        if root_u != root_v:
            # Merge smaller list into larger list
            if len(query_lists[root_u]) < len(query_lists[root_v]):
                root_u, root_v = root_v, root_u
                
            # Now root_u is the new root, and it has the larger list
            # We need to merge query_lists[root_v] into query_lists[root_u]
            # But first, check for completed queries
            
            list_v = query_lists[root_v]
            list_u = query_lists[root_u]
            
            # Check queries in the smaller list (list_v)
            # For each query in list_v, check if the other endpoint is in root_u's component
            # Note: The query is stored as (q_idx, other_node)
            # If find(other_node) == root_u, then the query is completed.
            
            completed_queries = []
            
            for q_idx, other_node in list_v:
                # If the answer is already set (e.g., from same building case, though we filtered those), skip
                if answers[q_idx] != 0 or q_idx == -1: # -1 is a marker for processed
                    continue
                    
                # Check if other_node is in the component of root_u
                # Since we are merging, other_node might be in root_v's component or root_u's component already?
                # No, if it was in root_u's component, it would have been processed when that component was formed?
                # Actually, we only add queries to the endpoints.
                # If other_node is in root_u's component, then find(other_node) == root_u.
                # If other_node is in root_v's component, find(other_node) == root_v.
                # If other_node is in a third component, it's not connected yet.
                
                root_other = find(other_node)
                if root_other == root_u:
                    # Query is completed! The current edge weight w is the bottleneck.
                    answers[q_idx] = w
                    completed_queries.append(q_idx)
                elif root_other == root_v:
                    # This shouldn't happen for a valid query between two different nodes initially?
                    # If other_node is in root_v, it means both endpoints were in root_v?
                    # But we filtered u==v. And we process edges.
                    # If both were in root_v, they would have been connected earlier.
                    # So this case implies the query was already answered?
                    # Let's check if answer is set.
                    if answers[q_idx] != 0:
                        completed_queries.append(q_idx)
                    else:
                        # Should not happen if logic is correct
                        pass
                else:
                    # Not connected yet, keep in list
                    list_u.append((q_idx, other_node))
                    
            # Remove completed queries from list_u? 
            # We can just leave them and check answers[q_idx] != 0 later, 
            # but to keep list_u small, we should filter.
            # However, filtering is O(N). We can just rebuild list_u.
            
            # Filter list_u to remove completed queries
            new_list_u = []
            for q_idx, other_node in list_u:
                if answers[q_idx] == 0:
                    new_list_u.append((q_idx, other_node))
                # else: already answered, ignore
            list_u = new_list_u
            
            # Add remaining queries from list_v to list_u
            for q_idx, other_node in list_v:
                if answers[q_idx] == 0:
                    list_u.append((q_idx, other_node))
                    
            # Update the query_lists for the new root
            query_lists[root_u] = list_u
            # Clear the old root's list to save memory
            query_lists[root_v] = []
            
            # Perform union
            parent[root_v] = root_u
            
    # For any queries that are still not answered (should not happen if graph is connected)
    # The grid is always connected.
    # But let's double check.
    
    # Calculate final answers
    results = []
    for i in range(Q_count):
        # Retrieve original query to calculate cost
        # We need Y, Z, and the bottleneck B*
        # We stored answers[i] as B*
        B_star = answers[i]
        
        # We need Y and Z. Let's retrieve from queries list.
        # queries[i] is (A, B, Y, C, D, Z, original_idx)
        # Wait, the index in queries list is not necessarily original_idx.
        # We stored original_idx in the query tuple.
        # Let's find the query corresponding to i.
        # Actually, we can just iterate through queries again.
        pass
        
    # Re-iterate to compute final cost
    # We need to map original_idx to (Y, Z)
    # Let's create a map
    yz_map = {}
    for q in queries:
        # q is (r1, c1, Y, r2, c2, Z, original_idx)
        yz_map[q[6]] = (q[2], q[5])
        
    final_answers = []
    for i in range(Q_count):
        B_star = answers[i]
        Y, Z = yz_map[i]
        
        if B_star >= max(Y, Z):
            ans = abs(Y - Z)
        else:
            ans = abs(Y - B_star) + abs(Z - B_star)
        final_answers.append(str(ans))
        
    print('\n'.join(final_answers))

solve()