import sys

def solve():
    # Increase recursion depth just in case, though we'll use iterative BFS/DFS
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
        
    # A will store the final answer
    A = [0] * (N + 1)
    
    # visited array to keep track of processed nodes
    visited = [False] * (N + 1)
    
    # C[u] will store the relative XOR value from the root of the component
    # We can reuse a list or dict, but since we process component by component,
    # we can just store it in a temporary structure or directly in A if we handle K later.
    # Let's use a list for C values per component.
    
    for i in range(1, N + 1):
        if visited[i]:
            continue
            
        # Start BFS/DFS for this component
        component_nodes = []
        stack = [i]
        visited[i] = True
        # relative value for root is 0
        rel_val = {i: 0}
        component_nodes.append(i)
        
        is_consistent = True
        
        idx = 0
        while idx < len(component_nodes):
            u = component_nodes[idx]
            idx += 1
            cu = rel_val[u]
            
            for v, w in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    rel_val[v] = cu ^ w
                    component_nodes.append(v)
                else:
                    # Check consistency
                    if rel_val[v] != (cu ^ w):
                        print("-1")
                        return
        
        # Now optimize K for this component
        size = len(component_nodes)
        K = 0
        
        # Check bits 0 to 29 (since Z_i <= 10^9 < 2^30)
        for b in range(30):
            cnt_set = 0
            for node in component_nodes:
                if (rel_val[node] >> b) & 1:
                    cnt_set += 1
            
            # If we set bit b of K to 0: cost is cnt_set (1s remain 1s)
            # If we set bit b of K to 1: cost is size - cnt_set (1s become 0s, 0s become 1s)
            if cnt_set > size - cnt_set:
                # Keep bit 0, cost is cnt_set
                pass
            else:
                # Set bit 1, cost is size - cnt_set
                K |= (1 << b)
                
        # Assign final values
        for node in component_nodes:
            A[node] = rel_val[node] ^ K
            
    # Print result
    print(" ".join(str(A[i]) for i in range(1, N + 1)))

solve()