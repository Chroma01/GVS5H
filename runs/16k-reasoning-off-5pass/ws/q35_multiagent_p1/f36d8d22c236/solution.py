import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    t = input_data[2]
    
    # If S and T are already identical, 0 operations
    if s == t:
        print(0)
        return
    
    # Build the mapping from S chars to T chars
    # mapping[s_char] = t_char
    mapping = {}
    # To check injectivity on values (targets), we keep track of used targets
    used_targets = set()
    
    for i in range(n):
        sc = s[i]
        tc = t[i]
        
        if sc == tc:
            continue
            
        # If sc is already mapped, it must map to tc
        if sc in mapping:
            if mapping[sc] != tc:
                print(-1)
                return
        else:
            # If sc is not mapped, check if tc is already used by another source
            if tc in used_targets:
                # tc is already the target of some other s_char
                print(-1)
                return
            mapping[sc] = tc
            used_targets.add(tc)
            
    # Now we have a valid mapping. Count the number of operations.
    # The mapping defines a functional graph where each node has out-degree <= 1.
    # Since the mapping is injective on both keys and values (for the mapped nodes),
    # the graph is a collection of disjoint paths and cycles.
    # Each edge represents one operation.
    # However, if there is a cycle, we need one extra operation to break it.
    
    num_edges = len(mapping)
    
    # Detect if there is a cycle in the mapping graph
    # Nodes are characters 'a'-'z'. We only care about nodes that are in the mapping.
    # Since each node has out-degree <= 1, we can detect cycles by following the chain.
    
    has_cycle = False
    
    # We'll use a visited set to avoid reprocessing
    visited = set()
    
    for start_node in mapping:
        if start_node in visited:
            continue
            
        # Traverse the chain starting from start_node
        path = []
        curr = start_node
        while curr is not None and curr not in visited:
            visited.add(curr)
            path.append(curr)
            if curr in mapping:
                curr = mapping[curr]
            else:
                curr = None
                
        # If we ended at a node that is in the current path, we found a cycle
        # But since we mark visited globally, we need to check if the last node
        # we tried to visit was already in the current path.
        # Actually, the above loop stops when curr is None or curr is in visited.
        # If curr is in visited, it could be in the current path or a previously processed path.
        # If it's in the current path, we have a cycle.
        
        # Let's re-implement cycle detection more carefully.
        # We can use a state array: 0=unvisited, 1=visiting, 2=visited
        pass

    # Re-do cycle detection with proper states
    state = {} # 'a'-'z' -> 0, 1, 2
    for char in "abcdefghijklmnopqrstuvwxyz":
        state[char] = 0
        
    has_cycle = False
    for char in mapping:
        if state[char] == 0:
            curr = char
            while curr is not None and state[curr] == 0:
                state[curr] = 1
                if curr in mapping:
                    curr = mapping[curr]
                else:
                    curr = None
                    
            if curr is not None and state[curr] == 1:
                # Found a cycle
                has_cycle = True
                break
                
            # Mark all nodes in the path as visited (state 2)
            # We need to trace back or re-trace. Let's just do a second pass or store path.
            # Actually, we can just set state to 2 for all nodes we touched in this traversal.
            # But we didn't store the path. Let's store it.
            pass

    # Let's rewrite the cycle detection with path storage
    state = {c: 0 for c in "abcdefghijklmnopqrstuvwxyz"}
    has_cycle = False
    
    for start_node in mapping:
        if state[start_node] != 0:
            continue
            
        path = []
        curr = start_node
        while curr is not None and state[curr] == 0:
            state[curr] = 1
            path.append(curr)
            if curr in mapping:
                curr = mapping[curr]
            else:
                curr = None
                
        if curr is not None and state[curr] == 1:
            # Cycle detected
            has_cycle = True
            break
            
        # Mark all nodes in path as 2 (fully visited)
        for node in path:
            state[node] = 2
            
    if has_cycle:
        print(num_edges + 1)
    else:
        print(num_edges)

solve()