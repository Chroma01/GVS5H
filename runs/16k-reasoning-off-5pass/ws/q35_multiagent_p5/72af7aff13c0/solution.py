import sys

# Increase recursion depth just in case, though we use iterative DP
sys.setrecursionlimit(300000)

def solve():
    # Read all input at once
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Grid A is 1-indexed conceptually, but we'll use 0-indexed internally
    # A[h][w] corresponds to row h, col w (0 <= h < H, 0 <= w < W)
    A = []
    for r in range(H):
        row = []
        for c in range(W):
            row.append(int(next(iterator)))
        A.append(row)

    try:
        Q = int(next(iterator))
        sh = int(next(iterator)) - 1
        sw = int(next(iterator)) - 1
    except StopIteration:
        Q = 0
        sh = 0
        sw = 0

    queries = []
    for _ in range(Q):
        d = next(iterator)
        a_val = int(next(iterator))
        queries.append((d, a_val))

    MOD = 998244353

    # Precompute L and R tables
    # L[h][w] = sum of products of paths from (0,0) to (h,w)
    # R[h][w] = sum of products of paths from (h,w) to (H-1, W-1)
    
    L = [[0] * W for _ in range(H)]
    R = [[0] * W for _ in range(H)]

    # Compute L
    # L[0][0] = A[0][0]
    # L[h][w] = A[h][w] * (L[h-1][w] + L[h][w-1])
    
    # Initialize L[0][0]
    L[0][0] = A[0][0] % MOD
    
    for w in range(1, W):
        L[0][w] = (L[0][w-1] * A[0][w]) % MOD
        
    for h in range(1, H):
        L[h][0] = (L[h-1][0] * A[h][0]) % MOD
        for w in range(1, W):
            val = (L[h-1][w] + L[h][w-1]) % MOD
            L[h][w] = (val * A[h][w]) % MOD

    # Compute R
    # R[H-1][W-1] = A[H-1][W-1]
    # R[h][w] = A[h][w] * (R[h+1][w] + R[h][w+1])
    
    R[H-1][W-1] = A[H-1][W-1] % MOD
    
    for w in range(W-2, -1, -1):
        R[H-1][w] = (R[H-1][w+1] * A[H-1][w]) % MOD
        
    for h in range(H-2, -1, -1):
        R[h][W-1] = (R[h+1][W-1] * A[h][W-1]) % MOD
        for w in range(W-2, -1, -1):
            val = (R[h+1][w] + R[h][w+1]) % MOD
            R[h][w] = (val * A[h][w]) % MOD

    # Initial total sum
    total_sum = L[H-1][W-1]

    # Current position of Takahashi
    cur_h, cur_w = sh, sw

    # Modular inverse function
    def mod_inv(n):
        return pow(n, MOD - 2, MOD)

    results = []

    for d, a_val in queries:
        # Move Takahashi
        if d == 'L':
            cur_w -= 1
        elif d == 'R':
            cur_w += 1
        elif d == 'U':
            cur_h -= 1
        elif d == 'D':
            cur_h += 1
        
        # Update grid value
        old_val = A[cur_h][cur_w]
        A[cur_h][cur_w] = a_val
        
        # Calculate contribution of the cell (cur_h, cur_w) to the total sum
        # Contribution = L[cur_h][cur_w] * R[cur_h][cur_w] / A[cur_h][cur_w]
        # If A[cur_h][cur_w] is 0, contribution is 0.
        
        # We need to compute L' and R' for the new value at (cur_h, cur_w)
        # L'[cur_h][cur_w] = A'[cur_h][cur_w] * (L[cur_h-1][cur_w] + L[cur_h][cur_w-1])
        # Note: L[cur_h-1][cur_w] and L[cur_h][cur_w-1] are NOT affected by the change at (cur_h, cur_w)
        # because they depend on cells strictly above or to the left.
        
        l_prev = 0
        if cur_h > 0:
            l_prev = L[cur_h-1][cur_w]
        if cur_w > 0:
            l_prev = (l_prev + L[cur_h][cur_w-1]) % MOD
        
        l_new = (a_val * l_prev) % MOD
        
        # Similarly for R
        # R'[cur_h][cur_w] = A'[cur_h][cur_w] * (R[cur_h+1][cur_w] + R[cur_h][cur_w+1])
        r_next = 0
        if cur_h < H - 1:
            r_next = R[cur_h+1][cur_w]
        if cur_w < W - 1:
            r_next = (r_next + R[cur_h][cur_w+1]) % MOD
            
        r_new = (a_val * r_next) % MOD
        
        # Old contribution
        if old_val == 0:
            old_contrib = 0
        else:
            # L[cur_h][cur_w] and R[cur_h][cur_w] currently hold values based on old_val
            # But wait, we haven't updated L and R tables yet.
            # So L[cur_h][cur_w] is the OLD L value.
            # R[cur_h][cur_w] is the OLD R value.
            old_l = L[cur_h][cur_w]
            old_r = R[cur_h][cur_w]
            old_contrib = (old_l * old_r) % MOD * mod_inv(old_val) % MOD
            
        # New contribution
        if a_val == 0:
            new_contrib = 0
        else:
            new_contrib = (l_new * r_new) % MOD * mod_inv(a_val) % MOD
            
        # Update total sum
        total_sum = (total_sum - old_contrib + new_contrib) % MOD
        
        # Now we must update the L and R tables for future queries.
        # Updating L:
        # L[cur_h][cur_w] changes. This affects L[cur_h][cur_w+1...W-1] and L[cur_h+1...H-1][cur_w...W-1].
        # We update row by row starting from cur_h.
        
        # Update L[cur_h][cur_w]
        L[cur_h][cur_w] = l_new
        
        # Update rest of row cur_h
        for w in range(cur_w + 1, W):
            val = (L[cur_h][w-1] + (L[cur_h-1][w] if cur_h > 0 else 0)) % MOD
            L[cur_h][w] = (val * A[cur_h][w]) % MOD
            
        # Update subsequent rows
        for h in range(cur_h + 1, H):
            # Update first column of this row if it's in the affected region (w >= cur_w)
            # Actually, L[h][cur_w] depends on L[h-1][cur_w] and L[h][cur_w-1].
            # L[h][cur_w-1] is unchanged if cur_w-1 < cur_w? No, L[h][cur_w-1] is to the left.
            # If cur_w > 0, L[h][cur_w-1] is unchanged.
            # If cur_w == 0, L[h][cur_w-1] is 0.
            
            # We need to update L[h][w] for w from cur_w to W-1.
            # L[h][cur_w] = A[h][cur_w] * (L[h-1][cur_w] + L[h][cur_w-1])
            
            # Compute L[h][cur_w]
            left_val = L[h][cur_w-1] if cur_w > 0 else 0
            up_val = L[h-1][cur_w]
            val = (up_val + left_val) % MOD
            L[h][cur_w] = (val * A[h][cur_w]) % MOD
            
            # Compute rest of row
            for w in range(cur_w + 1, W):
                val = (L[h][w-1] + L[h-1][w]) % MOD
                L[h][w] = (val * A[h][w]) % MOD

        # Update R:
        # R[cur_h][cur_w] changes. This affects R[cur_h][cur_w-1...0] and R[cur_h-1...0][cur_w...0].
        # We update row by row starting from cur_h upwards.
        
        R[cur_h][cur_w] = r_new
        
        # Update rest of row cur_h to the left
        for w in range(cur_w - 1, -1, -1):
            val = (R[cur_h][w+1] + (R[cur_h+1][w] if cur_h < H - 1 else 0)) % MOD
            R[cur_h][w] = (val * A[cur_h][w]) % MOD
            
        # Update preceding rows
        for h in range(cur_h - 1, -1, -1):
            # Update R[h][cur_w]
            right_val = R[h][cur_w+1] if cur_w < W - 1 else 0
            down_val = R[h+1][cur_w]
            val = (down_val + right_val) % MOD
            R[h][cur_w] = (val * A[h][cur_w]) % MOD
            
            # Update rest of row to the left
            for w in range(cur_w - 1, -1, -1):
                val = (R[h][w+1] + R[h+1][w]) % MOD
                R[h][w] = (val * A[h][w]) % MOD

        results.append(str(total_sum))

    print('\n'.join(results))

solve()