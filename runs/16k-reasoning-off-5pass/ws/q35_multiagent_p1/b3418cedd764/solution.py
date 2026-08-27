import sys

# Increase recursion depth just in case, though we'll use iterative DP
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
        A = [0] * (N + 1)
        for i in range(1, N + 1):
            A[i] = int(next(iterator))
    except StopIteration:
        return

    MOD = 998244353

    # Build the graph: edges i -> A[i]
    # We need to process trees rooted at cycle nodes.
    # The "children" of a node u in the tree sense are nodes v such that A[v] = u.
    children = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        children[A[i]].append(i)

    # Identify components and cycles
    # Each component has exactly one cycle.
    # We can find cycles using visited states.
    visited = [0] * (N + 1)  # 0: unvisited, 1: visiting, 2: visited
    cycle_nodes = set()
    component_id = [0] * (N + 1)
    comp_count = 0
    
    # To process trees, we need to know which nodes belong to which component
    # and identify the cycle nodes in each component.
    
    # Step 1: Find all cycles and mark nodes
    # We can do this by traversing each unvisited node.
    for start_node in range(1, N + 1):
        if visited[start_node] != 0:
            continue
        
        path = []
        curr = start_node
        while visited[curr] == 0:
            visited[curr] = 1
            path.append(curr)
            curr = A[curr]
        
        if visited[curr] == 1:
            # Found a cycle. The cycle starts at curr and ends before the next occurrence of curr in path.
            # Actually, curr is the first node in the current path that is being revisited.
            # So the cycle is the suffix of path starting from the first occurrence of curr.
            cycle_start_index = path.index(curr)
            cycle = path[cycle_start_index:]
            for node in cycle:
                cycle_nodes.add(node)
        
        # Mark all nodes in path as visited (2)
        for node in path:
            visited[node] = 2

    # Step 2: Assign component IDs and identify cycle nodes per component
    # We can do a BFS/DFS from each unvisited node to find its component.
    # But since we know the structure, we can just traverse.
    # Actually, let's just group nodes by component.
    # We can use a simple traversal.
    
    comp_of_node = [0] * (N + 1)
    comp_cycle_nodes = {} # comp_id -> list of cycle nodes
    
    comp_id_counter = 0
    
    # We need to process each component.
    # Let's iterate through all nodes and if not assigned, start a new component.
    for i in range(1, N + 1):
        if comp_of_node[i] != 0:
            continue
        
        comp_id_counter += 1
        cid = comp_id_counter
        
        # BFS/DFS to find all nodes in this component
        stack = [i]
        comp_nodes = []
        while stack:
            u = stack.pop()
            if comp_of_node[u] != 0:
                continue
            comp_of_node[u] = cid
            comp_nodes.append(u)
            
            # Add children to stack
            for v in children[u]:
                if comp_of_node[v] == 0:
                    stack.append(v)
        
        # Identify cycle nodes in this component
        c_cycle = [u for u in comp_nodes if u in cycle_nodes]
        comp_cycle_nodes[cid] = c_cycle

    # Step 3: Compute DP for trees
    # f[u][k] = number of ways to assign subtree at u such that x_u <= k
    # We process nodes in post-order (leaves to root).
    # Since it's a functional graph, we can process in reverse topological order of the trees.
    # The roots of the trees are the cycle nodes.
    # We can compute f[u][k] for all u and k in [1, M].
    
    # To get post-order, we can do a DFS from each cycle node into its tree.
    # Or simply, since N is small, we can do a topological sort based on distance from cycle?
    # Actually, we can just process nodes in decreasing order of depth from cycle.
    # But easier: use memoization or iterative DP with correct order.
    # Since children are processed before parents, we can process in reverse topological order.
    # We can compute in-degrees in the "tree" sense (where edges are u -> child if A[child]=u).
    # Wait, the tree edges are directed from child to parent in the functional graph.
    # So in the tree structure, edges go from u to children[u].
    # We want to process children before parents.
    # We can do a BFS from leaves? Or just use recursion with memoization.
    
    # Let's use iterative DP. We need an order where children are processed before parents.
    # We can compute the depth of each node from the cycle.
    # Nodes in cycle have depth 0.
    # Nodes pointing to cycle nodes have depth 1, etc.
    
    depth = [-1] * (N + 1)
    queue = []
    
    # Initialize cycle nodes with depth 0
    for u in cycle_nodes:
        depth[u] = 0
        queue.append(u)
        
    # BFS to assign depths
    # Note: edges in functional graph are u -> A[u].
    # In the tree, A[u] is the parent of u.
    # So if we know depth of A[u], depth of u is depth[A[u]] + 1.
    # But we start from cycle nodes.
    # We need to traverse backwards: from parent to children.
    # So we use the children list.
    
    # Re-do BFS using children list
    from collections import deque
    q = deque()
    for u in cycle_nodes:
        depth[u] = 0
        q.append(u)
        
    while q:
        u = q.popleft()
        for v in children[u]:
            if depth[v] == -1:
                depth[v] = depth[u] + 1
                q.append(v)
                
    # Now process nodes in decreasing order of depth.
    # This ensures that when we process u, all its children (which have greater depth) are already processed.
    nodes_by_depth = [[] for _ in range(N + 1)]
    for i in range(1, N + 1):
        if depth[i] != -1:
            nodes_by_depth[depth[i]].append(i)
            
    # f[u][k] will be stored in a list of size M+1 for each node u
    # f[u][k] = product over v in children[u] of f[v][k]
    # Base case: leaf node u, f[u][k] = k
    
    f = [[0] * (M + 1) for _ in range(N + 1)]
    
    for d in range(N, -1, -1):
        for u in nodes_by_depth[d]:
            # Compute f[u][k] for k in 1..M
            # If u is a leaf (no children), f[u][k] = k
            if not children[u]:
                for k in range(1, M + 1):
                    f[u][k] = k
            else:
                # f[u][k] = product_{v in children[u]} f[v][k]
                # We can compute this for each k
                for k in range(1, M + 1):
                    prod = 1
                    for v in children[u]:
                        prod = (prod * f[v][k]) % MOD
                    f[u][k] = prod

    # Step 4: Compute the answer
    # For each component, and for each value v in 1..M,
    # the number of ways for the component is product over r in cycle_nodes of T_r(v)
    # where T_r(v) is the number of ways to assign the tree at r with x_r = v.
    # T_r(v) = product_{v_child in children[r]} f[v_child][v]
    # Note: f[r][v] = product_{v_child in children[r]} f[v_child][v] = T_r(v)
    # So for a component with cycle C, the ways for value v is product_{r in C} f[r][v].
    
    # Let total_ways[v] = product over all components of (product_{r in C_comp} f[r][v])
    # Then answer = sum_{v=1}^M total_ways[v]
    
    # We can compute this by initializing an array ans_v of size M+1 with 1s.
    # For each component, for each cycle node r, multiply ans_v[v] by f[r][v] for all v.
    
    ans_v = [1] * (M + 1)
    
    for cid in range(1, comp_id_counter + 1):
        c_cycle = comp_cycle_nodes[cid]
        for r in c_cycle:
            for v in range(1, M + 1):
                ans_v[v] = (ans_v[v] * f[r][v]) % MOD
                
    total_ans = 0
    for v in range(1, M + 1):
        total_ans = (total_ans + ans_v[v]) % MOD
        
    print(total_ans)

solve()