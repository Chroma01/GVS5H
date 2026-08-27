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

    # Precompute sum of all original lengths
    total_original_sum = sum(U) + sum(D)
    
    # Binary search for the maximum valid H
    # H must be such that there exists U'_i with:
    # 0 <= U'_i <= U_i
    # 0 <= D'_i <= D_i  =>  0 <= H - U'_i <= D_i  =>  H - D_i <= U'_i <= H
    # So U'_i in [max(0, H - D_i), min(U_i, H)]
    # And |U'_i - U'_{i+1}| <= X
    
    # Lower bound for H: 0
    # Upper bound for H: max(U_i) + max(D_i) is a safe upper bound.
    # Actually, since U'_i <= U_i and D'_i <= D_i, H = U'_i + D'_i <= U_i + D_i.
    # So H <= min(U_i + D_i) is not required, but H <= max(U_i + D_i) is a loose bound.
    # A tighter upper bound is max(U) + max(D).
    
    low = 0
    high = max(U) + max(D)
    ans_H = 0
    
    # Function to check if a given H is valid
    def is_valid(H):
        # Propagate feasible intervals for U'_i
        # Let [a_i, b_i] be the feasible range for U'_i
        # a_1 = max(0, H - D[0]), b_1 = min(U[0], H)
        
        # Initialize for the first tooth
        L = max(0, H - D[0])
        R = min(U[0], H)
        
        if L > R:
            return False
            
        a = L
        b = R
        
        for i in range(1, N):
            # The new bounds from the sum constraint
            new_L = max(0, H - D[i])
            new_R = min(U[i], H)
            
            if new_L > new_R:
                return False
            
            # Propagate from previous interval [a, b]
            # U'_i can be in [a - X, b + X] due to difference constraint
            # Intersect with [new_L, new_R]
            
            a = max(new_L, a - X)
            b = min(new_R, b + X)
            
            if a > b:
                return False
                
        return True

    # Binary search for the largest H that is valid
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