import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    s = input_data[1]
    t = input_data[2]

    # Step 1: Check feasibility and build the mapping
    mapping = {}
    # mapping[char_in_s] = char_in_t
    
    # We also need to track which characters are present in S
    chars_in_s = set()
    
    for i in range(n):
        u = s[i]
        v = t[i]
        chars_in_s.add(u)
        
        if u in mapping:
            if mapping[u] != v:
                # Conflict: same source char maps to different target chars
                print(-1)
                return
        else:
            mapping[u] = v

    # Step 2: Build the graph and find cycles
    # The graph nodes are characters 'a'-'z'
    # Edges are u -> mapping[u] for u in mapping
    
    # We only care about edges where u != v, because u->u requires 0 ops
    # and doesn't form a cycle that needs breaking.
    
    # Identify all unique edges where u != v
    edges = []
    for u, v in mapping.items():
        if u != v:
            edges.append((u, v))
            
    if not edges:
        print(0)
        return

    # Build adjacency list for the graph of these edges
    # Since it's a functional graph (each node has out-degree <= 1),
    # we can just use a dict for next_node.
    next_node = {}
    for u, v in edges:
        next_node[u] = v
        
    # Find cycles
    # We iterate through all nodes that are part of the edges
    visited = set()
    has_cycle = False
    
    # We need to detect cycles in the functional graph defined by next_node
    # Nodes involved are keys in next_node
    
    for start_node in next_node:
        if start_node in visited:
            continue
            
        # Traverse the path from start_node
        path = []
        curr = start_node
        while curr is not None and curr not in visited:
            visited.add(curr)
            path.append(curr)
            if curr in next_node:
                curr = next_node[curr]
            else:
                curr = None
        
        # If we hit a node that is in the current path, we found a cycle
        # Check if curr is in path
        if curr is not None and curr in path:
            cycle_start_index = path.index(curr)
            cycle = path[cycle_start_index:]
            if len(cycle) > 0:
                has_cycle = True
                # We don't need to count the cycle length specifically for the formula
                # The formula is: Total Ops = (Number of edges where u!=v) - (1 if free char exists and has_cycle else 0)
                # So we just need to know if there is ANY cycle.
                break
        else:
            # No cycle found in this component, mark all as visited
            pass

    # Step 3: Check for free character
    # A free character is one that does not appear in S at all.
    # This allows us to use it as a temporary buffer to break one cycle.
    all_chars = set("abcdefghijklmnopqrstuvwxyz")
    free_char_exists = len(all_chars - chars_in_s) > 0
    
    # Step 4: Calculate answer
    num_edges = len(edges)
    ans = num_edges
    
    if has_cycle and free_char_exists:
        ans -= 1
        
    print(ans)

solve()