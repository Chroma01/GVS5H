import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        M = int(next(iterator))
        K = int(next(iterator))
    except StopIteration:
        return
    
    edges = []
    adj = [[] for _ in range(N + 1)]
    
    for i in range(M):
        u = int(next(iterator))
        v = int(next(iterator))
        edges.append((u, v))
        adj[u].append((v, i))
    
    # Binary search on the answer D
    # D can range from 0 to N-1 (max possible shortest path with 0/1 weights)
    # Actually, max path length is N-1 edges, so max distance is N-1.
    # But we can also have distance > N-1 if we use non-simple paths? No, shortest path is always simple.
    # So max answer is min(K, N-1).
    
    def can_achieve(D):
        """
        Check if it's possible to choose exactly K edges to set to 1
        such that the shortest path from 1 to N is at least D.
        
        This is equivalent to: can we choose K edges such that every path
        from 1 to N has at least D edges set to 1?
        
        We compute the minimum number of edges we need to set to 1 to ensure
        every path from 1 to N has at least D edges set to 1.
        If this minimum is <= K, then we can achieve D (by setting additional
        edges to 1 arbitrarily).
        
        We use DP: dp[v][j] = minimum number of edges set to 1 in the subgraph
        reachable from v such that every path from v to N has at least j edges set to 1.
        
        Since the graph may have cycles, we need to use iterative relaxation.
        """
        if D == 0:
            return True
        
        INF = float('inf')
        # dp[v][j] = minimum number of edges set to 1 in the subgraph reachable from v
        # such that every path from v to N has at least j edges set to 1.
        dp = [[INF] * (D + 1) for _ in range(N + 1)]
        
        # Base case
        dp[N][0] = 0
        
        # Use iterative relaxation (Bellman-Ford-like) for N iterations
        # This handles cycles correctly
        for iteration in range(N):
            changed = False
            for v in range(1, N + 1):
                if v == N:
                    continue
                
                # Get outgoing edges from v
                outgoing = adj[v]
                if not outgoing:
                    # No outgoing edges, so no paths to N
                    # dp[v][j] remains INF for all j > 0
                    continue
                
                degree = len(outgoing)
                
                # For each j from 0 to D
                for j in range(D + 1):
                    min_cost = INF
                    
                    # Iterate over all subsets of outgoing edges
                    # This is exponential in the degree, but for small degrees it's feasible
                    for mask in range(1 << degree):
                        cost = 0
                        valid = True
                        max_needed = 0
                        
                        for i in range(degree):
                            u, edge_idx = outgoing[i]
                            w = 1 if (mask & (1 << i)) else 0
                            cost += w
                            
                            needed = j - w
                            if needed < 0:
                                needed = 0
                            
                            if dp[u][needed] == INF:
                                valid = False
                                break
                            
                            max_needed = max(max_needed, dp[u][needed])
                        
                        if valid:
                            total_cost = cost + max_needed
                            if total_cost < min_cost:
                                min_cost = total_cost
                    
                    if min_cost < dp[v][j]:
                        dp[v][j] = min_cost
                        changed = True
            
            if not changed:
                break
        
        # Check if dp[1][D] <= K
        return dp[1][D] <= K
    
    # Binary search on D
    low = 0
    high = min(K, N - 1)
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        if can_achieve(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    
    print(ans)

solve()