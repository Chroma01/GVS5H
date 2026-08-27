import sys
sys.setrecursionlimit(300000)

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        print(-1)
        return
        
    N = int(data[0])
    
    if N < 5:
        # Minimum alkane has 1 degree-4 node + 4 leaves = 5 nodes
        print(-1)
        return
    
    adj = [[] for _ in range(N + 1)]
    idx = 1
    for _ in range(N - 1):
        u = int(data[idx])
        v = int(data[idx + 1])
        idx += 2
        adj[u].append(v)
        adj[v].append(u)
    
    # Root the tree at 1
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
    
    # Process in reverse order (leaves to root)
    # dp[u][k] = max vertices in subtree rooted at u, where u has k children connected in the alkane
    # k can be 0, 1, 2, 3, 4
    # For a child v connected to u, v must have degree 1 or 4 in the alkane.
    # If v is connected to u, its degree is (number of children of v in alkane) + 1.
    # So if v has 0 children in alkane, degree = 1 (valid, leaf).
    # If v has 3 children in alkane, degree = 4 (valid, internal).
    # We cannot use dp[v][1], dp[v][2], dp[v][4] as contributions because:
    # - dp[v][1]: degree = 2, invalid
    # - dp[v][2]: degree = 3, invalid
    # - dp[v][4]: degree = 5, invalid
    
    INF = float('-inf')
    dp = [[INF] * 5 for _ in range(N + 1)]
    
    for u in reversed(order):
        # Collect valid contributions from children
        # For each child v, the value we can get if we connect v to u is:
        # max(dp[v][0], dp[v][3])
        # dp[v][0] = 1 (v is a leaf in the alkane)
        # dp[v][3] = size of alkane rooted at v with 3 children
        
        child_vals = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            # v is a child of u
            val0 = dp[v][0]
            val3 = dp[v][3]
            best = max(val0, val3)
            if best > INF / 2:  # valid
                child_vals.append(best)
        
        # Sort in descending order to pick the best k children
        child_vals.sort(reverse=True)
        
        # dp[u][0] = 1 (u is a leaf in the alkane, no children connected)
        dp[u][0] = 1
        
        # dp[u][k] for k > 0: 1 + sum of top k child_vals
        current_sum = 1
        for k in range(1, 5):
            if k <= len(child_vals):
                current_sum += child_vals[k - 1]
                dp[u][k] = current_sum
            else:
                dp[u][k] = INF
    
    # The answer is the maximum dp[u][4] over all u
    # dp[u][4] means u is the root of an alkane with 4 children, so u has degree 4.
    ans = INF
    for u in range(1, N + 1):
        if dp[u][4] > ans:
            ans = dp[u][4]
    
    if ans < 0:
        print(-1)
    else:
        print(ans)

solve()