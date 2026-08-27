import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    N = int(next(it))
    X = int(next(it))
    
    # Initialize DP arrays for each vitamin type
    dp1 = [0] + [-1] * X
    dp2 = [0] + [-1] * X
    dp3 = [0] + [-1] * X
    
    # Track total amounts per vitamin for upper bound
    tot = [0, 0, 0]
    
    # Process each food item
    for _ in range(N):
        v = int(next(it))
        a = int(next(it))
        c = int(next(it))
        tot[v-1] += a
        
        # Select the appropriate DP array
        if v == 1:
            dp = dp1
        elif v == 2:
            dp = dp2
        else:
            dp = dp3
        
        # 0-1 knapsack update (iterate backwards to avoid reuse)
        for w in range(X, c-1, -1):
            if dp[w-c] != -1:
                val = dp[w-c] + a
                if val > dp[w]:
                    dp[w] = val
    
    # Upper bound for binary search: minimum total among the three vitamins
    min_total = min(tot)
    
    # Function to check if target T is achievable
    def possible(T):
        total_cost = 0
        # Check vitamin 1
        found = -1
        for c in range(X+1):
            if dp1[c] >= T:
                found = c
                break
        if found == -1:
            return False
        total_cost += found
        
        # Check vitamin 2
        found = -1
        for c in range(X+1):
            if dp2[c] >= T:
                found = c
                break
        if found == -1:
            return False
        total_cost += found
        
        # Check vitamin 3
        found = -1
        for c in range(X+1):
            if dp3[c] >= T:
                found = c
                break
        if found == -1:
            return False
        total_cost += found
        
        return total_cost <= X
    
    # Binary search for the maximum feasible T
    lo = 0
    hi = min_total + 1
    while lo < hi:
        mid = (lo + hi) // 2
        if possible(mid):
            lo = mid + 1
        else:
            hi = mid
    
    print(lo - 1)

if __name__ == "__main__":
    solve()