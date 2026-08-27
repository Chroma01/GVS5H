import sys

# Increase recursion depth just in case, though we use iterative approach
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
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

    # Precompute factorials and inverse factorials for nCr
    # We need up to W + H + 5
    MAX_N = W + H + 10
    fact = [1] * MAX_N
    inv = [1] * MAX_N
    
    for i in range(2, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for i in range(MAX_N-2, 1, -1):
        inv[i] = (inv[i+1] * (i+1)) % MOD

    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD

    # Calculate Total paths in full grid [0, W] x [0, H]
    # The number of valid paths in a full grid is given by:
    # binom(W+H+3, W+1) - (W+1)(H+1)
    # This formula represents the sum of paths from any valid start to any valid end in a full grid.
    total_full = (nCr(W + H + 3, W + 1) - (W + 1) * (H + 1)) % MOD
    total_full = (total_full + MOD) % MOD

    # Calculate paths that touch the hole [L, R] x [D, U]
    # The number of paths from (0,0) to (W,H) that touch the hole is:
    # binom(L+D, L) * binom(W+H-L-D, W-L) * binom(R-L+U-D+1, R-L) * binom(W-R+H-U, W-R)
    # However, we need to subtract paths that touch the hole from the total valid paths.
    # The formula for paths touching the hole in the context of the problem (sum of paths between valid nodes)
    # is derived as:
    # binom(L+D, L) * binom(W+H-L-D, W-L) * binom(R-L+U-D+1, R-L) * binom(W-R+H-U, W-R)
    
    term1 = nCr(L + D, L)
    term2 = nCr(W + H - L - D, W - L)
    term3 = nCr(R - L + U - D + 1, R - L)
    term4 = nCr(W - R + H - U, W - R)
    
    paths_touching_hole = (term1 * term2) % MOD
    paths_touching_hole = (paths_touching_hole * term3) % MOD
    paths_touching_hole = (paths_touching_hole * term4) % MOD

    # The answer is Total - Paths touching hole
    ans = (total_full - paths_touching_hole) % MOD
    ans = (ans + MOD) % MOD

    print(ans)

if __name__ == '__main__':
    solve()