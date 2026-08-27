import sys

# Increase recursion depth just in case, though we will use iterative approaches where possible
sys.setrecursionlimit(5000)

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
    # We need to process trees rooted at cycle nodes.
    # The edges for the tree structure (from parent to child) are A[i] -> i.
    # So, children[u] = list of i such that A[i] == u.
    children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        children[A[i]].append(i)

    # Identify components and cycles
    # Each node has out-degree 1. We can find cycles by following pointers.
    visited = [False] * (N + 1)
    in_cycle = [False] * (N + 1)
    cycle_nodes = [] # List of lists, each inner list is a cycle
    component_id = [-1] * (N + 1)
    
    # First, find all cycles
    for i in range(1, N + 1):
        if not visited[i]:
            path = []
            curr = i
            while not visited[curr]:
                visited[curr] = True
                path.append(curr)
                curr = A[curr]
            
            # Check if curr is in the current path
            if curr in path:
                idx = path.index(curr)
                cycle = path[idx:]
                for node in cycle:
                    in_cycle[node] = True
                cycle_nodes.append(cycle)
            # Nodes not in a cycle are part of trees leading to cycles
            # They are already marked visited.

    # For each node, we need to compute W_u(v) for v in 1..M
    # W_u(v) = number of ways to assign the subtree at u given x_u = v
    # The subtree at u consists of u and all nodes that eventually flow into u (excluding the cycle edge if u is in a cycle).
    # Actually, the "subtree" for DP purposes is the set of nodes that have u as an ancestor in the reversed graph (A[i]->i).
    # Since the graph is functional, each node belongs to exactly one tree rooted at a cycle node.
    # We process nodes in reverse topological order (leaves to root).
    # The root of each tree is a cycle node.
    
    # We can compute the processing order using BFS from leaves.
    # In-degree in the reversed graph (which is out-degree in original) is 1 for all nodes.
    # But for the tree structure A[i]->i, the "parent" of i is A[i].
    # Leaves in the tree are nodes that have no children in the reversed graph (i.e., no j such that A[j] == i).
    
    # Let's compute the size of the subtree for each node to help with ordering?
    # Actually, we can just do a topological sort on the DAG formed by removing cycle edges.
    # Or simpler: since N is small, we can just process nodes in an order such that children are processed before parents.
    # We can compute this by starting with leaves (nodes with no children in the tree sense) and moving up.
    
    # Compute out-degree in the tree sense (number of children)
    # Note: For cycle nodes, we don't consider the cycle edge as part of the tree.
    # The tree rooted at a cycle node C includes C and all nodes that flow into C.
    # The parent of any non-cycle node u is A[u].
    
    # Let's compute the processing order using Kahn's algorithm on the tree edges.
    # The tree edges are u -> v if A[v] == u.
    # We want to process v before u.
    # So we look at in-degree in the tree graph? No, we want to process leaves first.
    # Leaves are nodes with no children.
    
    # Let's compute the number of children for each node in the tree structure.
    # For cycle nodes, we still count their non-cycle children.
    tree_children_count = [0] * (N + 1)
    for i in range(1, N + 1):
        if not in_cycle[i]:
            tree_children_count[A[i]] += 1
        else:
            # For cycle nodes, we count all children that are not in the cycle?
            # Actually, the DP for a cycle node u considers the tree rooted at u.
            # The children of u in this tree are all j such that A[j] == u.
            # Some of these j might be in the cycle (if the cycle has length > 1, no, because A[j] is the next node in cycle).
            # If j is in the cycle and A[j] == u, then j is the next node in the cycle.
            # We should NOT include cycle nodes as children in the tree DP for u.
            # So for a cycle node u, its tree children are j such that A[j] == u and j is NOT in the cycle.
            pass
            
    # Let's refine:
    # For any node u, let T(u) be the set of nodes in the tree rooted at u (including u).
    # The children of u in T(u) are all j such that A[j] == u and j is not in the cycle (if u is in cycle) or j is not in the cycle (if u is not in cycle, but u is not in cycle only if it's part of a tree leading to a cycle).
    # Actually, if u is not in a cycle, it is part of some tree. Its parent is A[u].
    # The DP state W_u(v) is defined for the subtree rooted at u in the tree structure.
    # The subtree rooted at u includes u and all descendants in the reversed graph (A[j]==u).
    # We must exclude any node that is part of a cycle from being a child in the tree DP, because the cycle constraint is handled separately.
    
    # So, for each node u, the children in the tree DP are:
    # children_tree[u] = [ j for j in children[u] if not in_cycle[j] ]
    # Wait, if u is in a cycle, its children in the tree are those j with A[j]==u and j not in cycle.
    # If u is not in a cycle, its children in the tree are those j with A[j]==u and j not in cycle.
    # But if u is not in a cycle, it is in a tree. Its parent is A[u].
    # The DP for u depends on its children in the tree.
    
    # Let's build the tree children list properly.
    tree_children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        if not in_cycle[i]:
            # i is not in a cycle, so it belongs to some tree.
            # Its parent is A[i].
            # If A[i] is in a cycle, then i is a child of the cycle node A[i] in the tree.
            # If A[i] is not in a cycle, then i is a child of A[i] in the tree.
            # In either case, i is a child of A[i] in the tree structure.
            tree_children[A[i]].append(i)
        else:
            # i is in a cycle. It is not a child of any node in the tree DP sense for its own component's cycle handling.
            # However, it might be a parent of some non-cycle nodes.
            pass
            
    # Now, we need to process nodes in reverse topological order (children before parents).
    # We can use a queue of nodes with no children in the tree (leaves).
    # But note: the tree is defined by tree_children.
    # Leaves are nodes with tree_children[u] == [].
    
    # Compute in-degree for the tree (number of children) is not needed for Kahn's if we just start with leaves.
    # We want to process a node after all its children are processed.
    # So we can compute the number of unprocessed children for each node.
    
    # Let's compute the number of children for each node in the tree structure.
    # This is just len(tree_children[u]).
    
    # We'll use a stack or queue for processing.
    # Initialize with all leaves.
    queue = []
    for i in range(1, N + 1):
        if len(tree_children[i]) == 0:
            queue.append(i)
            
    # We need to store the order of processing.
    processing_order = []
    
    # We also need to track how many children are left to process for each node.
    # Since we are building the tree from leaves up, we can decrement the count for the parent.
    # But wait, the parent of i is A[i].
    # When i is processed, we can decrement the count for A[i].
    # If A[i]'s count becomes 0, we add A[i] to the queue.
    
    # However, we must be careful: A[i] might be in a cycle.
    # If A[i] is in a cycle, it will be processed after all its non-cycle children are done.
    # But cycle nodes are not added to the queue initially if they have children.
    # They will be added when all their children are processed.
    
    # Let's compute the initial "remaining children count" for each node.
    remaining_children = [len(tree_children[i]) for i in range(N + 1)]
    
    # Re-initialize queue with leaves
    queue = [i for i in range(1, N + 1) if remaining_children[i] == 0]
    
    # We'll use a list as a queue
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        processing_order.append(u)
        
        parent = A[u]
        # If parent is not in a cycle, or even if it is, we decrement its remaining children count.
        # But we only add parent to queue if it's not in a cycle? No, we add it if it's not in a cycle AND remaining becomes 0?
        # Actually, cycle nodes are also processed in this order, but they are part of the cycle.
        # The DP for cycle nodes is computed the same way, but they are not "roots" of trees in the same sense.
        # They are roots of trees that include themselves and their non-cycle descendants.
        # So we should process them too.
        
        remaining_children[parent] -= 1
        if remaining_children[parent] == 0:
            queue.append(parent)
            
    # Now processing_order contains all nodes in an order such that children are processed before parents.
    # Note: This order might not be unique, but it's valid.
    
    # Initialize W[u][v] for all u, v
    # W[u][v] = number of ways to assign the subtree at u given x_u = v
    # We can use a 2D array: W[u][v] for u in 1..N, v in 1..M
    # Since M is up to 2025, and N is up to 2025, this is 2025*2025 ~ 4 million, which is fine.
    
    W = [[0] * (M + 1) for _ in range(N + 1)]
    
    # Process nodes in processing_order
    for u in processing_order:
        # Compute W[u][v] for v in 1..M
        # W[u][v] = product over children c of S[c][v]
        # where S[c][v] = sum_{k=1}^v W[c][k]
        
        # First, compute S[c][v] for all children c
        # If u has no children, W[u][v] = 1 for all v.
        
        if len(tree_children[u]) == 0:
            for v in range(1, M + 1):
                W[u][v] = 1
        else:
            # Compute W[u][v] for each v
            # We can compute it iteratively
            # W[u][1] = product_{c} S[c][1]
            # W[u][v] = W[u][v-1] * (product_{c} S[c][v]) / (product_{c} S[c][v-1]) ?
            # Division is not easy. Instead, we can compute the product directly for each v.
            # But that would be O(M * degree) per node, total O(N * M * avg_degree) = O(N * M).
            # Since sum of degrees is N, this is O(N * M).
            
            # Let's compute S[c][v] for all c and v first?
            # We can compute S[c][v] on the fly or store it.
            # Let's store S[c][v] in a temporary array or compute it.
            
            # For each v, W[u][v] = prod_{c in tree_children[u]} S[c][v]
            # S[c][v] = S[c][v-1] + W[c][v]
            
            # We can compute S[c][v] for all c and v.
            # Let's create a list of S values for each child.
            
            # Precompute S for all children
            # S[c] is a list of length M+1
            # S[c][v] = sum_{k=1}^v W[c][k]
            
            # We can compute S[c] for each child c
            child_S = []
            for c in tree_children[u]:
                S_c = [0] * (M + 1)
                current_sum = 0
                for v in range(1, M + 1):
                    current_sum = (current_sum + W[c][v]) % MOD
                    S_c[v] = current_sum
                child_S.append(S_c)
                
            # Now compute W[u][v]
            for v in range(1, M + 1):
                prod = 1
                for S_c in child_S:
                    prod = (prod * S_c[v]) % MOD
                W[u][v] = prod

    # Now, for each component, compute the answer.
    # The answer for a component is sum_{v=1}^M prod_{c in cycle} W[c][v]
    
    total_ans = 1
    
    for cycle in cycle_nodes:
        # For this cycle, compute P(v) = prod_{c in cycle} W[c][v] for each v
        # Then sum P(v) for v=1..M
        
        # Initialize P[v] = 1 for all v
        P = [1] * (M + 1)
        
        for c in cycle:
            for v in range(1, M + 1):
                P[v] = (P[v] * W[c][v]) % MOD
                
        comp_ans = 0
        for v in range(1, M + 1):
            comp_ans = (comp_ans + P[v]) % MOD
            
        total_ans = (total_ans * comp_ans) % MOD
        
    print(total_ans)

solve()