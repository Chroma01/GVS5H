import sys

# Set recursion depth just in case, though we won't use recursion
sys.setrecursionlimit(2000)

def solve():
    # Read input from stdin
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    W = int(input_data[0])
    H = int(input_data[1])
    L = int(input_data[2])
    R = int(input_data[3])
    D = int(input_data[4])
    U = int(input_data[5])

    MOD = 998244353

    # Maximum value needed for factorials
    # The maximum coordinate sum is W + H.
    # The binomial coefficient arguments can go up to W + H + 2.
    MAX_VAL = W + H + 5

    # Precompute factorials and inverse factorials
    fact = [1] * MAX_VAL
    inv_fact = [1] * MAX_VAL

    for i in range(1, MAX_VAL):
        fact[i] = (fact[i-1] * i) % MOD

    # Fermat's Little Theorem for modular inverse
    inv_fact[MAX_VAL-1] = pow(fact[MAX_VAL-1], MOD - 2, MOD)
    for i in range(MAX_VAL-2, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD

    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % MOD
        return (num * den) % MOD

    # Function to calculate sum of binom(nCr_mod(i+j+2, i+2)) for i in [0, W] and j in [0, H]
    # This calculates the total number of paths in the full grid [0, W] x [0, H]
    # Total = sum_{xe=0}^W sum_{ye=0}^H C(xe + ye + 2, xe + 2)
    # We can compute this efficiently.
    # Let S(W, H) = sum_{xe=0}^W sum_{ye=0}^H C(xe + ye + 2, xe + 2)
    
    # We can compute the inner sum for a fixed xe:
    # Inner(xe) = sum_{ye=0}^H C(xe + ye + 2, xe + 2)
    # Using the identity sum_{i=0}^n C(r+i, r) = C(r+n+1, r+1)
    # Here, let k = xe + 2. Then we sum C(k + ye, k) for ye from 0 to H.
    # This equals C(k + H + 1, k + 1) = C(xe + 2 + H + 1, xe + 2 + 1) = C(xe + H + 3, xe + 3)
    
    # So Total = sum_{xe=0}^W C(xe + H + 3, xe + 3)
    # Let j = xe + 3. Then xe = j - 3. As xe goes 0 to W, j goes 3 to W+3.
    # Total = sum_{j=3}^{W+3} C(j + H, j)
    # Using identity sum_{i=r}^n C(i, r) = C(n+1, r+1)
    # Here, we are summing C(j+H, j) = C(j+H, H).
    # Let i = j+H. Then j = i-H. As j goes 3 to W+3, i goes H+3 to W+H+3.
    # Total = sum_{i=H+3}^{W+H+3} C(i, H)
    # Using identity sum_{i=r}^n C(i, r) = C(n+1, r+1)
    # Sum_{i=H}^{W+H+3} C(i, H) = C(W+H+4, H+1)
    # We need to subtract the terms for i=H, H+1, H+2.
    # Terms to subtract: C(H, H) + C(H+1, H) + C(H+2, H)
    # C(H, H) = 1
    # C(H+1, H) = H+1
    # C(H+2, H) = C(H+2, 2) = (H+2)(H+1)/2
    
    # So Total = C(W+H+4, H+1) - (1 + (H+1) + (H+2)*(H+1)//2)
    
    total_binom = nCr_mod(W + H + 4, H + 1)
    
    subtract_term = 1 + (H + 1) + ((H + 2) * (H + 1) // 2)
    subtract_term %= MOD
    
    total_paths = (total_binom - subtract_term + MOD) % MOD

    # Now calculate Bad paths (paths that enter the hole [L, R] x [D, U])
    # We sum over the first entry point P in the hole.
    # First entry points are on the left edge (x=L, D<=y<=U) and bottom edge (y=D, L<=x<=R).
    # To avoid double counting, we handle the corner (L,D) separately or split the ranges.
    
    bad_paths = 0

    # 1. Left edge: P = (L, y) for y in [D, U]
    # For y = D: Previous point can be (L-1, D) or (L, D-1).
    # Paths to (L-1, D): Starts in [0, L-1] x [0, D]. Count = C(L-1 + D + 2, L-1 + 2) = C(L+D+1, L+1)
    # Paths to (L, D-1): Starts in [0, L] x [0, D-1]. Count = C(L + D-1 + 2, L + 2) = C(L+D+1, L+2)
    
    if L >= 0 and D >= 0:
        # Corner (L, D)
        term1 = nCr_mod(L + D + 1, L + 1)
        term2 = nCr_mod(L + D + 1, L + 2)
        bad_paths = (bad_paths + term1 + term2) % MOD
        
        # Left edge for y in [D+1, U]
        # Previous point must be (L-1, y).
        # Paths to (L-1, y): Starts in [0, L-1] x [0, y]. Count = C(L-1 + y + 2, L-1 + 2) = C(L+y+1, L+1)
        for y in range(D + 1, U + 1):
            term = nCr_mod(L + y + 1, L + 1)
            bad_paths = (bad_paths + term) % MOD

    # 2. Bottom edge: P = (x, D) for x in [L+1, R]
    # Previous point must be (x-1, D).
    # Paths to (x-1, D): Starts in [0, x-1] x [0, D]. Count = C(x-1 + D + 2, x-1 + 2) = C(x+D+1, x+1)
    
    for x in range(L + 1, R + 1):
        term = nCr_mod(x + D + 1, x + 1)
        bad_paths = (bad_paths + term) % MOD

    # Result
    ans = (total_paths - bad_paths + MOD) % MOD
    print(ans)

solve()