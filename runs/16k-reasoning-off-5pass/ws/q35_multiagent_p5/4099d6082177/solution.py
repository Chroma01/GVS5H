import sys

# Increase recursion depth just in case, though we will use iterative approach
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        N = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return

    total_nodes = N * K
    
    # Edge case: K=1 means every node is a path of length 1. Always possible.
    if K == 1:
        print("Yes")
        return

    # Build adjacency list
    adj = [[] for _ in range(total_nodes + 1)]
    for _ in range(total_nodes - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Root the tree at node 1
    # We need parent pointers and a processing order (bottom-up)
    # Use BFS to establish parent pointers and get a topological order from root to leaves
    parent = [0] * (total_nodes + 1)
    order = []
    queue = [1]
    visited_bfs = [False] * (total_nodes + 1)
    visited_bfs[1] = True
    
    # Standard BFS to build tree structure and get order
    idx = 0
    while idx < len(queue):
        u = queue[idx]
        idx += 1
        order.append(u)
        
        for v in adj[u]:
            if not visited_bfs[v]:
                visited_bfs[v] = True
                parent[v] = u
                queue.append(v)
    
    # Process nodes in reverse order (from leaves up to root)
    # dp[u] will store the length of the path segment ending at u that is "open" (needs to be extended to parent)
    # If a node completes a path, we can consider its open length as 0 or -1, but let's stick to:
    # dp[u] = length of the path segment starting from some descendant and ending at u, which is NOT yet completed.
    # If all paths from children are completed, dp[u] = 1 (starting a new path at u).
    
    dp = [0] * (total_nodes + 1)
    
    # Reverse order gives us leaves first, then their parents, etc.
    for u in reversed(order):
        # Collect lengths from children
        # Children are neighbors except parent
        # Since we rooted at 1, children are nodes v where parent[v] == u
        
        # We can iterate over adj[u] and skip parent[u]
        incomplete_children = []
        
        for v in adj[u]:
            if v == parent[u]:
                continue
            # v is a child
            len_v = dp[v]
            if len_v < K:
                incomplete_children.append(len_v)
            # If len_v == K, it's a complete path, so it doesn't need extension.
            # If len_v > K, it's invalid, but our logic should prevent this.
        
        num_incomplete = len(incomplete_children)
        
        if num_incomplete > 1:
            # Cannot extend more than one path through this node
            print("No")
            return
        
        if num_incomplete == 1:
            # Extend the single incomplete path
            dp[u] = incomplete_children[0] + 1
        else:
            # No incomplete paths from children. Start a new path at u.
            dp[u] = 1
            
        if dp[u] > K:
            print("No")
            return

    # After processing all nodes, check the root
    # The root doesn't have a parent to extend to, so its path must be exactly complete (length K)
    if dp[1] == K:
        print("Yes")
    else:
        print("No")

solve()