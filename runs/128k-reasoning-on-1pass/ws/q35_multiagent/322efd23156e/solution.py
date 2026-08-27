import sys
import bisect

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    try:
        N = int(next(iterator))
        X = int(next(iterator))
    except StopIteration:
        return
    
    foods = {1: [], 2: [], 3: []}
    
    for _ in range(N):
        v = int(next(iterator))
        a = int(next(iterator))
        c = int(next(iterator))
        foods[v].append((a, c))
        
    best_arrays = {}
    # Use a sufficiently small number for unreachable states
    # Max possible sum of A_i is 5000 * 200000 = 10^9
    # So -10^15 is safe
    NEG_INF = -10**15
    
    for v in [1, 2, 3]:
        items = foods[v]
        dp = [NEG_INF] * (X + 1)
        dp[0] = 0
        
        max_reachable = 0
        
        # Local reference for speed
        dp_arr = dp
        
        for a, c in items:
            upper = max_reachable + c
            if upper > X:
                upper = X
            
            # Update dp table
            # Iterate backwards to avoid using the same item multiple times
            for j in range(upper, c - 1, -1):
                val = dp_arr[j-c] + a
                if val > dp_arr[j]:
                    dp_arr[j] = val
            
            max_reachable = upper
            
        # Compute prefix maximums
        # best[c] = max value achievable with cost <= c
        best = [0] * (X + 1)
        curr = NEG_INF
        for j in range(X + 1):
            if dp[j] > curr:
                curr = dp[j]
            best[j] = curr
        best_arrays[v] = best

    # Binary search for the maximum possible minimum intake
    low = 0
    high = 0
    for v in [1, 2, 3]:
        for a, c in foods[v]:
            high += a
            
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        
        total_cost = 0
        feasible = True
        
        for v in [1, 2, 3]:
            best = best_arrays[v]
            # Find the smallest cost c such that best[c] >= mid
            # bisect_left returns the first index where best[i] >= mid
            idx = bisect.bisect_left(best, mid)
            
            if idx > X:
                feasible = False
                break
            
            total_cost += idx
            if total_cost > X:
                feasible = False
                break
        
        if feasible:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
            
    print(ans)

if __name__ == '__main__':
    solve()