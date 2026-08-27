import sys

# Set recursion depth just in case, though we won't use recursion
sys.setrecursionlimit(2000)

def solve():
    # Read input
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
    
    # Precompute factorials and inverse factorials
    # Max n needed for nCr is roughly W + H + 4
    MAX_N = W + H + 10
    fact = [1] * MAX_N
    inv_fact = [1] * MAX_N
    
    for i in range(1, MAX_N):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv_fact[MAX_N-1] = pow(fact[MAX_N-1], MOD - 2, MOD)
    for i in range(MAX_N-2, -1, -1):
        inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD
        
    def nCr(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv_fact[r] * inv_fact[n-r]) % MOD
        return (num * den) % MOD

    # Helper for Out(x, y)
    # Out(x, y) = binom(W-x + H-y + 2, H-y + 1) - 1
    def get_out(x, y):
        n = W - x + H - y + 2
        r = H - y + 1
        val = nCr(n, r)
        return (val - 1 + MOD) % MOD

    # Calculate Total Paths in Full Grid |A|
    # |A| = sum_{x=0}^W sum_{y=0}^H Out(x, y)
    # Closed form derived:
    # |A| = binom(W + H + 4, H + 2) - 1 - (W + 2) - (W + 1)(H + 1)
    
    term1 = nCr(W + H + 4, H + 2)
    term2 = 1
    term3 = (W + 2) % MOD
    term4 = ((W + 1) * (H + 1)) % MOD
    
    total_A = (term1 - term2 - term3 - term4) % MOD
    total_A = (total_A + MOD) % MOD # Ensure positive
    
    # Calculate Invalid Paths |B|
    # |B| = Sum_{P in Hole, First Entry} In(P) * Out(P)
    # First entry points are on Left Edge: (L, y) for D <= y <= U
    # and Bottom Edge: (x, D) for L <= x <= R.
    # Corner (L, D) is in both, so we subtract it once.
    
    def get_in_left(y):
        # In(L, y) = binom(y + L + 1, L) - binom(y - H + L, L)
        term1 = nCr(y + L + 1, L)
        term2 = nCr(y - H + L, L)
        return (term1 - term2 + MOD) % MOD

    def get_in_bottom(x):
        # In(x, D) = binom(x + D + 1, D)
        return nCr(x + D + 1, D)

    sum_B = 0
    
    # Sum over Left Edge: x = L, D <= y <= U
    for y in range(D, U + 1):
        in_val = get_in_left(y)
        out_val = get_out(L, y)
        term = (in_val * out_val) % MOD
        sum_B = (sum_B + term) % MOD
        
    # Sum over Bottom Edge: y = D, L <= x <= R
    for x in range(L, R + 1):
        in_val = get_in_bottom(x)
        out_val = get_out(x, D)
        term = (in_val * out_val) % MOD
        sum_B = (sum_B + term) % MOD
        
    # Subtract corner (L, D) which was counted twice
    in_corner = get_in_left(D) # Same as get_in_bottom(L)
    out_corner = get_out(L, D)
    corner_term = (in_corner * out_corner) % MOD
    sum_B = (sum_B - corner_term + MOD) % MOD
    
    ans = (total_A - sum_B + MOD) % MOD
    print(ans)

if __name__ == '__main__':
    solve()