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

    # Binary search for the maximum possible minimum vitamin intake
    # Range for K is [0, X] because each food has at least 1 calorie and 1 unit of vitamin.
    # If X=0, answer is 0, but constraints say X>=1, C_i>=1.
    
    low = 0
    high = X  # Upper bound: even if we spend all X calories on 1-unit vitamins, max min is X
    ans = 0

    # Pre-separate foods by vitamin type for potentially cleaner logic, 
    # though iterating all foods in DP is fine.
    # We will implement the feasibility check inside the binary search.

    def is_feasible(K):
        if K == 0:
            return True
        
        # dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2
        # We cap i and j at K because having more than K doesn't help satisfy the condition ">= K"
        # and saves space/time.
        # Dimensions: (K+1) x (K+1)
        # Initialize with infinity
        INF = float('inf')
        dp = [[INF] * (K + 1) for _ in range(K + 1)]
        dp[0][0] = 0

        for v, a, c in foods:
            # We need to update dp table. Since each food can be used at most once,
            # we iterate backwards to avoid using the same food multiple times for the same state transition.
            # However, since we have 2 dimensions, we need to be careful with iteration order.
            # Standard knapsack: iterate backwards on the capacity/dimension being updated.
            # Here, both i and j can increase. So we iterate both backwards.
            
            # Create a copy or iterate in reverse to prevent using updated values from the current food
            # in the same step. Since we update dp[min(i+a, K)][min(j, K)] from dp[i][j],
            # if we iterate i from K down to 0 and j from K down to 0, we are safe.
            
            # Optimization: Only iterate over reachable states? 
            # Given N, X <= 5000 and K <= 5000, K^2 can be 25e6. N * K^2 = 125e9 is too slow.
            # We need a more efficient DP or a different approach.
            
            # Wait, the constraints are N, X <= 5000.
            # The standard 2D DP for 2 vitamins is O(N * K^2). If K is large, this is TLE.
            # However, note that the total calories X is also <= 5000.
            # We can use calories as one dimension of the DP!
            
            # Let's redefine DP:
            # dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2.
            # This is what we had. The issue is K can be up to 5000.
            # But notice that if K > X, it's impossible (since each unit of vitamin requires at least 1 calorie).
            # So K is effectively bounded by X.
            # Still, K^2 * N is too big.
            
            # Alternative DP:
            # dp[c] = a 2D array? No.
            # dp[i][j] = min calories.
            # Since X <= 5000, we can limit the calorie dimension.
            # But we are minimizing calories, so the value in dp[i][j] is the calorie cost.
            # The state space is K x K.
            
            # Is there a better way?
            # Let's use dp[i][j] = maximum Vitamin 3 obtainable with exactly i calories and at least j units of Vitamin 1?
            # No, we need Vitamin 2.
            
            # Let's use dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2.
            # This is correct.
            # To optimize, note that we only care about states where dp[i][j] <= X.
            # Also, we can cap i and j at K.
            
            # Let's try to optimize the inner loop.
            # Instead of iterating all i, j, we can track the range of reachable i, j.
            # But worst case is still large.
            
            # Let's reconsider the problem constraints and typical solutions for this specific problem (AtCoder ABC 214 D is 2 vitamins, this is 3).
            # For 3 vitamins, a common solution is binary search + 2D DP where dp[i][j] is min calories for vit1>=i, vit2>=j.
            # The complexity is O(N * K^2). With N=5000, K=5000, this is 125e9, which is too slow.
            
            # However, note that K is the answer we are binary searching for.
            # In the feasibility check for a specific K, we only need to check if dp[K][K] <= X.
            # But we need to compute the whole table.
            
            # Is there a constraint I missed?
            # N, X <= 5000.
            # Maybe K is small? No, K can be up to 5000.
            
            # Let's look at the structure again.
            # We have 3 vitamins.
            # dp[i][j] = min calories for vit1>=i, vit2>=j.
            # When we process a food with vitamin 3, it doesn't change i or j, but it adds to vitamin 3.
            # So we need to track vitamin 3 as well?
            # If we track vitamin 3, we need dp[i][j][k].
            
            # Correct approach for 3 vitamins with small X:
            # dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2.
            # This doesn't track Vitamin 3.
            
            # Let's use dp[i][j] = maximum Vitamin 3 obtainable with exactly i calories and at least j units of Vitamin 1?
            # No, we need Vitamin 2.
            
            # Let's use dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2.
            # And we store the maximum Vitamin 3 for that state? No, that's not a single value.
            
            # Actually, we can use dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2.
            # And we assume that we have collected some amount of Vitamin 3.
            # But we need to ensure Vitamin 3 >= K.
            
            # The standard solution for this problem is:
            # Binary search K.
            # dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2.
            # Initialize dp[0][0] = 0, others INF.
            # For each food:
            #   If vit 1: update dp[min(i+a, K)][j]
            #   If vit 2: update dp[i][min(j+a, K)]
            #   If vit 3: this food contributes to Vitamin 3.
            #       We need to track Vitamin 3.
            #       So we need a 3D DP: dp[i][j][k] = min calories.
            #       This is O(N * K^3), which is too slow.
            
            # Alternative:
            # dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2.
            # And we separately track the maximum Vitamin 3 we can get with the same subset?
            # No, the subset is determined by the choices.
            
            # Let's use dp[i][j] = maximum Vitamin 3 obtainable with exactly i calories and at least j units of Vitamin 1?
            # No.
            
            # Let's use dp[i][j] = minimum calories to get at least i units of Vitamin 1 and at least j units of Vitamin 2.
            # And we add a third dimension for Vitamin 3, but we cap it at K.
            # dp[i][j][k] = min calories.
            # To save space, we can use a dictionary or sparse array.
            # But worst case is still large.
            
            # Given the time, I will implement the 2D DP for 2 vitamins and assume the third vitamin is handled by a separate check?
            # No.
            
            # Let's try the 3D DP with optimization:
            # Only store states that are reachable.
            # Use a dictionary: dp[(i, j, k)] = min calories.
            # This might be sparse.
            
            dp = {}
            dp[(0, 0, 0)] = 0
            
            for v, a, c in foods:
                # We need to update dp. Iterate over a copy of keys.
                # To avoid using the same food multiple times, we collect updates and apply them.
                updates = []
                for (i, j, k), cost in dp.items():
                    if cost + c > X:
                        continue
                    
                    ni, nj, nk = i, j, k
                    
                    if v == 1:
                        ni = min(i + a, K)
                    elif v == 2:
                        nj = min(j + a, K)
                    elif v == 3:
                        nk = min(k + a, K)
                    
                    new_cost = cost + c
                    state = (ni, nj, nk)
                    if state not in dp or dp[state] > new_cost:
                        updates.append((state, new_cost))
                
                for state, cost in updates:
                    if state not in dp or dp[state] > cost:
                        dp[state] = cost

            return dp.get((K, K, K), INF) <= X

    # Binary search
    while low <= high:
        mid = (low + high) // 2
        if is_feasible(mid):
            ans = mid
            low = mid + 1
        else:
            high = mid - 1

    print(ans)

solve()