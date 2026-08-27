import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(300005)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        X = int(next(iterator))
        
        A = []
        for _ in range(N):
            A.append(int(next(iterator)))
            
        B = []
        for _ in range(N):
            B.append(int(next(iterator)))
            
        P = []
        for _ in range(N):
            P.append(int(next(iterator)) - 1) # Convert to 0-based index
            
        Q = []
        for _ in range(N):
            Q.append(int(next(iterator)) - 1) # Convert to 0-based index
            
    except StopIteration:
        return

    # Helper to find the cycle containing a specific node in a permutation
    # and check if all balls of that color are in that cycle.
    def get_cycle_and_check(start_node, next_node_func, balls_array):
        visited = [False] * N
        cycle_nodes = []
        curr = start_node
        
        # Traverse to find the cycle containing start_node
        # In a permutation, following edges from any node must eventually return to it.
        while not visited[curr]:
            visited[curr] = True
            cycle_nodes.append(curr)
            curr = next_node_func[curr]
            
        # In a permutation graph, the component containing start_node is a simple cycle.
        # The loop stops exactly when we hit a visited node. Since we mark nodes as we go,
        # the first visited node we encounter MUST be start_node.
        # If we hit a node visited in a previous run of this function, it would be an issue,
        # but here we create a fresh visited array each time.
        # So the cycle is correctly identified.
        
        # Check if all balls are in the cycle containing X
        for i in range(N):
            if balls_array[i] == 1:
                if i not in cycle_nodes:
                    return None, False # Impossible
        
        return cycle_nodes, True

    # Find cycle for P (Red balls)
    # P[i] is the destination of red ball from box i
    p_cycle, p_valid = get_cycle_and_check(X - 1, P, A)
    
    if not p_valid:
        print("-1")
        return

    # Find cycle for Q (Blue balls)
    # Q[i] is the destination of blue ball from box i
    q_cycle, q_valid = get_cycle_and_check(X - 1, Q, B)
    
    if not q_valid:
        print("-1")
        return

    # The set of boxes to operate on is (p_cycle - {X}) U (q_cycle - {X})
    # Since X is 0-based index X-1
    target_idx = X - 1
    
    # Create sets for efficient union
    red_ops = set(p_cycle)
    red_ops.discard(target_idx)
    
    blue_ops = set(q_cycle)
    blue_ops.discard(target_idx)
    
    total_ops = len(red_ops | blue_ops)
    
    print(total_ops)

if __name__ == '__main__':
    solve()