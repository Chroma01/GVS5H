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

    # Adjust A to be 0-indexed
    A = [x - 1 for x in A]

    MOD = 998244353

    # Step 1: Identify components and cycles
    # Each node has exactly one outgoing edge.
    # We need to find which nodes are in cycles and which are in trees leading to cycles.
    
    # Compute in-degrees to help with topological sort (Kahn's algorithm) to peel off trees
    in_degree = [0] * N
    for i in range(N):
        in_degree[A[i]] += 1

    # Queue for nodes with in-degree 0 (leaves of the trees in the reversed graph, or sources in the functional graph)
    queue = [i for i in range(N) if in_degree[i] == 0]
    
    # Nodes that are part of cycles will have in-degree >= 1 after peeling
    is_in_cycle = [False] * N
    
    # Process the queue to peel off tree nodes
    head = 0
    while head < len(queue):
        u = queue[head]
        head += 1
        v = A[u]
        in_degree[v] -= 1
        if in_degree[v] == 0:
            queue.append(v)
            
    # Nodes not processed in the queue are part of cycles
    for i in range(N):
        if in_degree[i] > 0:
            is_in_cycle[i] = True

    # Identify components and their cycle nodes
    # We can use a visited array to group nodes into components
    visited = [False] * N
    components = [] # List of lists, each list contains nodes in the component
    
    # First, identify cycle nodes and group them into components
    # Since each component has exactly one cycle, we can find cycles first.
    
    cycle_nodes = [i for i in range(N) if is_in_cycle[i]]
    
    # Group cycle nodes into components
    # We can traverse the cycle to find all nodes in the component
    # But it's easier to just assign component IDs to all nodes.
    
    comp_id = [-1] * N
    comp_count = 0
    
    # Process each unvisited cycle node to find its component
    for start_node in cycle_nodes:
        if comp_id[start_node] != -1:
            continue
        
        # Find the cycle
        cycle = []
        curr = start_node
        while True:
            if comp_id[curr] != -1:
                # This should not happen if we iterate correctly and only start from unvisited
                break
            cycle.append(curr)
            curr = A[curr]
            if curr == start_node:
                break
        
        # Assign component ID to cycle nodes
        for node in cycle:
            comp_id[node] = comp_count
            visited[node] = True # Mark as visited for component assignment
            
        # Now find all tree nodes that flow into this cycle
        # We can do a BFS/DFS from the cycle nodes in the reversed graph
        # Reversed graph: edge u -> v if A[u] == v becomes v -> u
        # But we already have the structure. We can just traverse backwards from cycle nodes.
        
        # Let's build the reverse adjacency list for tree nodes
        # Actually, we can just use the fact that we peeled the trees.
        # The nodes that were peeled are in trees. We need to assign them to components.
        # A node u is in the component of the cycle it eventually reaches.
        # We can determine this by following A until we hit a cycle node.
        
        # However, we can do this more efficiently:
        # For each node not in a cycle, follow A until we hit a cycle node.
        # But this is O(N^2) in worst case (long chains).
        # Instead, we can process nodes in reverse topological order (from the peeled queue).
        
        # The queue contains nodes in topological order (leaves to roots of trees).
        # We can assign component IDs to tree nodes by propagating from the cycle.
        # But the queue goes from leaves to cycle. So we can process the queue in reverse.
        
        # Let's store the tree nodes in a list
        tree_nodes = [i for i in range(N) if not is_in_cycle[i]]
        
        # Process tree nodes in reverse topological order (deepest first)
        # The queue was built from leaves to cycle. So reverse queue gives cycle to leaves?
        # No, queue[0] are leaves. queue[-1] are nodes adjacent to cycle.
        # So iterating queue in reverse order processes nodes closer to cycle first.
        
        # Wait, the queue contains ALL tree nodes.
        # For a node u in the queue, A[u] is its parent in the functional graph (closer to cycle).
        # So if we process u, we can assign comp_id[u] = comp_id[A[u]].
        # Since A[u] is closer to the cycle, it should have been processed or is in the cycle.
        # In the topological sort, A[u] appears after u in the queue?
        # No, in_degree[A[u]] is decremented when u is processed.
        # So A[u] is added to the queue only after all its children are processed.
        # So A[u] appears later in the queue than u.
        # Therefore, iterating the queue in reverse order ensures that when we process u, A[u] has already been assigned a component ID.
        
        # Let's verify:
        # Leaves have in_degree 0. They are added first.
        # Their parents have in_degree reduced. When a parent's in_degree becomes 0, it is added.
        # So parents are added after children.
        # Reverse order: parents processed before children.
        # So when we process a child u, its parent A[u] has already been assigned a component ID.
        
        for i in range(len(queue) - 1, -1, -1):
            u = queue[i]
            p = A[u]
            comp_id[u] = comp_id[p]
            
        comp_count += 1

    # Now comp_id[i] gives the component ID for each node i.
    # Group nodes by component
    comp_nodes = [[] for _ in range(comp_count)]
    for i in range(N):
        comp_nodes[comp_id[i]].append(i)
        
    # For each component, identify the cycle nodes and the tree structure
    # We need to compute dp[u][v] for each node u and v in [1, M]
    # dp[u][v] = number of valid assignments for the subtree rooted at u (in reversed graph) given x[u] = v
    
    # The reversed graph has edges A[i] -> i.
    # So for a node u, its children in the reversed graph are all i such that A[i] == u.
    
    # Build reverse adjacency list
    rev_adj = [[] for _ in range(N)]
    for i in range(N):
        rev_adj[A[i]].append(i)
        
    # We need to process nodes in an order such that children are processed before parents.
    # This is a post-order traversal of the reversed tree.
    # Since the reversed graph is a forest rooted at cycle nodes, we can do a DFS/BFS.
    # Or we can use the topological order we already have?
    # The queue contains tree nodes in topological order (leaves to cycle).
    # So reverse queue is cycle to leaves.
    # But we need leaves to cycle for DP.
    # So we can process the queue in forward order for tree nodes?
    # No, for DP, we need children processed before parents.
    # In the reversed graph, children of u are nodes i with A[i] == u.
    # These nodes i are "below" u in the tree.
    # In the functional graph, i -> A[i] = u.
    # So i is a child of u in the reversed graph.
    # In the topological sort of the functional graph (peeling), leaves (in-degree 0) are processed first.
    # These leaves are the deepest nodes in the reversed trees.
    # So processing the queue in forward order processes deepest nodes first.
    # This is exactly what we need for DP: process children before parents.
    
    # However, the queue only contains tree nodes. Cycle nodes are not in the queue.
    # We need to process cycle nodes last.
    # So we can process the queue (tree nodes) in forward order, then process cycle nodes.
    # But cycle nodes depend on their children (which are tree nodes or other cycle nodes).
    # For a cycle node u, its children in the reversed graph are tree nodes (which are in the queue) and possibly other cycle nodes?
    # No, in a functional graph, a cycle node's only outgoing edge is to the next cycle node.
    # So in the reversed graph, a cycle node's incoming edge is from the previous cycle node.
    # Its children in the reversed graph are the tree nodes that flow into it.
    # So for a cycle node u, all its children in the reversed graph are tree nodes.
    # These tree nodes are processed before u if we process the queue first.
    
    # So the order is:
    # 1. Process all tree nodes in the order of the queue (forward).
    # 2. Process all cycle nodes. For cycle nodes, we need to handle the cycle dependency.
    #    But wait, for a cycle node u, dp[u][v] depends on its children (tree nodes) which are already computed.
    #    So we can compute dp[u][v] for cycle nodes independently of other cycle nodes?
    #    Yes, because the cycle constraint is handled separately: all cycle nodes in a component must have the same value.
    #    The DP value dp[u][v] for a cycle node u includes the contributions of the tree attached to u.
    #    It does NOT include the contributions of other cycle nodes.
    #    So we can compute dp[u][v] for all u (tree and cycle) using the same logic.
    
    # Initialize dp table
    # dp[u][v] for v in 1..M. We'll use 0-indexed v: dp[u][v] corresponds to x[u] = v+1.
    # Size: N x (M+1)
    dp = [[0] * (M + 1) for _ in range(N)]
    
    # Prefix sums for children
    # For a node u, dp[u][v] = product over children c of (sum_{k=1}^v dp[c][k])
    # Let S[c][v] = sum_{k=1}^v dp[c][k]
    # Then dp[u][v] = product_{c} S[c][v]
    
    # We can compute S[c][v] on the fly or precompute.
    # Since we process in order, when we process u, all its children c have been processed.
    
    # Process tree nodes in queue order
    for u in queue:
        # Compute dp[u][v] for v in 1..M
        # dp[u][v] = product_{c in rev_adj[u]} S[c][v]
        # S[c][v] = sum_{k=1}^v dp[c][k]
        
        # First, compute S[c][v] for all children c
        # But we can just accumulate the product
        
        # Initialize dp[u][0] = 0 (not used, but for indexing)
        # dp[u][v] for v from 1 to M
        
        # Start with product = 1
        # For each child c, multiply by S[c][v]
        
        # To do this efficiently, we can maintain a running product
        # But we need to do it for each v.
        
        # Let's compute S[c][v] for each child c first
        # Then compute dp[u][v]
        
        # Initialize dp[u] with 1s? No, product starts at 1.
        # dp[u][v] = 1 initially, then multiply by S[c][v] for each child.
        
        # But if u has no children, dp[u][v] = 1 for all v.
        
        # Let's compute S[c][v] for all children c
        # We can store S[c] as a list
        
        child_S = []
        for c in rev_adj[u]:
            # Compute prefix sum for c
            S_c = [0] * (M + 1)
            current_sum = 0
            for v in range(1, M + 1):
                current_sum = (current_sum + dp[c][v]) % MOD
                S_c[v] = current_sum
            child_S.append(S_c)
            
        # Now compute dp[u][v]
        # dp[u][v] = product_{c} S_c[v]
        prod = 1
        for v in range(1, M + 1):
            for S_c in child_S:
                prod = (prod * S_c[v]) % MOD
            dp[u][v] = prod

    # Process cycle nodes
    # Cycle nodes are not in the queue.
    # We need to process them in an order such that their children (tree nodes) are done.
    # Tree nodes are already done.
    # So we can process cycle nodes in any order.
    
    # But we need to group them by component to compute the final answer.
    # For each component, the cycle nodes are known.
    # For each cycle node u, compute dp[u][v] using the same logic.
    
    # Get all cycle nodes
    cycle_nodes_list = [i for i in range(N) if is_in_cycle[i]]
    
    # Process each cycle node
    for u in cycle_nodes_list:
        child_S = []
        for c in rev_adj[u]:
            # c can be a tree node or another cycle node?
            # In a functional graph, a cycle node's only outgoing edge is to the next cycle node.
            # So in the reversed graph, a cycle node's incoming edge is from the previous cycle node.
            # Its children in the reversed graph are the tree nodes that flow into it.
            # So c is always a tree node for a cycle node u?
            # Yes, because if c were a cycle node, then A[c] = u, and A[u] = next_cycle_node.
            # But c is a child of u in the reversed graph, so A[c] = u.
            # If c is in a cycle, then A[c] is also in the cycle.
            # But u is in a cycle. So c is in the same cycle as u.
            # But then c is a cycle node.
            # However, in the reversed graph, the cycle is a simple cycle.
            # So u has exactly one child in the reversed graph that is a cycle node: the previous node in the cycle.
            # But wait, the condition for the cycle is that all cycle nodes have the same value.
            # The DP value dp[u][v] for a cycle node u should include the contribution of the tree attached to u.
            # It should NOT include the contribution of the other cycle nodes.
            # So when computing dp[u][v], we should only consider tree children, not cycle children.
            
            # How to distinguish?
            # If c is a cycle node, we skip it for the DP computation of u.
            # Because the cycle constraint is handled separately.
            
            if is_in_cycle[c]:
                continue
            # c is a tree node, already processed
            S_c = [0] * (M + 1)
            current_sum = 0
            for v in range(1, M + 1):
                current_sum = (current_sum + dp[c][v]) % MOD
                S_c[v] = current_sum
            child_S.append(S_c)
            
        prod = 1
        for v in range(1, M + 1):
            for S_c in child_S:
                prod = (prod * S_c[v]) % MOD
            dp[u][v] = prod

    # Now, for each component, compute G_c(v) = product_{u in cycle of c} dp[u][v]
    # Then the answer is sum_{v=1}^M product_{c} G_c(v)
    
    # Group cycle nodes by component
    comp_cycle_nodes = [[] for _ in range(comp_count)]
    for u in cycle_nodes_list:
        cid = comp_id[u]
        comp_cycle_nodes[cid].append(u)
        
    # For each component, compute G_c(v) for v in 1..M
    # G_c[v] = product_{u in comp_cycle_nodes[c]} dp[u][v]
    
    comp_G = [] # List of lists, comp_G[c][v] = G_c(v)
    
    for cid in range(comp_count):
        cycle_nodes = comp_cycle_nodes[cid]
        # Initialize G_c[v] = 1 for all v
        G_c = [1] * (M + 1)
        for u in cycle_nodes:
            for v in range(1, M + 1):
                G_c[v] = (G_c[v] * dp[u][v]) % MOD
        comp_G.append(G_c)
        
    # Now compute the total answer
    # ans = sum_{v=1}^M product_{c} G_c[v]
    
    # We can do this by iterating v and multiplying across components
    ans = 0
    for v in range(1, M + 1):
        prod = 1
        for G_c in comp_G:
            prod = (prod * G_c[v]) % MOD
        ans = (ans + prod) % MOD
        
    print(ans)

solve()