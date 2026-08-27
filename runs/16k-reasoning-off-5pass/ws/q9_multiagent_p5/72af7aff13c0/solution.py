import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read Grid A
    # We store A as a list of lists.
    A = []
    for r in range(H):
        row = []
        for c in range(W):
            row.append(int(next(iterator)))
        A.append(row)
        
    # Read Q
    Q = int(next(iterator))
    
    # Read initial sh, sw
    # Input is 1-indexed. Convert to 0-indexed.
    sh = int(next(iterator)) - 1
    sw = int(next(iterator)) - 1
    
    MOD = 998244353
    
    # Precompute DP table
    # dp[r][c] = sum of path products from (0,0) to (r,c)
    # We use a 1D array for better cache locality and to simplify indexing
    # Index (r, c) -> r*W + c
    
    dp_flat = [0] * (H * W)
    
    # Base case
    dp_flat[0] = A[0][0] % MOD
    
    # Fill first row
    curr = A[0][0]
    for c in range(1, W):
        curr = (curr * A[0][c]) % MOD
        dp_flat[c] = curr
        
    # Fill first column
    curr = dp_flat[0]
    for r in range(1, H):
        curr = (curr * A[r][0]) % MOD
        dp_flat[r*W] = curr
        
    # Fill rest
    for r in range(1, H):
        for c in range(1, W):
            idx = r*W + c
            prev_up = dp_flat[(r-1)*W + c]
            prev_left = dp_flat[r*W + c-1]
            dp_flat[idx] = ((prev_up + prev_left) % MOD * A[r][c]) % MOD
            
    output = []
    
    for _ in range(Q):
        d = next(iterator)
        a_val = int(next(iterator))
        
        # Determine new position (h, w)
        # Current position is (sh, sw).
        # Move one cell in direction d.
        if d == 'L':
            sw -= 1
        elif d == 'R':
            sw += 1
        elif d == 'U':
            sh -= 1
        elif d == 'D':
            sh += 1
            
        # Update A[sh][sw]
        A[sh][sw] = a_val
        
        # If the updated cell is the destination (H-1, W-1), we just update A and print.
        # However, the DP value at (H-1, W-1) is already stored in dp_flat.
        # We need to update it.
        if sh == H - 1 and sw == W - 1:
            # Recalculate dp_flat[(H-1)*W + (W-1)] based on neighbors
            idx = (H-1)*W + (W-1)
            up_val = dp_flat[(H-2)*W + (W-1)] if H > 1 else 0
            left_val = dp_flat[(H-1)*W + (W-2)] if W > 1 else 0
            dp_flat[idx] = ((up_val + left_val) % MOD * a_val) % MOD
            output.append(str(dp_flat[idx]))
            continue
            
        # Update DP table starting from (sh, sw)
        # The change propagates to the suffix rectangle [sh, H-1] x [sw, W-1].
        
        # Helper to get value safely
        def get_dp(r, c):
            if r < 0 or c < 0: return 0
            return dp_flat[r*W + c]

        # Update (sh, sw)
        idx = sh*W + sw
        up_val = get_dp(sh-1, sw)
        left_val = get_dp(sh, sw-1)
        new_val = ((up_val + left_val) % MOD * a_val) % MOD
        dp_flat[idx] = new_val
        
        # Propagate row by row
        # Row sh
        for c in range(sw + 1, W):
            idx = sh*W + c
            up_val = get_dp(sh-1, c)
            left_val = dp_flat[idx - 1] # dp[sh][c-1] is already updated
            new_val = ((up_val + left_val) % MOD * A[sh][c]) % MOD
            dp_flat[idx] = new_val
            
        # Rows sh+1 to H-1
        for r in range(sh + 1, H):
            # Column sw
            idx = r*W + sw
            up_val = dp_flat[(r-1)*W + sw] # dp[r-1][sw] is updated
            left_val = get_dp(r, sw-1) # dp[r][sw-1] is unchanged
            new_val = ((up_val + left_val) % MOD * A[r][sw]) % MOD
            dp_flat[idx] = new_val
            
            # Columns sw+1 to W-1
            for c in range(sw + 1, W):
                idx = r*W + c
                up_val = dp_flat[(r-1)*W + c] # dp[r-1][c] is updated
                left_val = dp_flat[idx - 1] # dp[r][c-1] is updated
                new_val = ((up_val + left_val) % MOD * A[r][c]) % MOD
                dp_flat[idx] = new_val
                
        output.append(str(dp_flat[(H-1)*W + (W-1)]))
        
    print('\n'.join(output))

if __name__ == '__main__':
    solve()