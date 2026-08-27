import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    s = input_data[1]
    t = input_data[2]
    
    # Check consistency: each char in S must map to exactly one char in T
    mapping = {}
    for i in range(n):
        u = s[i]
        v = t[i]
        if u in mapping:
            if mapping[u] != v:
                print(-1)
                return
        else:
            mapping[u] = v
            
    # Check injectivity: no two different chars in S map to the same char in T
    # i.e., the values in mapping must be unique
    mapped_values = set(mapping.values())
    if len(mapped_values) != len(mapping):
        print(-1)
        return
        
    # Build the functional graph and count non-self-loop edges
    # Nodes are characters 'a' to 'z'
    # Edges are mapping[u] = v for each u in mapping
    
    # Count non-self-loop edges
    non_self_loop_edges = 0
    for u, v in mapping.items():
        if u != v:
            non_self_loop_edges += 1
            
    # Check for cycles in the functional graph
    # The graph consists of nodes that are keys in mapping, with edges u -> mapping[u]
    # We need to detect if there's any cycle in this graph
    
    # To detect cycles, we can use DFS or simply check if the graph has cycles
    # Since it's a functional graph (each node has at most one outgoing edge),
    # we can trace paths.
    
    # Let's identify all nodes involved in the graph
    nodes = set(mapping.keys())
    
    # We'll use a visited array to detect cycles
    # States: 0 = unvisited, 1 = visiting, 2 = visited
    state = {node: 0 for node in nodes}
    has_cycle = False
    
    def dfs(node):
        nonlocal has_cycle
        if has_cycle:
            return
        state[node] = 1
        next_node = mapping.get(node)
        if next_node is not None:
            if state[next_node] == 1:
                # Found a cycle
                has_cycle = True
                return
            elif state[next_node] == 0:
                dfs(next_node)
        state[node] = 2
    
    for node in nodes:
        if state[node] == 0:
            dfs(node)
        if has_cycle:
            break
            
    # If there's a cycle, we need a spare character to break it
    # A spare character exists if not all 26 lowercase letters are in S
    # Actually, we need a character that is not in the domain of the mapping
    # i.e., not present in S at all, or more precisely, not involved in the cycle
    # But the standard condition is: if there's a cycle and all 26 chars are used in S,
    # then we can't break the cycle.
    
    if has_cycle:
        # Check if all 26 lowercase letters are present in S
        distinct_s = set(s)
        if len(distinct_s) == 26:
            print(-1)
        else:
            # We have a spare character, so we can break the cycle with one extra operation
            print(non_self_loop_edges + 1)
    else:
        print(non_self_loop_edges)

solve()