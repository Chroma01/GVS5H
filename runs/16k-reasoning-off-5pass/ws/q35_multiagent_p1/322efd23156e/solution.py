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
    vit1 = []
    vit2 = []
    vit3 = []
    
    for v, a, c in foods:
        if v == 1:
            vit1.append((a, c))
        elif v == 2:
            vit2.append((a, c))
        else:
            vit3.append((a, c))

    # Function to compute all possible (vitamin_amount, min_calories) pairs for a list of foods
    # Returns a list of tuples (vit, cost)
    def get_possibilities(items):
        # dp[c] = max vitamin amount achievable with exactly c calories
        # Initialize with -1 (impossible)
        # Max possible calories is X
        dp = [-1] * (X + 1)
        dp[0] = 0
        
        for a, c in items:
            # Iterate backwards to avoid using the same item multiple times
            for j in range(X, c - 1, -1):
                if dp[j - c] != -1:
                    new_vit = dp[j - c] + a
                    if new_vit > dp[j]:
                        dp[j] = new_vit
        
        # Collect all possible (vit, cost) pairs
        possibilities = []
        for cost in range(X + 1):
            if dp[cost] != -1:
                possibilities.append((dp[cost], cost))
        return possibilities

    # Precompute possibilities for each vitamin type
    poss1 = get_possibilities(vit1)
    poss2 = get_possibilities(vit2)
    poss3 = get_possibilities(vit3)
    
    # Sort possibilities by cost to optimize the check
    # For each vitamin, we want to find if there exists a combination with total cost <= X
    # and min(v1, v2, v3) >= K
    
    # To speed up, for each vitamin, we can create a list of (cost, max_vit)
    # and then for a given cost, we know the max vitamin.
    # But we need to combine them.
    
    # Let's sort each possibility list by cost
    poss1.sort(key=lambda x: x[1])
    poss2.sort(key=lambda x: x[1])
    poss3.sort(key=lambda x: x[1])
    
    # For each vitamin, create an array where arr[c] = max vitamin achievable with cost <= c
    # This allows O(1) lookup for max vitamin with cost <= c
    def preprocess_possibilities(possibilities):
        max_vit = 0
        arr = [0] * (X + 1)
        # We need to fill arr[c] with the max vitamin achievable with cost <= c
        # First, create a temp array with exact costs
        temp = [-1] * (X + 1)
        for vit, cost in possibilities:
            if vit > temp[cost]:
                temp[cost] = vit
        
        # Now compute prefix max
        current_max = 0
        for c in range(X + 1):
            if temp[c] != -1:
                if temp[c] > current_max:
                    current_max = temp[c]
            arr[c] = current_max
        return arr

    max_v1_by_cost = preprocess_possibilities(poss1)
    max_v2_by_cost = preprocess_possibilities(poss2)
    max_v3_by_cost = preprocess_possibilities(poss3)
    
    # Binary search for the maximum K
    low = 0
    high = 0
    # Upper bound for K: min of total vitamins of each type
    # But we can just use a large number, since if K is too large, it will fail
    # Max possible vitamin sum for one type is N * 200000 = 10^9
    # But we can cap high at 10^9
    
    # Calculate total vitamins for each type to set a tighter upper bound
    total_v1 = sum(a for a, c in vit1)
    total_v2 = sum(a for a, c in vit2)
    total_v3 = sum(a for a, c in vit3)
    
    high = min(total_v1, total_v2, total_v3)
    
    ans = 0
    
    while low <= high:
        mid = (low + high) // 2
        
        # Check if it's possible to have min(v1, v2, v3) >= mid
        # We need to find if there exists c1, c2, c3 such that:
        # c1 + c2 + c3 <= X
        # max_v1_by_cost[c1] >= mid
        # max_v2_by_cost[c2] >= mid
        # max_v3_by_cost[c3] >= mid
        
        # For each vitamin, find the minimum cost to achieve at least mid vitamins
        min_c1 = -1
        for c in range(X + 1):
            if max_v1_by_cost[c] >= mid:
                min_c1 = c
                break
        
        if min_c1 == -1:
            low = mid + 1
            continue
            
        min_c2 = -1
        for c in range(X + 1):
            if max_v2_by_cost[c] >= mid:
                min_c2 = c
                break
        
        if min_c2 == -1:
            low = mid + 1
            continue
            
        min_c3 = -1
        for c in range(X + 1):
            if max_v3_by_cost[c] >= mid:
                min_c3 = c
                break
        
        if min_c3 == -1:
            low = mid + 1
            continue
        
        if min_c1 + min_c2 + min_c3 <= X:
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
            
    print(ans)

solve()