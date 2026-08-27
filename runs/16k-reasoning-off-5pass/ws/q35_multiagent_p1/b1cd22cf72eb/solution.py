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

    # Precompute total sum of original lengths
    total_original_sum = sum(U) + sum(D)

    # Function to check if a given H is feasible
    def is_valid(H):
        # We need to find if there exists a sequence U'_1, ..., U'_N such that:
        # 1. max(0, H - D[i]) <= U'_i <= U[i] for all i
        # 2. |U'_i - U'_{i+1}| <= X for all i
        
        # We maintain the feasible interval [min_val, max_val] for U'_i
        # as we iterate through the teeth.
        
        # Initial feasible interval for U'_1
        # L_1 = max(0, H - D[0])
        # R_1 = U[0]
        
        min_val = max(0, H - D[0])
        max_val = U[0]
        
        if min_val > max_val:
            return False
            
        for i in range(1, N):
            # The previous U'_{i-1} was in [min_val, max_val]
            # So U'_i can be in [min_val - X, max_val + X]
            
            expanded_min = min_val - X
            expanded_max = max_val + X
            
            # Intersect with the current tooth's constraints
            # L_i = max(0, H - D[i])
            # R_i = U[i]
            
            current_L = max(0, H - D[i])
            current_R = U[i]
            
            # Intersection of [expanded_min, expanded_max] and [current_L, current_R]
            new_min = max(expanded_min, current_L)
            new_max = min(expanded_max, current_R)
            
            if new_min > new_max:
                return False
                
            min_val = new_min
            max_val = new_max
            
        return True

    # Binary search for the maximum H
    # Range of H:
    # Lower bound: 0 (since lengths are non-negative, H = U' + D' >= 0)
    # Upper bound: max(U) + max(D) <= 2 * 10^9
    
    low = 0
    high = 2 * 10**9 + 7 # Slightly more than max possible sum
    
    ans_H = 0
    
    while low <= high:
        mid = (low + high) // 2
        if is_valid(mid):
            ans_H = mid
            low = mid + 1
        else:
            high = mid - 1
            
    # The cost is sum(U_i + D_i) - N * H
    # We want to minimize cost, which means maximizing H.
    # We found the maximum valid H.
    
    min_cost = total_original_sum - N * ans_H
    print(min_cost)

solve()