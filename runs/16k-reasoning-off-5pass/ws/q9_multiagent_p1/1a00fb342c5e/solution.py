import sys

# Increase recursion depth just in case, though we use iterative BFS
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        M = int(next(iterator))
    except StopIteration:
        return

    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        adj[u].append((v, w))
        adj[v].append((u, w))

    # Array to store the value of each node relative to the root of its component (root=0)
    # Initialize with -1 to represent unvisited
    base_A = [-1] * (N + 1)
    
    # First pass: Check consistency and assign relative values
    # We use BFS to avoid recursion depth issues
    for i in range(1, N + 1):
        if base_A[i] == -1:
            # Start a new component
            base_A[i] = 0
            queue = [i]
            idx = 0
            
            while idx < len(queue):
                u = queue[idx]
                idx += 1
                
                current_val = base_A[u]
                
                for v, w in adj[u]:
                    expected_val = current_val ^ w
                    if base_A[v] == -1:
                        base_A[v] = expected_val
                        queue.append(v)
                    else:
                        if base_A[v] != expected_val:
                            print("-1")
                            return

    # Second pass: Minimize the sum for each component
    # We need to determine the optimal 'flip' value X for each component
    # such that sum(base_A[v] ^ X) is minimized for all v in the component.
    # This is done bit by bit.
    
    final_A = [0] * (N + 1)
    
    # We need to process each component again to group nodes
    visited_second = [False] * (N + 1)
    
    for i in range(1, N + 1):
        if not visited_second[i]:
            # Start collecting component
            component_nodes = []
            queue = [i]
            visited_second[i] = True
            component_nodes.append(i)
            
            idx = 0
            while idx < len(queue):
                u = queue[idx]
                idx += 1
                
                for v, w in adj[u]:
                    if not visited_second[v]:
                        visited_second[v] = True
                        queue.append(v)
                        component_nodes.append(v)
            
            # Now we have all nodes in this component.
            # Determine optimal X for this component.
            # X is constructed bit by bit.
            X = 0
            
            # Check bits 0 to 29 (since Z_i <= 10^9 < 2^30)
            for b in range(30):
                count_0 = 0
                count_1 = 0
                
                for node in component_nodes:
                    val = base_A[node]
                    if (val >> b) & 1:
                        count_1 += 1
                    else:
                        count_0 += 1
                
                # If X_bit = 0: cost is count_1 (since 0^1=1)
                # If X_bit = 1: cost is count_0 (since 1^0=1)
                # We want min(count_1, count_0).
                # If count_1 < count_0, we prefer X_bit = 0.
                # If count_1 >= count_0, we prefer X_bit = 1.
                
                if count_1 < count_0:
                    # Keep bit 0
                    pass
                else:
                    # Set bit 1
                    X |= (1 << b)
            
            # Apply X to all nodes in the component
            for node in component_nodes:
                final_A[node] = base_A[node] ^ X

    # Output the result
    print(*(final_A[1:]))

if __name__ == '__main__':
    solve()