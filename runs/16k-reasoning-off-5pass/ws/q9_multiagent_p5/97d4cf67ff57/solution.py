import sys

# Increase recursion depth just in case, though we use iterative approach
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

    if N == 0:
        print(-1)
        return

    adj = [[] for _ in range(N + 1)]
    degree = [0] * (N + 1)

    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)
        degree[u] += 1
        degree[v] += 1

    # If no node has degree >= 4, no alkane is possible
    # because every node in the core must have degree >= 4 in the original tree.
    if max(degree) < 4:
        print(-1)
        return

    # DP states for each node u:
    # dp[u][0]: u not in S, no core in subtree, u not in subgraph (contribution 0)
    # dp[u][1]: u not in S, no core in subtree, u is leaf (contribution 1)
    # dp[u][2]: u not in S, core exists in subtree, u not in subgraph (Impossible)
    # dp[u][3]: u not in S, core exists in subtree, u is leaf (Impossible)
    # dp[u][4]: u in S (degree 4 in subgraph)
    
    # Simplified logic derived:
    # If u is not in S:
    #   - If u is not in subgraph, the entire subtree contributes 0 (disconnected).
    #   - If u is a leaf in subgraph, it contributes 1, and all its children must be not in subgraph (contribution 0).
    #   - It is impossible for u (not in S) to be part of a core or have a core in its subtree while being a leaf.
    #   - It is impossible for u (not in S) to have a core in its subtree while u itself is not in subgraph (disconnected).
    # Therefore:
    #   dp[u][0] = 0
    #   dp[u][1] = 1
    #   dp[u][2] = -1 (impossible)
    #   dp[u][3] = -1 (impossible)
    
    # If u is in S:
    #   u must have degree 4 in the subgraph.
    #   Neighbors can be children (in S or leaves) or parent.
    #   In the DP (bottom-up), we calculate the max vertices in the subtree given u is in S.
    #   We assume the parent connection is handled later or u needs to fill its degree with children.
    #   Specifically, u needs 4 neighbors in the subgraph.
    #   Let k be the number of children in S.
    #   Let l be the number of children that are leaves.
    #   We must have k + l <= 4. The remaining 4 - (k+l) neighbors must be provided by the parent.
    #   If 4 - (k+l) > 0, the parent MUST be in the subgraph (either in S or as a leaf).
    #   If 4 - (k+l) == 0, the parent can be anything (not in subgraph or in subgraph).
    #   To maximize the score, for each child v, we have options:
    #     1. v in S: gain dp[v][4]
    #     2. v is leaf: gain 1
    #     3. v not in subgraph: gain 0
    #   We iterate k from 0 to 4 (number of children in S).
    #   For a fixed k, we pick the k children with the largest dp[v][4].
    #   Then we pick up to 4-k remaining children to be leaves (gain 1 each).
    #   The rest are ignored.
    
    # We use an iterative approach with a post-order traversal to avoid recursion depth issues.
    
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
    
    # Initialize DP table
    # dp[u] will be a list of 5 values
    dp = [[0] * 5 for _ in range(N + 1)]

    # Process in reverse order (bottom-up)
    for u in reversed(order):
        # Initialize base states for u not in S
        dp[u][0] = 0
        dp[u][1] = 1
        dp[u][2] = -1
        dp[u][3] = -1
        
        # If u cannot be in S (degree < 4), dp[u][4] remains -1
        if degree[u] < 4:
            dp[u][4] = -1
            continue
            
        # Collect children
        children = []
        for v in adj[u]:
            if v == parent[u]:
                continue
            children.append(v)
        
        # Prepare values for children
        # We need to sort children by dp[v][4] descending
        vals = []
        for v in children:
            s_val = dp[v][4]
            vals.append(s_val)
        
        vals.sort(reverse=True)
        
        # Calculate max for each k (number of children in S)
        current_max = -1
        
        # We can compute prefix sums of vals to quickly get sum of top k
        # But since k is small (0 to 4), we can just sum directly.
        
        for k in range(5):
            if k > len(children):
                break
            
            # Sum of top k children being in S
            sum_S = sum(vals[:k])
            
            # Remaining children
            rem = len(children) - k
            # Max L we can pick (children as leaves)
            # Constraint: k + l <= 4 => l <= 4 - k
            l = min(rem, 4 - k)
            
            # Check if valid (l must be >= 0, which is guaranteed by min)
            # Also check if we can actually form the degree 4 condition.
            # If k + l < 4, we need parent to fill the rest.
            # This is allowed in the DP state dp[u][4] because the parent connection is not yet decided.
            # The only hard constraint is that we cannot have more than 4 neighbors in the subgraph.
            # So k + l <= 4 is the only constraint.
            
            if l < 0: 
                continue
                
            # Total score: 1 (for u) + sum_S + l (leaves)
            score = 1 + sum_S + l
            
            if score > current_max:
                current_max = score
        
        dp[u][4] = current_max

    # Final answer is the maximum dp[u][4] over all u
    ans = -1
    for i in range(1, N + 1):
        if dp[i][4] > ans:
            ans = dp[i][4]
            
    print(ans)

if __name__ == '__main__':
    solve()