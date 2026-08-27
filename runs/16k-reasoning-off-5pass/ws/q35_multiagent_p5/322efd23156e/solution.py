import sys

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

    # Separate foods by vitamin type
    foods_by_vit = {1: [], 2: [], 3: []}
    for v, a, c in foods:
        foods_by_vit[v].append((a, c))

    # Precompute total vitamins for each type to set upper bound for binary search
    total_vit = {}
    for v in [1, 2, 3]:
        total_vit[v] = sum(a for a, c in foods_by_vit[v])
    
    max_possible_k = min(total_vit[1], total_vit[2], total_vit[3])
    
    # If max_possible_k is 0, answer is 0
    if max_possible_k == 0:
        print(0)
        return

    # DP function for a single vitamin type
    # Returns the minimum calories to get at least k units of this vitamin
    # If not possible, returns infinity
    def min_calories_for_vitamin(vitamin_type, k):
        if k == 0:
            return 0
        
        items = foods_by_vit[vitamin_type]
        if not items:
            return float('inf')
        
        # dp[w] = max units of vitamin achievable with exactly w calories
        dp = [-1] * (X + 1)
        dp[0] = 0
        
        for a, c in items:
            # Update dp in reverse order
            for w in range(X, c - 1, -1):
                if dp[w - c] != -1:
                    new_units = dp[w - c] + a
                    if new_units > dp[w]:
                        dp[w] = new_units
        
        # Find minimum w such that dp[w] >= k
        for w in range(X + 1):
            if dp[w] >= k:
                return w
        
        return float('inf')

    # Check function for binary search
    def check(k):
        c1 = min_calories_for_vitamin(1, k)
        if c1 == float('inf'):
            return False
        c2 = min_calories_for_vitamin(2, k)
        if c2 == float('inf'):
            return False
        c3 = min_calories_for_vitamin(3, k)
        if c3 == float('inf'):
            return False
        
        return (c1 + c2 + c3) <= X

    # Binary search for the maximum k
    low = 0
    high = max_possible_k
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
    
    print(ans)

solve()