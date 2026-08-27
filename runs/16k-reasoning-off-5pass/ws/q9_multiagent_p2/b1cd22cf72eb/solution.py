import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(200005)

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
    min_sum = float('inf')
    total_sum = 0

    for _ in range(N):
        u = int(next(iterator))
        d = int(next(iterator))
        U.append(u)
        D.append(d)
        s = u + d
        total_sum += s
        if s < min_sum:
            min_sum = s

    # Binary search for the maximum feasible H
    # Range of H is [0, min_sum]
    # If H > min_sum, then for some i, H - U_i > D_i, which implies D'_i > D_i, impossible.
    # Also H must be such that we can find D'_i satisfying constraints.
    
    low = 0
    high = min_sum
    ans_H = 0

    while low <= high:
        mid = (low + high) // 2
        H = mid
        
        # Check if H is feasible
        # Constraints for D'_i:
        # 1. 0 <= D'_i <= D_i
        # 2. H - U_i <= D'_i  (derived from U'_i <= U_i and U'_i + D'_i = H)
        # 3. |D'_{i+1} - D'_i| <= X
        
        # Initialize bounds
        # lower_bound[i] = max(0, H - U_i)
        # upper_bound[i] = D_i
        
        possible = True
        
        # Forward pass
        # We maintain the tightest possible [min_val, max_val] for D'_i
        # min_d[i] represents the minimum possible value for D'_i considering constraints from 0 to i
        # max_d[i] represents the maximum possible value for D'_i considering constraints from 0 to i
        
        min_d = [0] * N
        max_d = [0] * N
        
        for i in range(N):
            # Base constraints
            val = H - U[i]
            if val < 0:
                val = 0
            min_d[i] = val
            max_d[i] = D[i]
            
        # Propagate constraints from left to right
        for i in range(1, N):
            # Constraint from left neighbor: D'_i >= D'_{i-1} - X
            if min_d[i-1] - X > min_d[i]:
                min_d[i] = min_d[i-1] - X
            
            # Constraint from left neighbor: D'_i <= D'_{i-1} + X
            if max_d[i-1] + X < max_d[i]:
                max_d[i] = max_d[i-1] + X
            
            if min_d[i] > max_d[i]:
                possible = False
                break
        
        if not possible:
            high = mid - 1
            continue
            
        # Backward propagation
        # Propagate constraints from right to left to ensure consistency with right neighbors
        for i in range(N - 2, -1, -1):
            # Constraint from right neighbor: D'_i >= D'_{i+1} - X
            if min_d[i+1] - X > min_d[i]:
                min_d[i] = min_d[i+1] - X
            
            # Constraint from right neighbor: D'_i <= D'_{i+1} + X
            if max_d[i+1] + X < max_d[i]:
                max_d[i] = max_d[i+1] + X
            
            if min_d[i] > max_d[i]:
                possible = False
                break
        
        if possible:
            ans_H = H
            low = mid + 1
        else:
            high = mid - 1

    # Calculate minimum cost
    # Cost = sum(U_i + D_i) - N * H_max
    result = total_sum - N * ans_H
    print(result)

if __name__ == '__main__':
    solve()