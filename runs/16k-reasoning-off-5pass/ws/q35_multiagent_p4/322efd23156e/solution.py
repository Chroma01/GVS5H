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

    vit1_foods = []
    vit2_foods = []
    vit3_foods = []

    for _ in range(N):
        v = int(next(iterator))
        a = int(next(iterator))
        c = int(next(iterator))
        if v == 1:
            vit1_foods.append((a, c))
        elif v == 2:
            vit2_foods.append((a, c))
        else:
            vit3_foods.append((a, c))

    # Binary search for the maximum K
    # K can range from 0 to 5000 (since X <= 5000 and min C_i >= 1)
    low = 0
    high = 5000
    ans = 0

    def check(K):
        if K == 0:
            return True
        
        INF = float('inf')
        # dp[i][j] = min calories to get at least i Vit1, at least j Vit2
        # Dimensions: (K+1) x (K+1)
        dp = [[INF] * (K + 1) for _ in range(K + 1)]
        dp[0][0] = 0
        
        # Process Vit1 items
        # For each Vit1 item, update dp[new_i][j] = min(dp[new_i][j], dp[i][j] + c)
        # where new_i = min(i + a, K)
        # Iterate backwards to avoid using the same item multiple times
        for a, c in vit1_foods:
            for i in range(K, -1, -1):
                for j in range(K + 1):
                    if dp[i][j] == INF:
                        continue
                    new_i = i + a
                    if new_i > K:
                        new_i = K
                    new_cost = dp[i][j] + c
                    if new_cost < dp[new_i][j]:
                        dp[new_i][j] = new_cost

        # Process Vit2 items
        # For each Vit2 item, update dp[i][new_j] = min(dp[i][new_j], dp[i][j] + c)
        # where new_j = min(j + a, K)
        # Iterate backwards
        for a, c in vit2_foods:
            for j in range(K, -1, -1):
                for i in range(K + 1):
                    if dp[i][j] == INF:
                        continue
                    new_j = j + a
                    if new_j > K:
                        new_j = K
                    new_cost = dp[i][j] + c
                    if new_cost < dp[i][new_j]:
                        dp[i][new_j] = new_cost

        # Step 2: Compute min_cal_v3[k] = min calories to get at least k units of Vit3
        # This is a 1D knapsack
        min_cal_v3 = [INF] * (K + 1)
        min_cal_v3[0] = 0
        
        for a, c in vit3_foods:
            # Update min_cal_v3: for k from K down to 0
            for k in range(K, -1, -1):
                if min_cal_v3[k] == INF:
                    continue
                new_k = k + a
                if new_k > K:
                    new_k = K
                new_cost = min_cal_v3[k] + c
                if new_cost < min_cal_v3[new_k]:
                    min_cal_v3[new_k] = new_cost

        # Step 3: Check if there exists i>=K, j>=K such that dp[i][j] + min_cal_v3[K] <= X
        # Since we capped indices at K, dp[K][K] represents the min calories to get
        # at least K Vit1 and at least K Vit2.
        # We need at least K Vit3 as well, which costs min_cal_v3[K].
        
        if dp[K][K] == INF or min_cal_v3[K] == INF:
            return False
        
        return dp[K][K] + min_cal_v3[K] <= X

    # Binary search
    while low <= high:
        mid = (low + high) // 2
        if check(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1
            
    print(ans)

solve()