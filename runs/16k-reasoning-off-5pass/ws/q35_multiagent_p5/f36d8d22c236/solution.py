import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    N = int(input_data[0])
    S = input_data[1]
    T = input_data[2]
    
    # Step 1: Check feasibility
    # Build mapping from S-char to T-char
    mapping = {}
    for s_char, t_char in zip(S, T):
        if s_char in mapping:
            if mapping[s_char] != t_char:
                print(-1)
                return
        else:
            mapping[s_char] = t_char
            
    # Step 2: Build the graph and count operations
    # We only care about characters in S that need to change
    # Graph: directed edge from u to v if mapping[u] = v and u != v
    
    # Identify characters present in S
    chars_in_S = set(S)
    
    # Count K: number of characters c in S such that mapping[c] != c
    K = 0
    # Build adjacency for the functional graph (only for chars in S that map to something else)
    # Since it's a functional graph (each node has at most one outgoing edge),
    # we can just store the target.
    graph = {}
    for s_char in chars_in_S:
        t_char = mapping[s_char]
        if s_char != t_char:
            K += 1
            graph[s_char] = t_char
            
    # Step 3: Check for cycles in the graph
    # The graph is a collection of components, each being a set of trees rooted on a cycle,
    # or just a tree leading to a node not in the graph (but since we only include nodes that map to something else,
    # and the target might be in S or not. If the target is not in S, it's not in graph, so no cycle involving it).
    # Actually, if mapping[u] = v and v is not in chars_in_S, then v is not in graph, so u has no outgoing edge in graph?
    # Wait, we added u -> v to graph only if u != v. But if v is not in chars_in_S, then v is not a key in graph.
    # So the graph only contains nodes from chars_in_S that need to change.
    # A cycle exists if we can start from a node and follow edges back to itself.
    
    has_cycle = False
    visited = set()
    rec_stack = set()
    
    def has_cycle_dfs(node, visited, rec_stack, graph):
        visited.add(node)
        rec_stack.add(node)
        
        if node in graph:
            next_node = graph[node]
            if next_node not in visited:
                if has_cycle_dfs(next_node, visited, rec_stack, graph):
                    return True
            elif next_node in rec_stack:
                return True
                
        rec_stack.remove(node)
        return False
        
    for node in list(graph.keys()):
        if node not in visited:
            if has_cycle_dfs(node, visited, rec_stack, graph):
                has_cycle = True
                break
                
    # Step 4: Determine answer
    # If there is a cycle, we need an extra operation unless we have a dummy character.
    # A dummy character is one that is not in S.
    all_chars = set("abcdefghijklmnopqrstuvwxyz")
    dummy_available = (all_chars - chars_in_S) != set()
    
    if has_cycle and not dummy_available:
        print(K + 1)
    else:
        print(K)

solve()