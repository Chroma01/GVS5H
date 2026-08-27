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
        total_sum += u_val + d_val

    # We want to maximize H such that there exists a valid sequence U'_i
    # satisfying:
    # 1 <= U'_i <= min(U_i, H-1)
    # |U'_i - U'_{i+1}| <= X
    
    # Feasibility check for a given H
    def is_feasible(H):
        # Lower bound for U'_1 is 1, upper bound is min(U[0], H-1)
        low = 1
        high = U[0]
        if H - 1 < high:
            high = H - 1
        
        if low > high:
            return False
            
        for i in range(1, N):
            # The feasible range for U'_i based on previous step
            # U'_{i-1} was in [low, high]
            # So U'_i must be in [low - X, high + X]
            new_low = low - X
            new_high = high + X
            
            # Also constrained by 1 <= U'_i <= min(U[i], H-1)
            current_max = U[i]
            if H - 1 < current_max:
                current_max = H - 1
            
            # Intersect [new_low, new_high] with [1, current_max]
            low = max(1, new_low)
            high = min(current_max, new_high)
            
            if low > high:
                return False
                
        return True

    # Binary search for the maximum feasible H
    # H must be at least 2 (since min tooth length is 1, so U'+D'=H >= 2)
    # H can be at most 2 * 10^9 + 1 (since max U_i, D_i is 10^9, so max sum is 2*10^9, 
    # but we need U' >= 1 and D' >= 1, so H <= U_max + D_max is not strictly true, 
    # but H <= 2*10^9 is a safe upper bound since U' <= 10^9 and D' <= 10^9)
    
    low_H = 2
    high_H = 2 * 10**9 + 1
    ans_H = 1 # Should be at least 2 if feasible, but init to 1
    
    while low_H <= high_H:
        mid = (low_H + high_H) // 2
        if is_feasible(mid):
            ans_H = mid
            low_H = mid + 1
        else:
            high_H = mid - 1
            
    # Calculate the minimum cost
    # Cost = sum(U_i + D_i) - N * H
    # Since we maximized H, this minimizes the cost.
    min_cost = total_sum - N * ans_H
    
    print(min_cost)

if __name__ == '__main__':
    solve()