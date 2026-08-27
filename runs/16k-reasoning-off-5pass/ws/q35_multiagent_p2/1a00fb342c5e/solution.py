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
    
    # Adjacency list: adj[u] = [(v, z), ...]
    adj = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        z = int(next(iterator))
        adj[u].append((v, z))
        adj[v].append((u, z))
        
    # A array to store the final values
    A = [0] * (N + 1)
    # visited array to keep track of processed nodes
    visited = [False] * (N + 1)
    
    # For each component, we will store the list of nodes in it
    # and the relative XOR distance from the root of that component
    # relative_dist[u] = D_u such that A[u] = A[root] ^ D_u
    
    relative_dist = [0] * (N + 1)
    
    # Process each connected component
    for start_node in range(1, N + 1):
        if visited[start_node]:
            continue
            
        # Start a new component
        component_nodes = []
        stack = [start_node]
        visited[start_node] = True
        relative_dist[start_node] = 0
        component_nodes.append(start_node)
        
        # BFS/DFS to traverse the component and check consistency
        # Using a stack for DFS
        idx = 0
        while idx < len(component_nodes):
            u = component_nodes[idx]
            idx += 1
            
            for v, z in adj[u]:
                if not visited[v]:
                    visited[v] = True
                    relative_dist[v] = relative_dist[u] ^ z
                    component_nodes.append(v)
                else:
                    # Check for consistency
                    if relative_dist[v] != (relative_dist[u] ^ z):
                        print("-1")
                        return
        
        # Now optimize the root value for this component
        # The nodes in this component are in component_nodes
        # For each bit position k (0 to 29), decide the k-th bit of A[root]
        
        # We can compute the optimal root value by iterating bits
        root_val = 0
        
        # Precompute the bits of relative_dist for all nodes in component
        # To minimize sum, for each bit k, we want to choose root_bit_k such that
        # the total number of set bits at position k across all nodes in component is minimized.
        # If root_bit_k = 0, then A[u]'s bit k is relative_dist[u]'s bit k.
        # If root_bit_k = 1, then A[u]'s bit k is 1 ^ relative_dist[u]'s bit k.
        
        # Count how many nodes have bit k set in relative_dist
        # Let count_1 be the number of nodes where relative_dist[u] has bit k = 1
        # Let count_0 be the number of nodes where relative_dist[u] has bit k = 0
        # count_0 + count_1 = len(component_nodes)
        
        # If root_bit_k = 0: total set bits at k = count_1
        # If root_bit_k = 1: total set bits at k = count_0
        
        # We choose root_bit_k = 0 if count_1 <= count_0, else 1
        
        num_nodes = len(component_nodes)
        
        for k in range(30):
            count_1 = 0
            for u in component_nodes:
                if (relative_dist[u] >> k) & 1:
                    count_1 += 1
            
            count_0 = num_nodes - count_1
            
            if count_1 > count_0:
                root_val |= (1 << k)
                
        # Now set the actual values for all nodes in the component
        for u in component_nodes:
            A[u] = relative_dist[u] ^ root_val
            
    # Output the result for nodes 1 to N
    print(" ".join(str(A[i]) for i in range(1, N + 1)))

solve()