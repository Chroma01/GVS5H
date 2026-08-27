import sys

# Increase recursion depth just in case, though iterative approach is preferred
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n_str = next(iterator)
        N = int(n_str)
        S = next(iterator)
        T = next(iterator)
    except StopIteration:
        return

    # Step 1: Check consistency
    # If S[i] == S[j], then T[i] must equal T[j]
    # We can do this by mapping each character in S to its required character in T
    # If a character in S maps to different characters in T, it's impossible.
    
    mapping = {}
    for i in range(N):
        s_char = S[i]
        t_char = T[i]
        
        if s_char in mapping:
            if mapping[s_char] != t_char:
                print("-1")
                return
        else:
            mapping[s_char] = t_char
            
    # Step 2: Build the functional graph and check for cycles of length > 1
    # The nodes are the characters present in S.
    # An edge exists from u to v if mapping[u] == v.
    # Since each node has at most one outgoing edge, the graph is a collection of functional components.
    # A component consists of a set of trees rooted on a cycle.
    # If there is a cycle of length > 1, it is impossible to satisfy the requirements because
    # operations merge characters, and we cannot separate them later.
    
    # We only care about characters that are in S.
    unique_s_chars = set(S)
    
    visited = set()
    possible = True
    
    # We use an iterative approach to detect cycles
    # For each node in unique_s_chars, if not visited, trace the path.
    for start_node in unique_s_chars:
        if start_node in visited:
            continue
            
        path = []
        curr = start_node
        
        while curr is not None:
            if curr in visited:
                # Merged into a previously processed component (tree leading to a visited node)
                # No new cycle detected here.
                break
            elif curr in path:
                # Cycle detected within the current path
                # Check if the cycle length is > 1
                cycle_start_idx = path.index(curr)
                cycle_len = len(path) - cycle_start_idx
                
                if cycle_len > 1:
                    possible = False
                    break
                else:
                    # Cycle length 1 (self loop), which is fine.
                    # We stop tracing this component.
                    break
            else:
                path.append(curr)
                next_node = mapping.get(curr)
                if next_node is None:
                    # Should not happen if we only iterate unique_s_chars and mapping is defined for them
                    break
                curr = next_node
        
        # Mark all nodes in path as visited
        for node in path:
            visited.add(node)
            
        if not possible:
            break
            
    if not possible:
        print("-1")
        return

    # Step 3: Calculate minimum operations
    # The minimum number of operations is the number of unique characters in S
    # that are not equal to their target character.
    # Why? Because each such character u requires a path u -> ... -> mapping[u].
    # Since there are no cycles > 1, the graph is a DAG (of components rooted at fixed points).
    # The number of edges needed is exactly the number of nodes with out-degree > 0 in the requirement graph.
    
    ops = 0
    for char in unique_s_chars:
        if mapping[char] != char:
            ops += 1
            
    print(ops)

if __name__ == '__main__':
    solve()