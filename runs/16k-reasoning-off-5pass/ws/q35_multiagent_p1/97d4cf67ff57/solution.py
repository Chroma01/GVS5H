import sys

# Increase recursion depth to handle deep trees
sys.setrecursionlimit(300000)

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

    if N < 5:
        # An alkane requires at least one degree 4 node, which needs at least 5 nodes (1 center + 4 leaves)
        # Actually, a degree 4 node needs 4 neighbors. If those neighbors are leaves, total 5.
        # So minimum size is 5.
        print(-1)
        return

    adj = [[] for _ in range(N + 1)]
    
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Root the tree at 1
    parent = [0] * (N + 1)
    order = []
    stack = [1]
    visited = [False] * (N + 1)
    visited[1] = True
    
    # BFS/DFS to establish parent pointers and processing order
    # Using a stack for DFS order to get a topological sort from leaves up
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Process nodes in reverse order (leaves to root)
    # dp0[u]: max size of alkane subtree rooted at u where u is a LEAF in the alkane
    #         (u has no children in the alkane). Size is 1.
    # dp3[u]: max size of alkane subtree rooted at u where u is an INTERNAL node with 3 children in alkane
    #         (u will be connected to its parent in the alkane, making its degree 4).
    # dp4[u]: max size of alkane subtree rooted at u where u is the ROOT of the alkane with 4 children in alkane.
    
    dp0 = [1] * (N + 1)
    dp3 = [-float('inf')] * (N + 1)
    dp4 = [-float('inf')] * (N + 1)
    
    # Global answer
    ans = -float('inf')
    
    # Reverse order ensures children are processed before parents
    for u in reversed(order):
        # Collect values from children
        # For a child v connected to u, the best alkane structure at v is either:
        # - v is a leaf in the alkane (dp0[v] = 1)
        # - v is an internal node with 3 children in the alkane (dp3[v])
        # Note: v cannot be an internal node with 4 children if it's connected to u, 
        # because that would make v's degree 5 (1 parent + 4 children).
        
        child_vals = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            
            # The value contributed by child v if it is connected to u
            val = max(dp0[v], dp3[v])
            child_vals.append(val)
        
        # Sort in descending order to pick the largest values
        child_vals.sort(reverse=True)
        
        # Calculate dp3[u]: u has exactly 3 children in the alkane
        if len(child_vals) >= 3:
            # Sum of top 3 child values + 1 for u itself
            dp3[u] = 1 + sum(child_vals[:3])
        
        # Calculate dp4[u]: u has exactly 4 children in the alkane
        if len(child_vals) >= 4:
            # Sum of top 4 child values + 1 for u itself
            dp4[u] = 1 + sum(child_vals[:4])
            # Update global answer
            if dp4[u] > ans:
                ans = dp4[u]
    
    if ans == -float('inf'):
        print(-1)
    else:
        print(ans)

solve()