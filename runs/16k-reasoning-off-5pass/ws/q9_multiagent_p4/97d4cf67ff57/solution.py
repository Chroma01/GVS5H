import sys

# Increase recursion depth for deep trees
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
    for _ in range(N - 1):
        u = int(next(iterator))
        v = int(next(iterator))
        adj[u].append(v)
        adj[v].append(u)

    # Minimum alkane: 1 hub (deg 4) + 4 leaves = 5 vertices.
    if N < 5:
        print(-1)
        return

    # Tree DP
    # We root the tree at 1.
    # dp[u][k][0]: max vertices in subtree u, u has k connections to children, NO hub in subtree
    # dp[u][k][1]: max vertices in subtree u, u has k connections to children, AT LEAST ONE hub in subtree
    # k ranges from 0 to 4.
    
    # Build parent pointers and processing order (BFS)
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
    
    # Initialize DP tables
    # dp[u][k][state]
    dp = [[[-1] * 2 for _ in range(5)] for _ in range(N + 1)]

    # Process in reverse topological order (leaves to root)
    for u in reversed(order):
        # Base case: u is included, 0 children connected.
        # This is valid for state 0 (no hub yet).
        # State 1 is impossible with just u (size 1, no hub).
        dp[u][0][0] = 1
        dp[u][0][1] = -1
        
        children = [v for v in adj[u] if v != parent[u]]
        
        if not children:
            continue
            
        # We will maintain a list of best (k, val0, val1) for the current node u
        # Initially: [(0, 1, -1)]
        current_states = [(0, 1, -1)]
        
        for v in children:
            # Prepare options for child v
            # Option 0: Exclude v -> (k=0, val0=0, val1=-1)
            # Option 1..: Include v with k_v connections -> (k=k_v, val0=dp[v][k_v][0], val1=dp[v][k_v][1])
            
            child_options = [(0, 0, -1)] # Exclude
            
            for k_v in range(5):
                v0 = dp[v][k_v][0]
                v1 = dp[v][k_v][1]
                if v0 != -1:
                    child_options.append((k_v, v0, -1))
                if v1 != -1:
                    child_options.append((k_v, -1, v1))
            
            # Merge current_states with child_options
            new_current_states = {} # key: k, value: (val0, val1)
            
            for k_u, val0_u, val1_u in current_states:
                if val0_u == -1 and val1_u == -1:
                    continue
                
                for k_v, val0_v, val1_v in child_options:
                    # Check validity of child option
                    if val0_v == -1 and val1_v == -1:
                        continue
                        
                    nk = k_u + k_v
                    if nk > 4:
                        continue
                    
                    # Update state 0 (both u and v have no hub in their respective parts)
                    # State 0 is only valid if nk is 0 or 1 (u cannot be a hub)
                    if val0_u != -1 and val0_v != -1:
                        if nk <= 1:
                            new_val0 = val0_u + val0_v
                            if nk not in new_current_states or new_current_states[nk][0] < new_val0:
                                new_current_states[nk] = (new_val0, -1)
                    
                    # Update state 1 (at least one hub exists)
                    # State 1 is valid for nk in {0, 1, 3, 4}
                    # Case 1: u has hub, v has no hub
                    if val1_u != -1 and val0_v != -1:
                        new_val1 = val1_u + val0_v
                        if nk not in new_current_states or new_current_states[nk][1] < new_val1:
                            new_current_states[nk] = (new_current_states[nk][0], new_val1)
                            
                    # Case 2: u has no hub, v has hub
                    if val0_u != -1 and val1_v != -1:
                        new_val1 = val0_u + val1_v
                        if nk not in new_current_states or new_current_states[nk][1] < new_val1:
                            new_current_states[nk] = (new_current_states[nk][0], new_val1)
                            
                    # Case 3: both have hub
                    if val1_u != -1 and val1_v != -1:
                        new_val1 = val1_u + val1_v
                        if nk not in new_current_states or new_current_states[nk][1] < new_val1:
                            new_current_states[nk] = (new_current_states[nk][0], new_val1)
            
            # Update current_states
            current_states = list(new_current_states.values())
            
            # Ensure we have the best values for each k in the final dp table
            best = {}
            for k, v0, v1 in current_states:
                if k not in best:
                    best[k] = (v0, v1)
                else:
                    if v0 > best[k][0]:
                        best[k] = (v0, v1)
                    if v1 > best[k][1]:
                        best[k] = (v0, v1)
            
            for k in range(5):
                if k in best:
                    dp[u][k][0] = best[k][0]
                    dp[u][k][1] = best[k][1]
                else:
                    dp[u][k][0] = -1
                    dp[u][k][1] = -1

    # The answer is the maximum of dp[u][k][1] for all u and k in {1, 4}
    # Because the root of the alkane subgraph (in the rooted tree) must be a leaf (k=1) or a hub (k=4).
    # And we need at least one hub in the subgraph.
    ans = -1
    for u in range(1, N + 1):
        for k in [1, 4]:
            if dp[u][k][1] != -1:
                ans = max(ans, dp[u][k][1])
    
    print(ans)

if __name__ == '__main__':
    solve()