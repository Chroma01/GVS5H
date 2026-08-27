import sys

# Increase recursion depth just in case, though we will use iterative approaches where possible
sys.setrecursionlimit(5000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = [int(next(iterator)) for _ in range(N)]
    except StopIteration:
        return

    MOD = 998244353

    # Build the graph
    # A[i] is the node that i points to. Note: input is 1-indexed, convert to 0-indexed.
    # adj[i] = A[i] - 1
    adj = [a - 1 for a in A]
    
    # Reverse graph to identify trees rooted on cycles
    # rev_adj[u] contains list of v such that v -> u
    rev_adj = [[] for _ in range(N)]
    for i in range(N):
        rev_adj[adj[i]].append(i)

    # Step 1: Detect cycles and identify which nodes are in cycles
    # We can use a visited array and process each component
    visited = [False] * N
    in_cycle = [False] * N
    cycle_node_values = [0] * N # Will store the value v for the cycle if we were to fix it, but we compute DP
    
    # To find cycles, we can use a standard DFS or iterative path following
    # Since it's a functional graph, each component has exactly one cycle.
    
    # Let's identify all nodes that are part of any cycle
    # We can do this by computing in-degrees and peeling off trees (Kahn's algorithm style)
    in_degree = [0] * N
    for i in range(N):
        in_degree[adj[i]] += 1
        
    queue = [i for i in range(N) if in_degree[i] == 0]
    while queue:
        u = queue.pop(0)
        in_cycle[u] = False # Mark as not in cycle (it's a tree node)
        v = adj[u]
        in_degree[v] -= 1
        if in_degree[v] == 0:
            queue.append(v)
            
    # Nodes with in_degree > 0 are part of cycles
    for i in range(N):
        if in_degree[i] > 0:
            in_cycle[i] = True
            
    # Step 2: Process each component
    # We need to compute DP[u][v] for each node u, which is the number of ways to assign the subtree at u
    # given that x_u = v.
    # The subtree at u consists of u and all nodes that eventually point to u (in the reverse graph sense, 
    # i.e., descendants in the tree rooted at u in the reverse graph, but only tree nodes, not cycle nodes).
    # Actually, the "subtree" for DP purposes is the set of nodes that have u as an ancestor in the dependency chain.
    # Since edges are i -> A[i], the dependency is x_i <= x_{A[i]}.
    # So for a node u, its children in the DP tree are nodes v such that A[v] = u.
    # These are exactly rev_adj[u].
    # However, we must be careful: if u is in a cycle, its "children" in the DP tree are the tree nodes attached to it.
    # The cycle nodes themselves are handled by the cycle constraint.
    
    # We will compute DP[u][v] for all u and v in 1..M.
    # DP[u][v] = product over c in rev_adj[u] of (sum_{k=1}^v DP[c][k])
    # Note: This formula applies to tree nodes. For cycle nodes, we will compute a separate value.
    # Actually, the formula is the same for all nodes if we consider the "subtree" to be the tree attached to u.
    # If u is in a cycle, the "subtree" at u consists of u and all tree nodes that eventually point to u.
    # But wait, the cycle nodes are contracted. So for a cycle node u, DP[u][v] should represent the number of ways
    # to assign the tree attached to u (excluding other cycle nodes) given x_u = v.
    # The cycle constraint is handled separately.
    
    # Let's define DP[u][v] for all u as:
    # If u is a leaf in the tree (no children in rev_adj that are tree nodes), DP[u][v] = 1.
    # If u has children c_1, ..., c_k in rev_adj (which are tree nodes or other nodes in the tree part),
    # DP[u][v] = product_{j=1}^k (sum_{k=1}^v DP[c_j][k]).
    
    # We need to process nodes in bottom-up order (leaves to roots).
    # We can use the topological order from the Kahn's algorithm peeling.
    # The nodes were peeled in order from leaves to the cycle.
    # So we can reverse the order of peeling to get bottom-up order for DP.
    
    # Re-run Kahn's to get the order
    in_degree = [0] * N
    for i in range(N):
        in_degree[adj[i]] += 1
        
    queue = [i for i in range(N) if in_degree[i] == 0]
    topo_order = []
    while queue:
        u = queue.pop(0)
        topo_order.append(u)
        v = adj[u]
        in_degree[v] -= 1
        if in_degree[v] == 0:
            queue.append(v)
            
    # Now, topo_order contains tree nodes in topological order (leaves first).
    # Cycle nodes are not in topo_order.
    
    # Initialize DP table
    # dp[u][v] for v in 1..M. We'll use 0-indexed for v, so v=0 corresponds to value 1.
    # dp[u] is a list of size M.
    dp = [[1] * M for _ in range(N)]
    
    # Process tree nodes in topological order
    for u in topo_order:
        # For each child c in rev_adj[u], we need to compute prefix sums of dp[c]
        # Then dp[u][v] = product of prefix_sum[c][v] for all children c
        
        # First, compute prefix sums for each child
        # But we can do it on the fly or precompute.
        # Let's precompute prefix sums for all children of u
        
        children = rev_adj[u]
        # Filter out cycle nodes? No, rev_adj[u] only contains tree nodes if u is a tree node.
        # Because if u is a tree node, its parent adj[u] is closer to the cycle.
        # The children in rev_adj[u] are nodes v such that adj[v] = u.
        # Since u is a tree node, v must also be a tree node (because if v were a cycle node, adj[v] would be in the cycle, not u).
        # So all children in rev_adj[u] are tree nodes.
        
        prod = 1
        for c in children:
            # Compute prefix sum of dp[c]
            # prefix_sum[v] = sum_{k=0}^v dp[c][k]
            # We can compute this iteratively
            current_prefix_sum = 0
            for v_idx in range(M):
                current_prefix_sum = (current_prefix_sum + dp[c][v_idx]) % MOD
                # Multiply this into the product for dp[u][v_idx]
                # But we need to store the product for each v_idx.
                # So we can't do it in one pass easily without storing intermediate results.
                pass
        
        # Better: compute prefix sums for each child first
        child_prefix_sums = []
        for c in children:
            p_sum = [0] * M
            current = 0
            for v_idx in range(M):
                current = (current + dp[c][v_idx]) % MOD
                p_sum[v_idx] = current
            child_prefix_sums.append(p_sum)
            
        # Now compute dp[u]
        for v_idx in range(M):
            val = 1
            for p_sum in child_prefix_sums:
                val = (val * p_sum[v_idx]) % MOD
            dp[u][v_idx] = val

    # Step 3: For each cycle, compute the number of ways
    # Identify cycles
    visited_cycle = [False] * N
    total_ans = 1
    
    for i in range(N):
        if in_cycle[i] and not visited_cycle[i]:
            # Found a new cycle
            cycle_nodes = []
            curr = i
            while not visited_cycle[curr]:
                visited_cycle[curr] = True
                cycle_nodes.append(curr)
                curr = adj[curr]
            
            # Now, for this cycle, all nodes must have the same value v.
            # The number of ways for a fixed v is product_{c in cycle_nodes} dp[c][v-1]
            # Because dp[c][v-1] is the number of ways to assign the tree attached to c given x_c = v.
            # Note: dp[c][v-1] already includes the ways for the tree nodes attached to c.
            # The cycle nodes themselves are not included in the dp computation for the tree part.
            # So the total ways for the component is sum_{v=1}^M (product_{c in cycle_nodes} dp[c][v-1])
            
            ways_for_component = 0
            for v_idx in range(M):
                # v_idx corresponds to value v = v_idx + 1
                prod = 1
                for c in cycle_nodes:
                    prod = (prod * dp[c][v_idx]) % MOD
                ways_for_component = (ways_for_component + prod) % MOD
                
            total_ans = (total_ans * ways_for_component) % MOD

    print(total_ans)

solve()