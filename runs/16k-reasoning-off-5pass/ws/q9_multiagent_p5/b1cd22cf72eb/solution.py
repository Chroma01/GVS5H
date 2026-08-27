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
        
        U = []
        D = []
        
        for _ in range(N):
            u_val = int(next(iterator))
            d_val = int(next(iterator))
            U.append(u_val)
            D.append(d_val)
            
    except StopIteration:
        return

    # Function to check if a specific H is valid
    # Returns True if valid, False otherwise.
    # Validity means there exists a sequence U'_i such that:
    # 1. L_i <= U'_i <= R_i for all i
    # 2. |U'_i - U'_{i+1}| <= X for all i
    # where L_i = max(0, H - D_i) and R_i = min(U_i, H)
    def is_valid(H):
        # Calculate bounds for each i
        # We compute R_i = min(U_i, H) and L_i = max(0, H - D_i)
        
        # Forward pass: Compute max possible value for U'_i given left constraints
        # tight_upper[i] = min(R_i, tight_upper[i-1] + X)
        # We use a large number for infinity, but since max possible value is bounded by max(U) + N*X,
        # or simply H, we can use H as the initial "infinity" effectively, or a very large number.
        # However, logically, the first element can be at most R_0.
        
        tight_upper = [0] * N
        
        # We can use a very large number for the initial constraint from the left (conceptually infinity)
        # But practically, tight_upper[0] is just R_0.
        # Let's handle the loop carefully.
        
        current_limit = float('inf')
        
        for i in range(N):
            # Determine R_i
            r_i = U[i]
            if H < r_i:
                r_i = H
            
            # Determine L_i
            l_i = H - D[i]
            if l_i < 0:
                l_i = 0
            
            # Check immediate feasibility
            if l_i > r_i:
                return False
            
            # Update current_max constraint from left
            if current_limit == float('inf'):
                current_limit = r_i
            else:
                current_limit = min(current_limit + X, r_i)
            
            tight_upper[i] = current_limit
        
        # Backward pass: Propagate constraints from right to left
        # tight_upper[i] = min(tight_upper[i], tight_upper[i+1] + X)
        
        for i in range(N - 2, -1, -1):
            tight_upper[i] = min(tight_upper[i], tight_upper[i+1] + X)
            
        # Final check: Does the tightest upper bound satisfy the lower bound?
        for i in range(N):
            l_i = H - D[i]
            if l_i < 0:
                l_i = 0
            if tight_upper[i] < l_i:
                return False
        
        return True

    # The problem asks to minimize cost.
    # Cost for a fixed H is sum(U_i + D_i) - N * H.
    # This cost is strictly decreasing with H.
    # Therefore, to minimize cost, we must maximize H.
    # Constraints on H:
    # 1. H <= U_i + D_i for all i (since U'_i <= U_i, D'_i <= D_i => H <= U_i + D_i)
    #    So H <= min(U_i + D_i).
    # 2. H >= 0 (since lengths are non-negative).
    # 3. H must be such that a valid sequence U'_i exists (checked by is_valid).
    
    # The set of valid H is likely an interval [0, H_max].
    # We can binary search for the largest H in [0, min_sum] that is valid.
    
    min_sum = min(u + d for u, d in zip(U, D))
    
    low = 0
    high = min_sum
    best_H = 0
    
    # Binary search for the maximum valid H
    while low <= high:
        mid = (low + high) // 2
        if is_valid(mid):
            best_H = mid
            low = mid + 1
        else:
            high = mid - 1
            
    # Calculate total cost
    total_initial_sum = sum(u + d for u, d in zip(U, D))
    ans = total_initial_sum - N * best_H
    
    print(ans)

if __name__ == '__main__':
    solve()