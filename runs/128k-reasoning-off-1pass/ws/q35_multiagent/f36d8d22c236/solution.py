import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    T = input_data[2]
    
    # Step 1: Check consistency and build mapping
    mapping = {}
    for s_char, t_char in zip(S, T):
        if s_char in mapping:
            if mapping[s_char] != t_char:
                print(-1)
                return
        else:
            mapping[s_char] = t_char
            
    # Step 2: Build the graph and count edges
    # Graph is a set of edges (u, v) where u != v
    edges = []
    for u, v in mapping.items():
        if u != v:
            edges.append((u, v))
            
    m = len(edges)
    
    # If no edges needed, 0 operations
    if m == 0:
        print(0)
        return
        
    # Step 3: Detect cycles in the functional graph
    # The graph has nodes that are characters in the mapping keys or values
    # Since each node has out-degree <= 1, we can detect cycles by traversal
    
    # Build adjacency list for the graph
    adj = {}
    for u, v in edges:
        adj[u] = v
        
    # Find all nodes involved in the graph
    nodes = set(adj.keys()) | set(adj.values())
    
    visited = set()
    has_cycle = False
    
    for start_node in nodes:
        if start_node in visited:
            continue
            
        # Traverse from start_node
        path = []
        curr = start_node
        while curr is not None and curr not in visited:
            visited.add(curr)
            path.append(curr)
            curr = adj.get(curr, None)
            
        # If we hit a node that is in the current path, we found a cycle
        if curr is not None and curr in path:
            has_cycle = True
            break
            
    # Step 4: Determine if there's a spare character
    # A spare character is one that is not in T
    chars_in_T = set(T)
    has_spare = len(chars_in_T) < 26
    
    # Step 5: Calculate answer
    if has_cycle:
        if has_spare:
            print(m + 1)
        else:
            print(-1)
    else:
        print(m)

solve()