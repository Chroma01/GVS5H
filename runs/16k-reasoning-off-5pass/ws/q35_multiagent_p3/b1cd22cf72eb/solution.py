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
        
        U = []
        D = []
        
        for _ in range(N):
            u_val = int(next(iterator))
            d_val = int(next(iterator))
            U.append(u_val)
            D.append(d_val)
    except StopIteration:
        return

    # Precompute sum of U_i + D_i
    total_sum = sum(U[i] + D[i] for i in range(N))
    
    # The cost for a valid H is total_sum - N * H.
    # To minimize cost, we need to maximize H.
    # We binary search for the largest H such that a valid sequence U' exists.
    
    # Constraints on H:
    # 1 <= U'_i <= U_i
    # 1 <= D'_i <= D_i  =>  1 <= H - U'_i <= D_i  =>  H - D_i <= U'_i <= H - 1
    # So, max(1, H - D_i) <= U'_i <= min(U_i, H - 1)
    # Also |U'_i - U'_{i+1}| <= X
    
    # Lower bound for H: 2 (since U'_i >= 1, D'_i >= 1)
    # Upper bound for H: max(U_i + D_i)
    
    low = 2
    high = max(U[i] + D[i] for i in range(N))
    
    ans_H = -1
    
    def is_valid(H):
        # Check if there exists a sequence U'_i such that:
        # L_i <= U'_i <= R_i and |U'_i - U'_{i+1}| <= X
        # where L_i = max(1, H - D_i), R_i = min(U_i, H - 1)
        
        # Maintain the feasible interval [a, b] for U'_i
        # Initially for i=0, the interval is [L_0, R_0]
        
        # Compute L_0 and R_0
        L0 = 1 if H - D[0] < 1 else H - D[0]
        R0 = U[0] if H - 1 > U[0] else H - 1
        
        if L0 > R0:
            return False
            
        a = L0
        b = R0
        
        for i in range(1, N):
            # The new constraints for U'_i are [L_i, R_i]
            Li = 1 if H - D[i] < 1 else H - D[i]
            Ri = U[i] if H - 1 > U[i] else H - 1
            
            # The previous interval [a, b] for U'_{i-1} implies that U'_i must be in [a - X, b + X]
            # So the new feasible interval is intersection of [Li, Ri] and [a - X, b + X]
            
            new_a = Li if Li > a - X else a - X
            new_b = Ri if Ri < b + X else b + X
            
            if new_a > new_b:
                return False
            
            a = new_a
            b = new_b
            
        return True

    # Binary search for the largest valid H
    while low <= high:
        mid = (low + high) // 2
        if is_valid(mid):
            ans_H = mid
            low = mid + 1
        else:
            high = mid - 1
            
    if ans_H == -1:
        # This should not happen given the problem constraints, as H=2 is always valid
        print(0)
    else:
        cost = total_sum - N * ans_H
        print(cost)

solve()