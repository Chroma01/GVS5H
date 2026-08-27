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
    total_sum = 0
    
    for _ in range(N):
        u_val = int(next(iterator))
        d_val = int(next(iterator))
        U.append(u_val)
        D.append(d_val)
        total_sum += (u_val + d_val)

    # The maximum possible H is min(U_i + D_i) because U'_i >= 1 and D'_i >= 1
    # implies U'_i + D'_i >= 2, and U'_i <= U_i, D'_i <= D_i implies U'_i + D'_i <= U_i + D_i.
    # So H <= U_i + D_i for all i.
    min_sum = total_sum
    for i in range(N):
        if U[i] + D[i] < min_sum:
            min_sum = U[i] + D[i]
            
    H_max = min_sum
    H_min = 2
    
    # Function to check if a given H is feasible
    def is_feasible(H):
        # Upper bound for U'_i is min(U_i, H-1)
        # Lower bound for U'_i is 1
        
        # Initialize range for the first tooth
        # L_i, R_i represent the feasible interval [L_i, R_i] for U'_i
        limit = H - 1
        
        # For i=0
        r = min(U[0], limit)
        l = 1
        if l > r:
            return False
            
        for i in range(1, N):
            # From previous step, U'_{i-1} in [l, r]
            # U'_i must be in [l - X, r + X]
            new_l = l - X
            new_r = r + X
            
            # Intersect with absolute bounds [1, min(U_i, H-1)]
            abs_l = 1
            abs_r = min(U[i], limit)
            
            l = max(new_l, abs_l)
            r = min(new_r, abs_r)
            
            if l > r:
                return False
                
        return True

    # Binary search for the maximum feasible H
    # Feasibility is monotonic: if H is feasible, H+1 is also feasible (up to H_max)
    # because the constraint U'_i <= H-1 becomes looser.
    
    low = H_min
    high = H_max
    best_H = H_min
    
    while low <= high:
        mid = (low + high) // 2
        if is_feasible(mid):
            best_H = mid
            low = mid + 1
        else:
            high = mid - 1
            
    # The cost is sum(U_i + D_i) - N * H
    # We want to minimize cost, so we maximize H.
    ans = total_sum - N * best_H
    print(ans)

if __name__ == '__main__':
    solve()