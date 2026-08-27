import sys
sys.setrecursionlimit(300000)

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return

    iterator = iter(data)
    try:
        N = int(next(iterator))
    except StopIteration:
        return

    if N < 5:
        # Minimum alkane needs at least 1 degree 4 node + 4 leaves = 5 nodes
        # Actually, a degree 4 node needs 4 neighbors. Each neighbor can be a leaf.
        # So min size is 5.
        print(-1)
        return

    adj = [[] for _ in range(N + 1)]
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # dp[u][k] = max vertices in a valid alkane-like subtree rooted at u
    # with exactly k children connected in the subgraph.
    # k can be 0, 1, 2, 3, 4.
    # A child v connected to u must be in a state where v's degree in the alkane is 1 or 4.
    # Since v is a child of u, v has a parent in the alkane.
    # So v's degree must be 4, meaning v has 3 children in the alkane (state dp[v][3]).
    # OR, v is a leaf in the alkane, meaning v has 0 children in the alkane (state dp[v][0]).
    # So the value contributed by connecting child v is max(dp[v][0], dp[v][3]).
    
    # Initialize dp table with -1 (invalid)
    # dp[u][0] is always 1 (just the node itself, no children)
    dp = [[-1] * 5 for _ in range(N + 1)]
    
    # Root the tree arbitrarily at 1
    parent = [0] * (N + 1)
    order = []
    stack = [1]
    visited = [False] * (N + 1)
    visited[1] = True
    
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # Process nodes in reverse topological order (leaves to root)
    for u in reversed(order):
        # Get children
        children = [v for v in adj[u] if v != parent[u]]
        
        # Base case: dp[u][0] = 1
        dp[u][0] = 1
        
        # Calculate the potential contribution of each child if connected
        # Contribution = max(dp[v][0], dp[v][3])
        # If dp[v][0] or dp[v][3] is -1, that child cannot be connected in a valid way
        child_vals = []
        for v in children:
            val0 = dp[v][0]
            val3 = dp[v][3]
            best = -1
            if val0 != -1:
                best = max(best, val0)
            if val3 != -1:
                best = max(best, val3)
            
            if best != -1:
                child_vals.append(best)
        
        # Sort child values in descending order to pick top k
        child_vals.sort(reverse=True)
        
        # Compute dp[u][k] for k=1 to 4
        current_sum = 0
        for k in range(1, 5):
            if k <= len(child_vals):
                current_sum += child_vals[k-1]
                dp[u][k] = 1 + current_sum
            else:
                dp[u][k] = -1

    # The answer is the maximum dp[r][4] over all nodes r.
    # dp[r][4] represents a valid alkane rooted at r with degree 4.
    ans = -1
    for u in range(1, N + 1):
        if dp[u][4] != -1:
            if dp[u][4] > ans:
                ans = dp[u][4]
                
    print(ans)

solve()