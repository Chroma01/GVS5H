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

    if N == 1:
        # A single node has degree 0, which is not 1 or 4.
        # Also, no vertex has degree 4.
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
    
    # BFS/DFS to determine processing order (bottom-up)
    while stack:
        u = stack.pop()
        order.append(u)
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                parent[v] = u
                stack.append(v)
    
    # dp[u][k][h]
    # k: number of children of u selected in the subgraph (0 to 4)
    # h: 0 if no degree-4 node in subtree, 1 if at least one degree-4 node exists
    # Value: max vertices in the subtree, or -inf if invalid
    INF_NEG = -10**9
    dp = [[[INF_NEG] * 2 for _ in range(5)] for _ in range(N + 1)]

    # Process nodes in reverse topological order (leaves to root)
    for u in reversed(order):
        # Initialize dp[u] for leaf case first, then update with children
        # Start with state where 0 children are selected
        dp[u][0][0] = 1
        dp[u][0][1] = INF_NEG # Cannot have a degree-4 node if only u is present and it's a leaf (deg 1)
        
        # Collect gains from children
        # For each child v, we can include it or not.
        # If included, v must have degree 1 (0 children selected) or degree 4 (3 children selected).
        
        gains = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            
            # Option 1: Include v as degree 1 in subgraph
            # v has 0 children selected.
            # Gain is dp[v][0][0] (no 4 in v's subtree) or dp[v][0][1] (has 4 in v's subtree)
            val0_no4 = dp[v][0][0]
            val0_with4 = dp[v][0][1]
            
            # Option 2: Include v as degree 4 in subgraph
            # v has 3 children selected.
            # v itself is degree 4, so has4 must be 1.
            val3_with4 = dp[v][3][1]
            # dp[v][3][0] is invalid because v has degree 4, so has4 must be 1.
            
            # We want to form pairs (gain, has4_flag) for including v.
            # If we include v, we can choose the best configuration for v.
            # Best with has4=0: only possible if v has degree 1 and no 4 in subtree.
            best_no4 = val0_no4
            # Best with has4=1: max of (v deg 1 with 4 in subtree, v deg 4)
            best_with4 = INF_NEG
            if val0_with4 != INF_NEG:
                best_with4 = max(best_with4, val0_with4)
            if val3_with4 != INF_NEG:
                best_with4 = max(best_with4, val3_with4)
            
            # If both are invalid, this child cannot be included.
            if best_no4 == INF_NEG and best_with4 == INF_NEG:
                continue
                
            gains.append((best_no4, best_with4))
        
        # Now merge gains into dp[u]
        # Current dp[u] represents states before considering any children (only u itself)
        # We iterate through each child's gain and update dp[u]
        
        # We need a temporary array for the next state
        # dp[u][k][h] can transition to dp[u][k+1][h'] by adding a child
        
        # Initialize temp with current dp[u]
        # But since we are building up k, we should process children one by one.
        # Let's use a temporary DP table for the current node being built.
        
        # Start with the base state (0 children selected)
        # cur_dp[k][h]
        cur_dp = [[INF_NEG] * 2 for _ in range(5)]
        cur_dp[0][0] = 1
        cur_dp[0][1] = INF_NEG
        
        for (g_no4, g_with4) in gains:
            new_dp = [[INF_NEG] * 2 for _ in range(5)]
            
            # For each possible number of children selected so far (k)
            for k in range(5):
                for h in range(2):
                    if cur_dp[k][h] == INF_NEG:
                        continue
                    
                    # Option 1: Don't include the current child
                    # State remains (k, h)
                    if cur_dp[k][h] > new_dp[k][h]:
                        new_dp[k][h] = cur_dp[k][h]
                    
                    # Option 2: Include the current child
                    # New number of children: k + 1
                    if k + 1 <= 4:
                        # If we include with has4=0 (only possible if g_no4 is valid)
                        if g_no4 != INF_NEG:
                            # New has4 is h OR 0 = h
                            val = cur_dp[k][h] + g_no4
                            if val > new_dp[k+1][h]:
                                new_dp[k+1][h] = val
                        
                        # If we include with has4=1 (g_with4 is valid)
                        if g_with4 != INF_NEG:
                            # New has4 is h OR 1 = 1
                            val = cur_dp[k][h] + g_with4
                            if val > new_dp[k+1][1]:
                                new_dp[k+1][1] = val
            
            cur_dp = new_dp
        
        # After processing all children, copy cur_dp to dp[u]
        for k in range(5):
            for h in range(2):
                dp[u][k][h] = cur_dp[k][h]

    # The root is 1. It has no parent.
    # So its degree in the subgraph is exactly k.
    # Valid alkane requires:
    # 1. Root degree is 1 or 4.
    # 2. At least one vertex of degree 4 in the entire subgraph (has4 == 1).
    
    ans = INF_NEG
    
    # Check k=1, has4=1
    if dp[1][1][1] != INF_NEG:
        ans = max(ans, dp[1][1][1])
        
    # Check k=4, has4=1
    if dp[1][4][1] != INF_NEG:
        ans = max(ans, dp[1][4][1])
        
    if ans == INF_NEG:
        print(-1)
    else:
        print(ans)

solve()