import sys

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    N = int(next(iterator))
    M = int(next(iterator))
    A = [0] * (N + 1)
    for i in range(1, N + 1):
        A[i] = int(next(iterator))

    MOD = 998244353

    # Build the graph: each node i has an edge to A[i]
    # We need to find components and cycles.
    # Since each node has out-degree 1, we can use visited arrays to find cycles.
    
    # Step 1: Identify which nodes are in cycles and which are not.
    # Also, for each node, we need to know its children in the "tree" sense.
    # The graph edges are i -> A[i]. So if we reverse the edges, we get trees rooted at cycle nodes.
    
    # Reverse graph: children[u] contains all v such that A[v] == u
    children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        children[A[i]].append(i)
        
    # Find cycles using DFS or iterative traversal
    visited = [0] * (N + 1)  # 0: unvisited, 1: visiting, 2: visited
    in_cycle = [False] * (N + 1)
    cycle_nodes = []
    
    # We'll process each component
    # To find cycles, we can iterate through each node and follow the path until we hit a visited node.
    
    # First, let's mark all nodes that are part of cycles.
    # We can do this by computing in-degrees in the functional graph and peeling off trees.
    # But since N is small, we can just use the standard cycle detection.
    
    # Let's use a simpler approach: for each unvisited node, traverse until we find a node that is either in current path or already processed.
    
    # Actually, let's use the in-degree peeling method to identify cycle nodes.
    in_degree = [0] * (N + 1)
    for i in range(1, N + 1):
        in_degree[A[i]] += 1
        
    queue = []
    for i in range(1, N + 1):
        if in_degree[i] == 0:
            queue.append(i)
            
    # Peel off non-cycle nodes
    while queue:
        u = queue.pop(0)
        in_cycle[u] = False
        v = A[u]
        in_degree[v] -= 1
        if in_degree[v] == 0:
            queue.append(v)
            
    # All nodes not marked as peeled are in cycles
    for i in range(1, N + 1):
        if not in_cycle[i]:
            in_cycle[i] = True
            
    # Now, for each node, we need to compute W(u, v) and S(u, v).
    # W(u, v) = number of ways to assign values to the subtree rooted at u (in the reversed graph, i.e., trees directed towards cycle)
    # such that x_u = v.
    # S(u, v) = sum_{k=1}^v W(u, k)
    
    # We process nodes in reverse topological order (leaves to roots).
    # Since we've peeled the trees, we can process nodes in decreasing order of their "depth" from the cycle.
    # Alternatively, we can use the fact that after peeling, the remaining nodes are in cycles, and the peeled nodes form trees.
    # We can process the peeled nodes in the order they were peeled (which is from leaves to roots towards the cycle).
    
    # Let's create a list of nodes in the order they were peeled.
    peeled_order = []
    # Re-run the peeling to get the order
    in_degree2 = [0] * (N + 1)
    for i in range(1, N + 1):
        in_degree2[A[i]] += 1
        
    queue2 = []
    for i in range(1, N + 1):
        if in_degree2[i] == 0:
            queue2.append(i)
            
    while queue2:
        u = queue2.pop(0)
        peeled_order.append(u)
        v = A[u]
        in_degree2[v] -= 1
        if in_degree2[v] == 0:
            queue2.append(v)
            
    # Now, peeled_order contains all non-cycle nodes in topological order (leaves first).
    # Cycle nodes are those not in peeled_order.
    
    # Initialize W and S arrays
    # W[u][v] for u in 1..N, v in 1..M
    # S[u][v] for u in 1..N, v in 1..M
    
    # We'll use 1-indexed for v, so size M+1
    W = [[0] * (M + 1) for _ in range(N + 1)]
    S = [[0] * (M + 1) for _ in range(N + 1)]
    
    # Process peeled nodes in order (leaves to roots)
    for u in peeled_order:
        # For a leaf in the tree part, W[u][v] = 1 for all v
        # But if u has children in the reversed graph, we need to compute based on children.
        # Note: children[u] contains all v such that A[v] == u. These are the children in the tree rooted at u.
        # Since we process in topological order, all children of u have been processed.
        
        # Compute W[u][v] for each v
        # W[u][v] = product over c in children[u] of S[c][v]
        
        # Start with W[u][v] = 1 for all v
        for v in range(1, M + 1):
            W[u][v] = 1
            
        for c in children[u]:
            for v in range(1, M + 1):
                W[u][v] = (W[u][v] * S[c][v]) % MOD
                
        # Compute S[u][v] = S[u][v-1] + W[u][v]
        S[u][1] = W[u][1]
        for v in range(2, M + 1):
            S[u][v] = (S[u][v-1] + W[u][v]) % MOD
            
    # Now process cycle nodes.
    # For cycle nodes, we need to compute W[u][v] similarly, but note that the cycle edges are not included in the tree structure.
    # The children of a cycle node in the tree part are all nodes v such that A[v] == u and v is not in the cycle.
    # But wait, our children list includes all v such that A[v] == u, including other cycle nodes.
    # We need to exclude cycle neighbors when computing W for cycle nodes.
    
    # Let's identify the cycle structure for each component.
    # We'll group cycle nodes by component.
    
    # First, let's compute W[u][v] for cycle nodes, but only considering non-cycle children.
    # We can do this by initializing W[u][v] = 1 and then multiplying by S[c][v] for c in children[u] if c is not in cycle.
    
    cycle_nodes_list = [i for i in range(1, N + 1) if in_cycle[i]]
    
    # For each cycle node, compute W[u][v] considering only non-cycle children
    for u in cycle_nodes_list:
        for v in range(1, M + 1):
            W[u][v] = 1
            
        for c in children[u]:
            if not in_cycle[c]:
                for v in range(1, M + 1):
                    W[u][v] = (W[u][v] * S[c][v]) % MOD
                    
        # Compute S[u][v] for cycle nodes as well, though it's not directly used for the cycle product,
        # but it might be needed if a cycle node is a child of another cycle node? No, in a functional graph,
        # cycle nodes only point to other cycle nodes. So the tree part of a cycle node only includes non-cycle nodes.
        # So we don't need S for cycle nodes for the purpose of computing other W values.
        # But let's compute it anyway for consistency.
        S[u][1] = W[u][1]
        for v in range(2, M + 1):
            S[u][v] = (S[u][v-1] + W[u][v]) % MOD
            
    # Now, for each component, find the cycle and compute the product of W[c][v] for all c in the cycle.
    # Then sum over v.
    
    # Group cycle nodes by component.
    # We can do this by traversing the cycle for each unvisited cycle node.
    
    visited_cycle = [False] * (N + 1)
    total_answer = 0
    
    for start_node in cycle_nodes_list:
        if visited_cycle[start_node]:
            continue
            
        # Find the cycle starting from start_node
        cycle = []
        curr = start_node
        while not visited_cycle[curr]:
            visited_cycle[curr] = True
            cycle.append(curr)
            curr = A[curr]
            # We should return to start_node to complete the cycle
            if curr == start_node:
                break
                
        # Now, for each v from 1 to M, compute the product of W[c][v] for c in cycle
        # Then sum these products.
        
        for v in range(1, M + 1):
            prod = 1
            for c in cycle:
                prod = (prod * W[c][v]) % MOD
            total_answer = (total_answer + prod) % MOD
            
    print(total_answer)

solve()