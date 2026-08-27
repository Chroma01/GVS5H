import sys

# Increase recursion depth just in case, though iterative approach is preferred for large N
sys.setrecursionlimit(3000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        A = [0] * (N + 1)
        for i in range(1, N + 1):
            A[i] = int(next(iterator))
    except StopIteration:
        return

    MOD = 998244353

    # Build the reversed graph: A[i] -> i means i is a child of A[i] in the reversed graph
    # Original: i -> A[i] with constraint x[i] <= x[A[i]]
    # Reversed: A[i] -> i with constraint x[i] <= x[A[i]] (parent >= child)
    adj = [[] for _ in range(N + 1)]
    in_degree = [0] * (N + 1)
    
    for i in range(1, N + 1):
        parent = A[i]
        adj[parent].append(i)
        in_degree[i] += 1

    # Identify components and cycles
    # We can use a visited array and follow the functional graph to find cycles
    visited = [False] * (N + 1)
    on_stack = [False] * (N + 1) # Not strictly needed if we just trace paths
    
    # We need to process each component. A component is defined by the set of nodes reachable from the cycle.
    # Since each node has out-degree 1 in original graph, components are disjoint.
    # We can find the cycle for each unvisited node by following A[i].
    
    # To efficiently compute DP, we need to process trees in post-order (bottom-up).
    # The "trees" are rooted at the cycle nodes in the reversed graph.
    # We can identify the cycle nodes first.
    
    # Step 1: Find cycles and mark cycle nodes
    # We can use a standard cycle detection on the functional graph.
    # Since N is small, we can just trace each node.
    
    cycle_nodes = set()
    visited_global = [False] * (N + 1)
    
    for i in range(1, N + 1):
        if visited_global[i]:
            continue
        
        # Trace path from i
        path = []
        curr = i
        while not visited_global[curr]:
            visited_global[curr] = True # Mark as visited in this traversal to detect loops? 
            # Wait, we need to distinguish between "visited in current traversal" and "visited globally".
            # Actually, since it's a functional graph, components are disjoint.
            # We can just find the cycle for the component containing i.
            path.append(curr)
            curr = A[curr]
        
        # curr is now a node that has been visited.
        # If curr is in the current path, we found a cycle.
        # If curr was visited in a previous component traversal, then the current path leads to an already processed component.
        # But since components are disjoint, if curr was visited globally, it must be part of a previously processed component.
        # However, we are iterating 1..N. If we encounter a visited node, it means we hit a node from a previous component.
        # But wait, the graph is a set of components. If we start at an unvisited node, we will eventually hit a node that is either:
        # 1. In the current path (cycle found)
        # 2. Visited in a previous traversal (impossible if we process components correctly? No, components are disjoint sets of nodes).
        # Actually, if we process each node, we will eventually cover all nodes.
        # If we hit a visited node from a previous component, it means the current node is part of that component?
        # No, because each node has out-degree 1. If we start at an unvisited node, we trace a path.
        # The path must end in a cycle. If the cycle was already processed, then all nodes in the path leading to it should have been processed?
        # Not necessarily. We might process a node in the tree part first.
        # So we need to be careful.
        
        # Better approach:
        # 1. Compute in-degrees in the original graph.
        # 2. Topological sort to remove tree nodes (nodes with in-degree 0 in original graph? No, in-degree in original graph is number of children).
        #    Wait, original graph: i -> A[i]. In-degree of u is number of i such that A[i] = u.
        #    Nodes with in-degree 0 are leaves in the original graph (no one points to them).
        #    We can peel off nodes with in-degree 0. The remaining nodes form the cycles.
        #    This is a standard way to find cycles in a functional graph.
        
        pass

    # Let's restart the cycle finding with in-degree peeling
    in_deg = [0] * (N + 1)
    for i in range(1, N + 1):
        in_deg[A[i]] += 1

    q = []
    for i in range(1, N + 1):
        if in_deg[i] == 0:
            q.append(i)

    # Peel off tree nodes
    # We need to keep track of which nodes are part of a cycle
    is_cycle = [False] * (N + 1)
    
    # We also need to know the component structure.
    # Actually, we can just identify the cycle nodes.
    # The nodes that remain after peeling are the cycle nodes.
    # But we need to know which tree nodes belong to which cycle node to build the DP.
    
    # Let's do the peeling to identify cycle nodes first.
    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        # u is a tree node (not in cycle)
        # Remove u: decrement in-degree of A[u]
        v = A[u]
        in_deg[v] -= 1
        if in_deg[v] == 0:
            q.append(v)
            
    # Now nodes with in_deg > 0 are cycle nodes.
    # Actually, in a functional graph, the remaining nodes form disjoint cycles.
    # So in_deg will be 1 for cycle nodes (since each node in a cycle has exactly one incoming edge from the cycle).
    # Wait, if a cycle node has a tree attached, it has incoming edges from the tree.
    # But we peeled all tree nodes. So now only cycle edges remain.
    # So yes, in_deg[v] == 1 for cycle nodes.
    
    cycle_nodes_list = [i for i in range(1, N + 1) if in_deg[i] > 0]
    
    # Now we need to build the DP.
    # We need to process nodes in reverse topological order (leaves to roots).
    # The "roots" of our trees are the cycle nodes.
    # The "leaves" are the nodes that were peeled first (or rather, the ones with no incoming edges in the original graph).
    # We can use the order of peeling (reverse of q) to process.
    # q contains nodes in topological order (leaves first).
    # So we can iterate q in reverse order.
    
    # However, we need to handle the cycle nodes carefully.
    # The cycle nodes are the roots. They have no children in the reversed graph that are NOT in the cycle?
    # No, in the reversed graph (A[i] -> i), the cycle nodes are roots of trees.
    # The edges in the reversed graph are: for each i, edge A[i] -> i.
    # The cycle nodes have edges from other cycle nodes (forming the cycle) and from tree nodes.
    # Wait, in the reversed graph, the cycle is still a cycle.
    # But we want to treat the cycle as a single root for the purpose of the DP?
    # No, the problem states x[c1] = x[c2] = ... = x[ck] = v.
    # So we can compute DP for the trees attached to each cycle node, but we must stop at the cycle.
    # Actually, the standard DP on trees works if we consider the cycle as the root.
    # But the cycle nodes are connected to each other.
    # However, since all cycle nodes must have the same value, we can compute the DP for the "tree" attached to each cycle node,
    # where the "tree" includes the cycle node itself?
    # No, if we include the cycle node, the DP for cycle node c would depend on its parent in the cycle (which is also a cycle node).
    # But since all cycle nodes have the same value, we can just compute the DP for the tree rooted at c (in reversed graph)
    # EXCLUDING the incoming edge from the previous cycle node.
    # But the reversed graph has edges A[i] -> i.
    # For a cycle node c, its children in reversed graph are:
    # 1. Nodes i such that A[i] = c (these are the tree nodes attached to c).
    # 2. The node p such that A[p] = c? No, in reversed graph, edges are A[i] -> i.
    #    So if c is in a cycle c1 -> c2 -> ... -> ck -> c1 (original),
    #    then in reversed graph: c2 -> c1, c3 -> c2, ..., c1 -> ck.
    #    So c1 has a child c2? No, c2 -> c1 means c2 is parent of c1?
    #    Original: c1 -> c2. Reversed: c2 -> c1.
    #    So in reversed graph, the cycle is c2 -> c1 -> ck -> ... -> c2.
    #    So each cycle node has exactly one child in the cycle (the next node in the original cycle).
    #    And it has children from the trees attached to it.
    #    So the reversed graph is a set of cycles with trees rooted on them?
    #    No, the reversed graph is a functional graph where each node has out-degree 1?
    #    Original: out-degree 1. Reversed: in-degree 1? No.
    #    Original: i -> A[i]. Reversed: A[i] -> i.
    #    In reversed graph, each node i has exactly one incoming edge from A[i].
    #    So reversed graph is a collection of components where each component has exactly one cycle,
    #    and edges point AWAY from the cycle?
    #    Original: edges point towards cycle.
    #    Reversed: edges point away from cycle.
    #    So in reversed graph, the cycle nodes are roots of trees (and the cycle itself).
    #    Wait, if edges point away from the cycle, then the cycle nodes have no incoming edges from the cycle?
    #    Original cycle: c1 -> c2 -> ... -> ck -> c1.
    #    Reversed: c2 -> c1, c3 -> c2, ..., c1 -> ck.
    #    So in reversed graph, c1 has incoming from c2, c2 from c3, etc.
    #    So the cycle is still a cycle.
    #    And the tree nodes (which were pointing to the cycle in original) now point AWAY from the cycle.
    #    So in reversed graph, the structure is: a cycle, and trees rooted on the cycle nodes, with edges directed away from the cycle.
    #    This is exactly what we need for DP!
    #    We want to count assignments where x[child] <= x[parent].
    #    In reversed graph: parent is A[i], child is i.
    #    Constraint: x[i] <= x[A[i]].
    #    So if we process in reversed graph, we have a tree rooted at the cycle (edges away from cycle).
    #    We need to assign values such that x[child] <= x[parent].
    #    This means values are non-decreasing as we go away from the cycle.
    #    So if we fix the cycle value to v, then for any node u, x[u] <= v?
    #    No. If x[child] <= x[parent], and root is v, then children can be <= v, grandchildren <= children, etc.
    #    So x[u] <= v for all u.
    #    This matches our previous logic.
    
    # So the plan:
    # 1. Identify cycle nodes.
    # 2. Build the reversed graph (adj[A[i]].append(i)).
    # 3. For each cycle node, we need to compute the number of ways for the tree rooted at it (in reversed graph).
    #    But the cycle nodes are connected.
    #    However, since all cycle nodes must have the same value v, we can treat the cycle as a single entity.
    #    But the trees attached to different cycle nodes are independent given the cycle value.
    #    So for each cycle node c, we compute dp[c][v] = number of ways for the tree rooted at c (excluding the cycle edge) given x[c] = v.
    #    Wait, the tree rooted at c in reversed graph includes all nodes that can reach c?
    #    No, in reversed graph, edges are A[i] -> i.
    #    So if we start at c, we can reach all nodes i such that A[i] = c, and their children, etc.
    #    These are exactly the nodes that point to c in the original graph (directly or indirectly).
    #    So yes, these are the tree nodes attached to c.
    #    The cycle edge in reversed graph is from the next cycle node to c.
    #    So we should NOT include the cycle edge in the DP for c.
    #    We can simply remove the cycle edges from the reversed graph before DP, or handle them specially.
    #    Since we know the cycle nodes, we can just ignore the edge from the "next" cycle node.
    
    # Algorithm refined:
    # 1. Find cycle nodes.
    # 2. Build reversed graph adj.
    # 3. For each cycle node c, identify its children in the reversed graph.
    #    The children are all i such that A[i] = c.
    #    Note: One of these children might be the previous cycle node in the cycle?
    #    Original: ... -> p -> c -> q -> ...
    #    Reversed: ... -> c -> p (no, A[p]=c so c->p), c -> q (no, A[q]=c? No, A[c]=q so q->c).
    #    So in reversed graph, c has children: all i such that A[i] = c.
    #    The node p (where A[p]=c) is a child of c in reversed graph.
    #    The node q (where A[c]=q) is a parent of c in reversed graph (edge q->c).
    #    So the cycle edges in reversed graph are q->c, r->q, etc.
    #    So c has a child q? No, A[c]=q means edge q->c. So q is parent of c.
    #    So c has children: all i such that A[i] = c.
    #    Does any cycle node point to c? Yes, the previous node in the cycle.
    #    Let p be such that A[p] = c. Then p is a child of c in reversed graph.
    #    So the cycle edge is c -> p in reversed graph.
    #    So we must exclude p from the children of c when computing DP for c.
    #    How to find p? p is the node such that A[p] = c.
    #    Since it's a cycle, there is exactly one such p in the cycle.
    #    So for each cycle node c, we find its predecessor in the cycle (p) and exclude it from the children list.
    
    # 4. Compute DP.
    #    We need to process nodes in reverse topological order of the reversed graph (leaves to roots).
    #    The leaves of the reversed graph are the nodes with no children (in reversed graph).
    #    These are the nodes i such that no j has A[j] = i.
    #    We can use the in-degree in the reversed graph (which is the out-degree in original graph? No).
    #    In reversed graph, in-degree of u is number of i such that A[i] = u.
    #    Wait, we want to process from leaves (no children) to roots (cycle).
    #    Children in reversed graph: adj[u].
    #    We want to process u after all its children are processed.
    #    So we need the topological order of the reversed graph.
    #    We can compute in-degrees in the reversed graph (number of children).
    #    Wait, topological sort requires in-degree (number of incoming edges).
    #    In reversed graph, edges are u -> v. We want to process v before u.
    #    So we need to process nodes with out-degree 0 first?
    #    Yes, leaves in reversed graph have out-degree 0.
    #    So we can compute out-degrees in reversed graph (size of adj[u]).
    #    Queue nodes with out-degree 0.
    #    Process them, then decrement out-degree of parents.
    #    This will give us an order from leaves to cycle.
    
    # 5. DP state: dp[u][v] = number of ways for subtree rooted at u (in reversed graph) given x[u] = v.
    #    dp[u][v] = product over children c of (sum_{k=1}^v dp[c][k]).
    #    Base case: leaves have dp[leaf][v] = 1 for all v.
    #    We can optimize the sum: let S[c][v] = sum_{k=1}^v dp[c][k].
    #    Then dp[u][v] = product S[c][v].
    #    We can compute S[c] incrementally.
    
    # 6. For cycle nodes, we compute dp[c][v] using the children excluding the cycle predecessor.
    #    Then the total ways for the component given cycle value v is product of dp[c][v] for all c in cycle.
    #    Sum this product over v=1..M.

    # Implementation details:
    # - Find cycle nodes.
    # - Build reversed graph.
    # - Compute out-degrees in reversed graph.
    # - Topological sort (leaves first).
    # - DP.
    # - Aggregate.

    # Step 1: Find cycle nodes
    # We already did this with in_deg peeling.
    # cycle_nodes_list contains all cycle nodes.
    
    # Step 2: Build reversed graph and compute out-degrees
    adj = [[] for _ in range(N + 1)]
    out_deg_rev = [0] * (N + 1)
    
    # We need to map each node to its predecessor in the cycle to exclude it.
    # Let's store the predecessor for each cycle node.
    pred_in_cycle = {}
    
    # We can find the predecessor by tracing the cycle.
    # Since we have cycle_nodes_list, we can just trace.
    # But we need to know which node points to which.
    # We can use the original A array.
    # For each cycle node c, find p such that A[p] == c and p is in cycle_nodes_list.
    # Since it's a cycle, there is exactly one such p.
    
    # Let's build the cycle structure first.
    # We can just iterate through cycle_nodes_list and find the predecessor.
    # But we need to be careful not to include non-cycle nodes.
    # Actually, we can just find the predecessor for all nodes, but only care about cycle nodes.
    
    # Let's build a map: next_node[u] = A[u].
    # For cycle nodes, we can find the predecessor.
    
    # To avoid O(N^2), we can precompute predecessors for all nodes?
    # No, just for cycle nodes.
    # We can iterate 1..N, if A[i] is in cycle_nodes_list, then i is a candidate predecessor.
    # But there might be multiple i (tree nodes). We need the one that is also in cycle_nodes_list.
    
    # Let's create a set of cycle nodes for O(1) lookup.
    cycle_set = set(cycle_nodes_list)
    
    # Find predecessor for each cycle node
    cycle_pred = {}
    for c in cycle_nodes_list:
        # Find p in cycle_set such that A[p] == c
        # Since N is small, we can just iterate.
        for p in cycle_nodes_list:
            if A[p] == c:
                cycle_pred[c] = p
                break
    
    # Build reversed graph and out-degrees
    # We only care about edges that are NOT cycle edges.
    # Cycle edges in reversed graph: c -> pred[c].
    # So we add edge u -> v to adj if v is a child of u in reversed graph AND (u, v) is not a cycle edge.
    # Wait, the DP is on the tree rooted at c. The tree includes all nodes reachable from c in reversed graph EXCEPT the cycle edge.
    # So we should build the full reversed graph, but when computing DP for c, we skip the child pred[c].
    # For non-cycle nodes, they are not roots, so we process them normally.
    # But wait, non-cycle nodes are part of the trees.
    # The topological sort will process them.
    # So we can build the full reversed graph.
    
    for i in range(1, N + 1):
        parent = A[i]
        adj[parent].append(i)
        out_deg_rev[parent] += 1
        
    # Topological sort (leaves first)
    # Leaves in reversed graph are nodes with out_deg_rev == 0.
    # But wait, cycle nodes have out_deg_rev >= 1 (at least the cycle edge).
    # Tree nodes might have out_deg_rev > 0.
    # We want to process from leaves (out_deg_rev == 0) up to cycle.
    
    q = []
    for i in range(1, N + 1):
        if out_deg_rev[i] == 0:
            q.append(i)
            
    topo_order = []
    head = 0
    while head < len(q):
        u = q[head]
        head += 1
        topo_order.append(u)
        
        # u is processed. It is a child of A[u] in reversed graph.
        # So we decrement out_deg_rev[A[u]].
        p = A[u]
        out_deg_rev[p] -= 1
        if out_deg_rev[p] == 0:
            q.append(p)
            
    # Now process in reverse topological order (from cycle to leaves? No, from leaves to cycle).
    # topo_order is leaves -> ... -> cycle.
    # We need to process children before parents.
    # So we iterate topo_order in reverse?
    # No, topo_order has leaves first.
    # If we process u, we need dp values of its children.
    # Children of u are in adj[u].
    # Are children of u processed before u?
    # In topo_order, children appear before parents?
    # Yes, because we start with leaves (no children) and move up.
    # So if we iterate topo_order in reverse, we get parents before children?
    # No, topo_order: [leaves, ..., roots].
    # Reverse: [roots, ..., leaves].
    # We need children before parents.
    # So we should iterate topo_order as is?
    # Let's check: u is in topo_order. Its children v are in adj[u].
    # When did v get added to q?
    # v was added when its out-degree became 0.
    # u's out-degree becomes 0 only after all its children are processed (removed from q).
    # So v appears before u in topo_order.
    # So we can iterate topo_order in reverse? No, we need v before u.
    # So we iterate topo_order in reverse order?
    # If v is before u, then iterating in reverse gives u before v. That's wrong.
    # We need to process v before u.
    # So we iterate topo_order in the order it was generated?
    # No, topo_order is [leaves, ..., roots].
    # If we process leaves first, we compute dp[leaf].
    # Then we move to next node.
    # But the next node might be a child of the current node?
    # No, the next node in topo_order is another leaf or a node whose children are all processed.
    # So if we iterate topo_order in reverse, we get roots first. That's wrong.
    # We need to iterate topo_order in the order of generation?
    # Wait, if we process u, we need dp[v] for all v in adj[u].
    # Are v in adj[u] already processed?
    # v is a child of u. v appears before u in topo_order.
    # So if we iterate topo_order in reverse, we see u before v.
    # So we need to iterate topo_order in the order of generation?
    # No, if we iterate in generation order, we see v before u.
    # So we can compute dp[v] when we see v.
    # Then when we see u, dp[v] is ready.
    # So we iterate topo_order in the order it was generated?
    # Wait, topo_order is [leaves, ..., roots].
    # If we process leaves first, we compute dp[leaf].
    # Then we process the next node.
    # But the next node might be a child of the first node?
    # No, the first node is a leaf. It has no children.
    # The next node might be a child of some other node.
    # So yes, we can iterate topo_order in the order it was generated.
    # But wait, we need to update the parent's DP after processing the child.
    # So we can just iterate topo_order in reverse?
    # No, if we iterate in reverse, we get roots first.
    # We need to process children first.
    # So we iterate topo_order in the order it was generated?
    # Let's trace:
    # q = [l1, l2, ..., r1, r2] (leaves to roots).
    # If we process l1, we compute dp[l1].
    # Then we process l2.
    # ...
    # Then we process r1. r1 has children. Are they processed?
    # Yes, because children appear before r1 in q.
    # So we can iterate q in the order it was generated.
    # But wait, we need to accumulate the product for the parent.
    # So when we process u, we compute dp[u].
    # Then we update A[u]'s DP?
    # No, dp[u] depends on children.
    # So we compute dp[u] using children's dp.
    # Then we can use dp[u] to help compute dp[A[u]].
    # So we need to store dp[u] and then when we process A[u], we use it.
    # So we iterate q in the order it was generated.
    # But wait, q contains all nodes.
    # Cycle nodes are at the end of q.
    # So we process leaves, then intermediate, then cycle.
    # This is correct.
    
    # DP table: dp[u][v] for v in 1..M.
    # To save space, we can use a list of lists.
    # But M is up to 2025, N up to 2025. 2025*2025 ints is ~4MB. Fine.
    
    dp = [[0] * (M + 1) for _ in range(N + 1)]
    
    # Precompute prefix sums for children?
    # We can compute dp[u][v] for all v.
    # dp[u][v] = product_{c in children} (sum_{k=1}^v dp[c][k])
    # We can compute this for each u.
    
    # Initialize dp for leaves?
    # Actually, the formula works for leaves too (empty product = 1).
    
    # We need to handle the cycle nodes specially: exclude the cycle predecessor.
    # But the topological order processes cycle nodes last.
    # So when we process a cycle node c, we can just skip the child pred[c].
    
    # Let's implement.
    
    # We need to know the children of each node in the reversed graph.
    # adj[u] contains all children.
    # For cycle nodes, we skip cycle_pred[c].
    
    # Also, we need to handle the case where a cycle node has no tree children (only cycle edge).
    # Then dp[c][v] = 1 (product over empty set).
    
    # One more thing: the cycle nodes are processed in the order they appear in q.
    # The order among cycle nodes doesn't matter.
    
    # Let's do it.
    
    # We need to store the sum of dp[c] for each child c to avoid recomputing.
    # But we can just compute it on the fly.
    
    # Optimization: 
    # dp[u][v] = product S[c][v].
    # S[c][v] = sum_{k=1}^v dp[c][k].
    # We can precompute S[c] for all c.
    
    # Since we process in topological order, when we are at u, all children c are processed.
    # So we can compute S[c] for all children.
    # Then compute dp[u].
    
    # Let's store S[u] as well.
    
    S = [[0] * (M + 1) for _ in range(N + 1)]
    
    # Process in topological order
    for u in topo_order:
        # Compute dp[u]
        # Identify children
        children = adj[u]
        # If u is a cycle node, exclude the cycle predecessor
        if u in cycle_set:
            children = [c for c in children if c != cycle_pred[u]]
        
        # Compute product of sums
        # dp[u][v] = product_{c in children} S[c][v]
        # We can compute this for all v.
        
        # Initialize product = 1
        # For each v, multiply by S[c][v]
        
        # To optimize, we can compute the product for each v.
        # Since M is small, O(M * deg) is fine.
        
        # But we can do it smarter:
        # For each child c, we have S[c].
        # We want P[v] = product S[c][v].
        # We can iterate v from 1 to M.
        
        # However, we can also compute S[u] from dp[u].
        # S[u][v] = S[u][v-1] + dp[u][v].
        
        # Let's compute dp[u] first.
        
        # We need to handle the case where children is empty.
        # Then dp[u][v] = 1 for all v.
        
        if not children:
            for v in range(1, M + 1):
                dp[u][v] = 1
        else:
            # Compute product for each v
            # We can do this by iterating v
            # But we can also do it by iterating children and updating an array.
            # Initialize res[v] = 1
            res = [1] * (M + 1)
            for c in children:
                # Multiply res[v] by S[c][v]
                # We can do this in a loop
                # But Python loops are slow.
                # We can use list comprehension or map?
                # Or just a simple loop.
                # Given N, M <= 2025, total operations ~ N*M.
                # 4*10^6 is fine.
                for v in range(1, M + 1):
                    res[v] = (res[v] * S[c][v]) % MOD
            
            for v in range(1, M + 1):
                dp[u][v] = res[v]
        
        # Compute S[u]
        curr = 0
        for v in range(1, M + 1):
            curr = (curr + dp[u][v]) % MOD
            S[u][v] = curr
            
    # Now aggregate results for each component
    # We need to group cycle nodes by component.
    # But wait, the cycle nodes are disjoint.
    # Each cycle node belongs to exactly one component.
    # And the component is defined by the cycle.
    # So we can just iterate over all cycle nodes, compute the product of dp[c][v] for all c in the same cycle.
    # But we need to know which cycle nodes belong to the same cycle.
    # We can use the cycle_pred map to link them.
    # Or we can just iterate 1..N, if u is in cycle_set, find its cycle component.
    # Since we have cycle_pred, we can traverse the cycle.
    
    # Let's mark visited cycle nodes to group them.
    visited_cycle = [False] * (N + 1)
    total_ans = 0
    
    for c in cycle_nodes_list:
        if visited_cycle[c]:
            continue
        
        # Find all nodes in this cycle
        cycle_nodes = []
        curr = c
        while not visited_cycle[curr]:
            visited_cycle[curr] = True
            cycle_nodes.append(curr)
            curr = cycle_pred[curr]
        
        # Compute product for this cycle
        # For each v, product = product_{c in cycle_nodes} dp[c][v]
        # Then sum over v.
        
        # We can compute the product for each v.
        # Since cycle_nodes is small (<= N), and M is 2025.
        # O(M * cycle_len).
        
        # Initialize product array
        prod = [1] * (M + 1)
        for node in cycle_nodes:
            for v in range(1, M + 1):
                prod[v] = (prod[v] * dp[node][v]) % MOD
        
        # Sum
        comp_sum = 0
        for v in range(1, M + 1):
            comp_sum = (comp_sum + prod[v]) % MOD
            
        total_ans = (total_ans + comp_sum) % MOD
        
    print(total_ans)

solve()