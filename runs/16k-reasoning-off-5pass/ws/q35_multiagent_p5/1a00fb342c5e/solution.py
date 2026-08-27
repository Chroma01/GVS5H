import sys

def solve():
    # Increase recursion depth just in case, though we will use iterative BFS/DFS
    sys.setrecursionlimit(300000)
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    N = int(next(iterator))
    M = int(next(iterator))
    
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        adj[u].append((v, w))
        adj[v].append((u, w))
        
    # visited array to keep track of processed nodes
    # We store the relative value R_i for each node
    # R_i is such that A_i = R_i ^ C_component
    # Initially, we don't know C_component, so we just store R_i relative to the root of the component
    # We use -1 to indicate unvisited
    rel_val = [-1] * (N + 1)
    
    # To store the final answer
    ans = [0] * (N + 1)
    
    # We'll process each connected component
    for i in range(1, N + 1):
        if rel_val[i] != -1:
            continue
            
        # Start a new component
        # Use a stack for DFS or queue for BFS. Let's use a list as a stack for DFS
        stack = [i]
        rel_val[i] = 0
        component_nodes = [i]
        
        # BFS/DFS to propagate values
        # Using a list as a queue for BFS to avoid recursion depth issues
        queue = [i]
        idx = 0
        while idx < len(queue):
            u = queue[idx]
            idx += 1
            
            for v, w in adj[u]:
                if rel_val[v] == -1:
                    rel_val[v] = rel_val[u] ^ w
                    component_nodes.append(v)
                    queue.append(v)
                else:
                    # Check consistency
                    if rel_val[v] != (rel_val[u] ^ w):
                        print("-1")
                        return

        # Now we have all nodes in the component and their relative values
        # We need to find the optimal constant C for this component
        # A_j = rel_val[j] ^ C
        # We want to minimize sum(A_j) = sum(rel_val[j] ^ C)
        
        # Determine the maximum possible bit we need to consider
        # Z_i <= 10^9 < 2^30, so 30 bits are enough (0 to 29)
        # However, rel_val can be larger if paths are long? 
        # No, XOR sum of values <= 10^9 will not exceed 2^30 - 1 roughly.
        # Let's check up to 31 bits to be safe (up to 2^30)
        
        size = len(component_nodes)
        optimal_C = 0
        
        for bit in range(31):
            cnt_set = 0
            for node in component_nodes:
                if (rel_val[node] >> bit) & 1:
                    cnt_set += 1
            
            cnt_unset = size - cnt_set
            
            # If we set bit of C to 0: contribution is cnt_set * 2^bit
            # If we set bit of C to 1: contribution is cnt_unset * 2^bit
            if cnt_unset < cnt_set:
                optimal_C |= (1 << bit)
                
        # Apply the optimal C to all nodes in the component
        for node in component_nodes:
            ans[node] = rel_val[node] ^ optimal_C
            
    # Print the result
    print(" ".join(map(str, ans[1:])))

solve()