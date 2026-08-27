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

    U = []
    D = []
    
    for _ in range(N):
        u_val = int(next(iterator))
        d_val = int(next(iterator))
        U.append(u_val)
        D.append(d_val)

    # Determine the range of possible H
    # H must satisfy:
    # 1. U'_i >= 1 => H - D'_i >= 1 => H >= D'_i + 1. Since D'_i <= D_i, we need H >= D_i + 1 is not strictly required,
    #    but we need H - D_i <= U'_i <= U_i. So H - D_i <= U_i => H <= U_i + D_i.
    #    Also H - D_i >= 1 is not required, but U'_i >= 1 => H - D'_i >= 1. Since D'_i <= D_i, H - D_i <= H - D'_i.
    #    The constraint is U'_i >= 1 and D'_i >= 1.
    #    U'_i + D'_i = H.
    #    U'_i <= U_i, D'_i <= D_i.
    #    So 1 <= U'_i <= U_i and 1 <= H - U'_i <= D_i.
    #    From 1 <= H - U'_i => U'_i <= H - 1.
    #    From H - U'_i <= D_i => U'_i >= H - D_i.
    #    So for each i, U'_i must be in [max(1, H - D_i), min(U_i, H - 1)].
    #    For this interval to be non-empty, we need max(1, H - D_i) <= min(U_i, H - 1).
    #    This implies:
    #      1 <= U_i (always true)
    #      1 <= H - 1 => H >= 2
    #      H - D_i <= U_i => H <= U_i + D_i
    #      H - D_i <= H - 1 => -D_i <= -1 => D_i >= 1 (always true)
    #    So for all i, we need H <= U_i + D_i. Thus H_max = min(U_i + D_i).
    #    Also H >= 2. But more tightly, we need H - D_i <= U_i for all i, so H <= min(U_i + D_i).
    #    And we need H - D_i >= 1 is not required, but U'_i >= 1.
    #    The lower bound for H comes from the fact that U'_i >= 1.
    #    Is there a lower bound on H?
    #    If H is very small, say H=2, then U'_i + D'_i = 2. Since U'_i >= 1, D'_i >= 1, we must have U'_i=1, D'_i=1.
    #    This requires U_i >= 1 and D_i >= 1, which is true.
    #    However, we also need to satisfy the smoothness constraint.
    #    Let's just set H_min = 2 and H_max = min(U_i + D_i).
    #    Wait, if H < max(D_i) + 1, then for some i, H - D_i <= 0, so L_i = 1.
    #    If H > min(U_i + D_i), then for some i, H - D_i > U_i, so L_i > R_i, invalid.
    #    So H must be in [2, min(U_i + D_i)].
    
    H_max = min(U[i] + D[i] for i in range(N))
    H_min = 2
    
    if H_min > H_max:
        # This should not happen given constraints U_i, D_i >= 1
        print(0)
        return

    # Function to calculate minimum sum of U' for a fixed H
    def get_min_sum_U_prime(H):
        # Determine initial bounds [L_i, R_i] for each U'_i
        L = [0] * N
        R = [0] * N
        for i in range(N):
            l_i = H - D[i]
            if l_i < 1:
                l_i = 1
            r_i = U[i]
            if r_i > H - 1:
                r_i = H - 1
            
            if l_i > r_i:
                return float('inf')
            
            L[i] = l_i
            R[i] = r_i
        
        # Propagate constraints forward
        # low[i] represents the minimum possible value for U'_i
        # high[i] represents the maximum possible value for U'_i
        low = list(L)
        high = list(R)
        
        for i in range(1, N):
            # U'_i >= U'_{i-1} - X => low[i] = max(low[i], low[i-1] - X)
            # U'_i <= U'_{i-1} + X => high[i] = min(high[i], high[i-1] + X)
            low[i] = max(low[i], low[i-1] - X)
            high[i] = min(high[i], high[i-1] + X)
            if low[i] > high[i]:
                return float('inf')
        
        # Propagate constraints backward
        for i in range(N - 2, -1, -1):
            # U'_i >= U'_{i+1} - X => low[i] = max(low[i], low[i+1] - X)
            # U'_i <= U'_{i+1} + X => high[i] = min(high[i], high[i+1] + X)
            low[i] = max(low[i], low[i+1] - X)
            high[i] = min(high[i], high[i+1] + X)
            if low[i] > high[i]:
                return float('inf')
        
        # The minimum sum is achieved by taking the smallest possible value for each U'_i
        # which is low[i] after propagation.
        return sum(low)

    # The cost function for a fixed H is:
    # Cost(H) = sum(U_i + D_i) - N * H + min_sum_U_prime(H)
    # This function is convex. We can use ternary search.
    
    total_UD = sum(U[i] + D[i] for i in range(N))
    
    def cost(H):
        min_sum = get_min_sum_U_prime(H)
        if min_sum == float('inf'):
            return float('inf')
        return total_UD - N * H + min_sum

    # Ternary search for the minimum cost in [H_min, H_max]
    left = H_min
    right = H_max
    
    while right - left > 2:
        mid1 = left + (right - left) // 3
        mid2 = right - (right - left) // 3
        
        c1 = cost(mid1)
        c2 = cost(mid2)
        
        if c1 < c2:
            right = mid2
        else:
            left = mid1
            
    # Check the remaining points
    ans = float('inf')
    for H in range(left, right + 1):
        c = cost(H)
        if c < ans:
            ans = c
            
    print(ans)

solve()