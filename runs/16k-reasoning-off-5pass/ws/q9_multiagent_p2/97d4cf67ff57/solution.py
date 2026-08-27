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

    # DP states:
    # 0: u not selected
    # 1: u selected, 0 children connected (needs parent to be leaf)
    # 2: u selected, 3 children connected (needs parent to be internal)
    # 3: u selected, 4 children connected (complete, u is internal)
    # 4: u selected, 1 child connected (complete, u is leaf)
    
    # We store tuples (max_size, max_size_with_deg4)
    # max_size_with_deg4 is -1 if impossible to have a degree 4 node in this component
    
    dp = [[(-1, -1)] * 5 for _ in range(N + 1)]

    def get_child_options(u):
        opts = []
        for v in adj[u]:
            d0, d1, d2, d3, d4 = dp[v]
            choices = []
            # Option: Don't connect (size 0)
            choices.append((0, False))
            # Option: Connect as leaf (state 1)
            if d1 != -1:
                choices.append((d1, False))
            # Option: Connect as internal (state 2)
            if d2 != -1:
                choices.append((d2, True))
            opts.append(choices)
        return opts

    def dfs(u, p):
        # State 0: u not selected
        dp[u][0] = (0, False)
        
        opts = get_child_options(u)
        
        # Helper to pick k children
        def pick_k(k, force_internal=False):
            if k == 0:
                return (0, False)
            
            INF = -10**18
            
            gains = []
            for i, choices in enumerate(opts):
                best_l = INF
                best_i = INF
                
                for s, is_int in choices:
                    if is_int:
                        if s > best_i:
                            best_i = s
                    else:
                        if s > best_l:
                            best_l = s
                
                # We can always choose "not connect" (size 0)
                # If we connect as leaf, gain is best_l.
                # If we connect as internal, gain is best_i.
                
                max_active = INF
                can_be_internal = (best_i != INF)
                
                if best_l != INF:
                    max_active = max(max_active, best_l)
                if best_i != INF:
                    max_active = max(max_active, best_i)
                
                gains.append({
                    'idx': i,
                    'max_active': max_active,
                    'best_l': best_l,
                    'best_i': best_i,
                    'can_internal': can_be_internal
                })
            
            # Sort by max_active descending
            gains.sort(key=lambda x: x['max_active'], reverse=True)
            
            # Check if we have enough children that can be active
            valid_count = 0
            for g in gains:
                if g['max_active'] != INF:
                    valid_count += 1
            
            if valid_count < k:
                return (-1, False)
            
            # Calculate sum of top k max_active
            sum_top_k = 0
            for i in range(k):
                sum_top_k += gains[i]['max_active']
            
            # Check if we have a degree 4 node in the top k selection
            has_internal_in_top_k = False
            for i in range(k):
                if gains[i]['best_i'] != INF:
                    if gains[i]['best_i'] >= gains[i]['best_l']:
                        has_internal_in_top_k = True
            
            # If we need to force an internal child
            if force_internal and not has_internal_in_top_k:
                best_forced = -10**18
                found = False
                
                # Iterate over which child is the "guaranteed internal" one
                for i in range(len(gains)):
                    if gains[i]['best_i'] == INF:
                        continue
                    
                    current_sum = gains[i]['best_i']
                    
                    # Pick k-1 others
                    others = []
                    for j in range(len(gains)):
                        if j == i:
                            continue
                        if gains[j]['max_active'] != INF:
                            others.append(gains[j]['max_active'])
                    
                    if len(others) < k - 1:
                        continue
                    
                    others.sort(reverse=True)
                    for val in others[:k-1]:
                        current_sum += val
                    
                    if current_sum > best_forced:
                        best_forced = current_sum
                        found = True
                
                if found:
                    return (best_forced, True)
                else:
                    return (-1, False)
            
            return (sum_top_k, has_internal_in_top_k)

        # State 1: 0 children
        dp[u][1] = (1, False)
        
        # State 2: 3 children
        res = pick_k(3, force_internal=False)
        if res[0] != -1:
            dp[u][2] = (res[0] + 1, res[1])
        else:
            dp[u][2] = (-1, False)
            
        # State 3: 4 children
        res = pick_k(4, force_internal=False)
        if res[0] != -1:
            dp[u][3] = (res[0] + 1, True)
        else:
            dp[u][3] = (-1, False)
            
        # State 4: 1 child
        res = pick_k(1, force_internal=False)
        if res[0] != -1:
            dp[u][4] = (res[0] + 1, res[1])
        else:
            dp[u][4] = (-1, False)

    dfs(1, -1)
    
    ans = -1
    
    # Check state 3 (root is internal)
    if dp[1][3][0] != -1:
        ans = max(ans, dp[1][3][0])
    
    # Check state 4 (root is leaf, child is internal)
    if dp[1][4][0] != -1 and dp[1][4][1]:
        ans = max(ans, dp[1][4][0])
        
    print(ans)

if __name__ == '__main__':
    solve()