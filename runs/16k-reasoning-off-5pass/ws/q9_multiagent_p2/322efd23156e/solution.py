import sys

# Increase recursion depth just in case, though not used here
sys.setrecursionlimit(2000)

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

    foods = []
    for _ in range(N):
        v = int(next(iterator))
        a = int(next(iterator))
        c = int(next(iterator))
        foods.append((v, a, c))

    # The maximum possible answer k is bounded by X/3 because each food provides exactly one vitamin
    # and each food costs at least 1 calorie. To get k of each vitamin, we need at least 3k foods,
    # costing at least 3k calories. Thus 3k <= X => k <= X/3.
    # Since X <= 5000, k <= 1666.
    
    limit_k = X // 3

    # Helper to compute min costs for a list of foods
    # Returns a list where dp[k] is the minimum calories to get >= k units of vitamin
    def get_min_costs(foods_list, limit):
        # dp[v] = min calories to get exactly v units (capped at limit)
        # Initialize with infinity
        dp = [float('inf')] * (limit + 1)
        dp[0] = 0
        
        for a, c in foods_list:
            # Iterate backwards to simulate 0/1 knapsack (each food used at most once)
            for v in range(limit, -1, -1):
                if dp[v] == float('inf'):
                    continue
                next_v = v + a
                if next_v > limit:
                    next_v = limit
                if dp[v] + c < dp[next_v]:
                    dp[next_v] = dp[v] + c
        return dp

    foods1 = []
    foods2 = []
    foods3 = []
    
    for v, a, c in foods:
        if v == 1:
            foods1.append((a, c))
        elif v == 2:
            foods2.append((a, c))
        else:
            foods3.append((a, c))
            
    costs1 = get_min_costs(foods1, limit_k)
    costs2 = get_min_costs(foods2, limit_k)
    costs3 = get_min_costs(foods3, limit_k)
    
    # Find max k
    ans = 0
    for k in range(limit_k, -1, -1):
        c1 = costs1[k]
        c2 = costs2[k]
        c3 = costs3[k]
        # Check if all vitamins can be achieved and total calories within limit
        if c1 != float('inf') and c2 != float('inf') and c3 != float('inf'):
            if c1 + c2 + c3 <= X:
                ans = k
                break
                
    print(ans)

if __name__ == '__main__':
    solve()