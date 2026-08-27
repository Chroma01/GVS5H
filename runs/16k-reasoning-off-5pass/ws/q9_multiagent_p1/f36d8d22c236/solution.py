import sys

# Increase recursion depth just in case, though iterative approach is preferred
sys.setrecursionlimit(3000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    # Map to store the required transformation for each character
    # mapping[char] = target_char
    mapping = {}
    
    # Check consistency and build the mapping
    # Since N can be up to 2*10^5, we iterate once.
    # We only care about characters present in S.
    for i in range(N):
        s_char = S[i]
        t_char = T[i]
        
        if s_char in mapping:
            if mapping[s_char] != t_char:
                print("-1")
                return
        else:
            mapping[s_char] = t_char

    # Identify characters that need to change (mapping[c] != c)
    # These are the nodes in our functional graph that are part of the transformation
    nodes_to_change = []
    for char in mapping:
        if mapping[char] != char:
            nodes_to_change.append(char)
    
    # If no characters need to change, 0 operations
    if not nodes_to_change:
        print("0")
        return

    # Build the graph for nodes_to_change
    # We only care about the subgraph induced by nodes_to_change
    # However, a node might map to a node that is NOT in nodes_to_change (e.g., a->a, but a is in nodes_to_change? No, if a->a, it's not in nodes_to_change)
    # Wait, if mapping[c] != c, then c is in nodes_to_change.
    # The target mapping[c] could be a character that is NOT in nodes_to_change?
    # If mapping[c] == d, and d is not in nodes_to_change, it means mapping[d] == d.
    # So d is a fixed point.
    # In the functional graph, edges go from c -> d.
    # We need to count cycles in this graph.
    
    # Let's construct the adjacency list for the relevant nodes
    # Nodes are 'a'-'z'. We can use an array of size 26.
    
    # visited array: 0 = unvisited, 1 = visiting (in current path), 2 = visited (processed)
    visited = {c: 0 for c in mapping}
    cycle_count = 0
    
    # We only need to traverse starting from nodes in nodes_to_change
    # But a cycle might be reachable from a node not in nodes_to_change?
    # No, if a node is not in nodes_to_change, it maps to itself (fixed point).
    # A fixed point cannot be part of a cycle of length >= 2.
    # So we only need to traverse from nodes_to_change.
    
    for start_node in nodes_to_change:
        if visited[start_node] != 0:
            continue
            
        path = []
        curr = start_node
        is_cycle = False
        
        while visited[curr] == 0:
            visited[curr] = 1
            path.append(curr)
            next_node = mapping[curr]
            
            # If next_node is not in the mapping keys, it means it's not in S?
            # But mapping is built from S. So next_node must be in mapping keys?
            # Wait, mapping keys are characters present in S.
            # If mapping[curr] = next_node, then next_node is the target in T.
            # Does next_node have to be in S? Not necessarily.
            # If next_node is not in S, then mapping[next_node] is undefined.
            # But if next_node is not in S, it means it never appears as a source.
            # So it cannot be part of a cycle (since a cycle requires every node to have an outgoing edge).
            # So if next_node is not in mapping, we stop.
            
            if next_node not in mapping:
                break
                
            curr = next_node
            
            if visited[curr] == 1:
                # Cycle detected
                is_cycle = True
                break
            elif visited[curr] == 2:
                # Merged into a previously processed component
                break
        
        if is_cycle:
            cycle_count += 1
            
        # Mark all nodes in path as visited (2)
        for node in path:
            visited[node] = 2

    # The number of operations is the number of unique characters that need to change
    # plus the number of cycles.
    # Why?
    # For a DAG (no cycles), we can topologically sort and process from sinks to sources.
    # Each edge (u -> v) where u != v requires 1 operation.
    # Total ops = number of edges = number of nodes in nodes_to_change.
    # For a cycle of length L, we need L+1 operations (L to break the cycle using a dummy, 
    # effectively turning the cycle into a DAG structure or resolving dependencies).
    # Actually, the logic derived was: Ops = |nodes_to_change| + number_of_cycles.
    
    ans = len(nodes_to_change) + cycle_count
    print(ans)

if __name__ == '__main__':
    solve()