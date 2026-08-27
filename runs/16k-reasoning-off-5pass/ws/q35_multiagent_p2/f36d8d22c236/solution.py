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
    # Map from character in S to character in T
    mapping = {}
    
    # Also keep track of which characters in T are targets of multiple sources
    # to check injectivity (though the problem allows multiple sources to map to same target,
    # it does NOT allow one source to map to multiple targets).
    # Actually, the constraint is: if S[i] == S[j], then T[i] must equal T[j].
    # This means the mapping from S-char to T-char must be a well-defined function.
    
    for i in range(n):
        char_s = s[i]
        char_t = t[i]
        
        if char_s in mapping:
            if mapping[char_s] != char_t:
                print("-1")
                return
        else:
            mapping[char_s] = char_t

    # Step 2: Build the functional graph and count edges/cycles
    # The graph nodes are the unique characters present in S.
    # Edges are defined by the mapping: u -> mapping[u]
    
    # We only care about characters that are in S.
    unique_s_chars = set(mapping.keys())
    
    # Count non-identity edges (edges where u != mapping[u])
    edges = 0
    for u in unique_s_chars:
        if u != mapping[u]:
            edges += 1
            
    # Count cycles in the functional graph
    # A cycle is a sequence u1 -> u2 -> ... -> uk -> u1 where all ui are distinct
    # and ui != mapping[ui] (since self-loops are not counted as cycles in this context)
    # Actually, self-loops are not cycles for the purpose of the +1 cost.
    # We need to count the number of disjoint cycles in the graph formed by edges u -> mapping[u]
    # where u != mapping[u].
    
    visited = set()
    cycles = 0
    
    for start_node in unique_s_chars:
        if start_node in visited:
            continue
        if start_node == mapping.get(start_node, start_node):
            # Self-loop, not a cycle for our cost calculation
            visited.add(start_node)
            continue
            
        # Traverse the path from start_node
        path = []
        curr = start_node
        while curr not in visited and curr in mapping and curr != mapping[curr]:
            visited.add(curr)
            path.append(curr)
            curr = mapping[curr]
            
        # If we hit a node that is already visited in the current path, we found a cycle
        if curr in path:
            # Find the start of the cycle in the path
            cycle_start_index = path.index(curr)
            cycle_nodes = path[cycle_start_index:]
            cycles += 1
            
        # Mark all nodes in the path as visited
        for node in path:
            visited.add(node)
            
    # Step 3: Calculate the answer
    # The minimum number of operations is edges + cycles
    ans = edges + cycles
    print(ans)

if __name__ == '__main__':
    solve()