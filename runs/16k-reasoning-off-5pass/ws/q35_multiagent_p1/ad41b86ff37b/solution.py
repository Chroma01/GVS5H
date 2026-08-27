import sys

# Increase recursion depth to handle deep trees
sys.setrecursionlimit(10**6)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    if N < 3:
        # Constraints say N >= 3, but handle small cases gracefully
        print(0)
        return

    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # We will iterate over each vertex as the potential center of the Snowflake Tree.
    # For each center, we analyze its branches (neighbors' subtrees).
    
    max_kept = 0

    # To avoid recursion depth issues and for efficiency, we can use iterative DFS for subtree calculations
    # However, since we root the tree at each center, we need to be careful.
    # A better approach: For each center c, we can run a DFS/BFS to compute branch sizes and costs.
    
    # Optimization: Precompute parent pointers and order for a fixed root? 
    # No, the root changes. We'll do a local DFS for each center.
    
    # To speed up, we can use a stack for DFS.
    
    for center in range(1, N + 1):
        # For the current center, we want to compute the best Snowflake Tree.
        # The center itself is kept.
        # We look at each neighbor as a potential arm.
        
        neighbors = adj[center]
        if not neighbors:
            continue
            
        # We need to compute for each branch (starting at neighbor) the list of costs.
        # Cost of a node v in the branch (away from center) is (subtree_size_at_v - 1).
        # We collect all such costs for the branch, sort them, and compute prefix sums.
        
        branch_costs = [] # List of lists, each inner list is sorted costs for a branch
        
        for neighbor in neighbors:
            # Perform DFS/BFS to traverse the branch starting at neighbor, avoiding center
            # We need subtree sizes relative to the branch root (neighbor).
            # Since the tree is unrooted, we treat neighbor as root of this branch.
            
            # Iterative DFS to compute subtree sizes and collect costs
            # Stack elements: (node, parent, state)
            # state 0: first visit, process children
            # state 1: after children, compute size
            
            stack = [(neighbor, center, 0)]
            order = [] # To store nodes in post-order for size computation
            
            # We also need to collect all nodes in the branch to compute costs
            branch_nodes = []
            
            while stack:
                u, p, state = stack.pop()
                if state == 0:
                    stack.append((u, p, 1))
                    for v in adj[u]:
                        if v != p:
                            stack.append((v, u, 0))
                else:
                    order.append(u)
                    branch_nodes.append(u)
            
            # Now compute subtree sizes in post-order
            # We can use a dictionary or array for sizes. Since branch_nodes is a list, we can map.
            # But creating a dict for each branch might be slow.
            # Instead, we can compute sizes on the fly if we process in reverse order of discovery?
            # No, post-order is needed.
            
            # Let's use a simple array for sizes, indexed by node ID.
            # But resetting it is O(N). We can use a dict for the current branch.
            subtree_size = {}
            costs = []
            
            # Process in post-order (which is the order we collected, since we appended after children)
            # Actually, the 'order' list is in post-order because we append when state=1.
            for u in order:
                sz = 1
                for v in adj[u]:
                    if v != center and v != subtree_size.get('parent', None): # Need parent info
                        pass
                # We need to know children. Let's store parent during DFS.
                pass
            
            # Let's redo DFS to store parent and compute sizes properly
            parent_map = {neighbor: center}
            stack = [neighbor]
            post_order = []
            
            # BFS or DFS to get traversal order
            # Using stack for DFS
            stack = [neighbor]
            visited = {neighbor}
            while stack:
                u = stack.pop()
                post_order.append(u)
                for v in adj[u]:
                    if v != parent_map[u] and v not in visited:
                        parent_map[v] = u
                        visited.add(v)
                        stack.append(v)
            
            # Post-order is reverse of BFS/DFS order? No.
            # We need to process children before parents.
            # Reverse post_order gives us an order where children are processed before parents?
            # In DFS, we visit parent, then children. So reverse DFS order is children first.
            # Let's use the 'post_order' from the first DFS which was correct.
            
            # Re-do the first DFS to get correct post-order and parent map
            parent_map = {neighbor: center}
            stack = [(neighbor, center)]
            post_order = []
            
            # We need to distinguish between first visit and after children.
            # Let's use a separate stack for processing.
            stack = [neighbor]
            visited = {neighbor}
            # To get post-order, we can do:
            # 1. Get all nodes in the branch.
            # 2. Sort them by depth descending? Or use the post-order from DFS.
            
            # Let's use the iterative DFS that produces post-order
            stack = [(neighbor, center, 0)]
            post_order = []
            parent_map = {neighbor: center}
            
            while stack:
                u, p, state = stack.pop()
                if state == 0:
                    stack.append((u, p, 1))
                    for v in adj[u]:
                        if v != p:
                            parent_map[v] = u
                            stack.append((v, u, 0))
                else:
                    post_order.append(u)
            
            # Now compute subtree sizes in post-order
            subtree_size = {}
            costs = []
            for u in post_order:
                sz = 1
                for v in adj[u]:
                    if v != parent_map[u]:
                        sz += subtree_size[v]
                subtree_size[u] = sz
                # Cost to make u a leaf is sz - 1
                costs.append(sz - 1)
            
            costs.sort()
            branch_costs.append(costs)
        
        # Now, for each possible y, compute the total kept vertices
        # y can range from 1 to max(len(c) for c in branch_costs)
        if not branch_costs:
            continue
            
        max_y = max(len(c) for c in branch_costs)
        
        # We want to compute for each y: sum of max(0, size_i - prefix_sum_i[y])
        # size_i is the size of branch i.
        branch_sizes = [len(c) + 1 for c in branch_costs] # +1 for the arm node itself? 
        # Wait, the branch includes the neighbor. The cost list includes costs for all nodes in the branch.
        # The size of the branch is the number of nodes in it.
        # Let's re-verify: 
        # branch_costs[i] has length = size of branch i.
        # subtree_size[neighbor] is the size of the branch.
        # So branch_sizes[i] = len(branch_costs[i])
        
        branch_sizes = [len(c) for c in branch_costs]
        
        # Precompute prefix sums for each branch
        prefix_sums = []
        for costs in branch_costs:
            ps = [0] * (len(costs) + 1)
            current = 0
            for i, c in enumerate(costs):
                current += c
                ps[i+1] = current
            prefix_sums.append(ps)
        
        # For each y from 1 to max_y
        # We can iterate y and sum up contributions
        # To optimize, we can iterate y and for each branch, if y <= len, add contribution
        
        # Since max_y can be up to N, and number of branches can be up to N, this is O(N^2) in worst case.
        # But we can prune: if y > max_y, break.
        
        current_total = 0
        # We can maintain the sum for each y? No, we just compute for each y.
        
        # Let's iterate y from 1 to max_y
        for y in range(1, max_y + 1):
            kept = 1 # Center
            for i in range(len(branch_costs)):
                if y <= branch_sizes[i]:
                    cost_sum = prefix_sums[i][y]
                    kept_in_branch = branch_sizes[i] - cost_sum
                    if kept_in_branch > 0:
                        kept += kept_in_branch
                # If y > branch_sizes[i], this branch cannot be an arm with y leaves
            if kept > max_kept:
                max_kept = kept

    # The answer is N - max_kept
    print(N - max_kept)

solve()