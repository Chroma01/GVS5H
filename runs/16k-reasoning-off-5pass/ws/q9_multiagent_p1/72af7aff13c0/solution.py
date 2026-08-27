import sys

# Increase recursion depth just in case, though not strictly needed for this iterative solution
sys.setrecursionlimit(300000)

def solve():
    # Read all input from stdin efficiently
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        H = int(next(iterator))
        W = int(next(iterator))
    except StopIteration:
        return

    # Read the grid A
    # We will store A as a flat list for efficiency, but access via (r, c) -> r*W + c
    # Constraints: HW <= 200,000
    A = [0] * (H * W)
    for r in range(H):
        for c in range(W):
            A[r * W + c] = int(next(iterator))

    Q = int(next(iterator))
    sh = int(next(iterator)) - 1 # 0-indexed row
    sw = int(next(iterator)) - 1 # 0-indexed column
    
    MOD = 998244353

    # Precompute factorials and inverse factorials for combinations
    # Max value for n in nCr is (H-1) + (W-1) = H + W - 2
    # So we need up to H + W
    max_n = H + W + 5
    fact = [1] * max_n
    inv = [1] * max_n
    
    for i in range(1, max_n):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[max_n-1] = pow(fact[max_n-1], MOD - 2, MOD)
    for i in range(max_n-2, -1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    # Precompute coefficients K[h][w]
    # The problem asks for the sum of products of values along all paths from (1,1) to (H,W).
    # Let this sum be S.
    # S = Sum over all paths P of (Product of A_{h,w} for (h,w) in P).
    # By linearity of expectation (or algebraic expansion), this sum can be rewritten as:
    # S = Sum over all cells (r,c) of (A_{r,c} * (Number of paths passing through (r,c))).
    # The number of paths passing through (r,c) is:
    #   (Paths from (0,0) to (r,c)) * (Paths from (r,c) to (H-1, W-1))
    # Note: Coordinates are 0-indexed here.
    # Paths from (0,0) to (r,c): C(r+c, r)
    # Paths from (r,c) to (H-1, W-1): C((H-1-r)+(W-1-c), H-1-r)
    
    K = [0] * (H * W)
    
    for r in range(H):
        for c in range(W):
            # Paths from (0,0) to (r,c)
            ways_start = nCr(r + c, r)
            
            # Paths from (r,c) to (H-1, W-1)
            rem_r = H - 1 - r
            rem_c = W - 1 - c
            ways_end = nCr(rem_r + rem_c, rem_r)
            
            coeff = (ways_start * ways_end) % MOD
            K[r * W + c] = coeff
            
    # Calculate initial total sum
    current_total = 0
    for i in range(H * W):
        val = A[i]
        term = (val * K[i]) % MOD
        current_total = (current_total + term) % MOD
        
    # Process queries
    results = []
    
    for _ in range(Q):
        d = next(iterator)
        a_val = int(next(iterator))
        
        # Determine the cell (r, c) being updated
        # Takahashi moves from current (sh, sw)
        r, c = sh, sw
        
        if d == 'L':
            c -= 1
        elif d == 'R':
            c += 1
        elif d == 'U':
            r -= 1
        elif d == 'D':
            r += 1
            
        # Now (r, c) is the cell to update.
        # Update the grid value
        idx = r * W + c
        old_val = A[idx]
        A[idx] = a_val
        
        # Update the total sum
        coeff = K[idx]
        
        # Remove old contribution
        current_total = (current_total - (old_val * coeff) % MOD + MOD) % MOD
        # Add new contribution
        current_total = (current_total + (a_val * coeff) % MOD) % MOD
        
        results.append(str(current_total))
        
        # Update current position for next query
        sh, sw = r, c

    print('\n'.join(results))

if __name__ == '__main__':
    solve()