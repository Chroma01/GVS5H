import sys

# Set recursion depth just in case, though not needed for this iterative solution
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    N = int(input_data[0])
    s = input_data[1]
    
    MOD = 998244353
    
    # Count number of 1s in s
    k = s.count('1')
    
    # Precompute factorials and inverse factorials
    # We need factorials up to N
    fact = [1] * (N + 1)
    inv = [1] * (N + 1)
    
    for i in range(1, N + 1):
        fact[i] = (fact[i-1] * i) % MOD
        
    inv[N] = pow(fact[N], MOD - 2, MOD)
    for i in range(N - 1, -1, -1):
        inv[i] = (inv[i+1] * (i + 1)) % MOD
        
    def nCr_mod(n, r):
        if r < 0 or r > n:
            return 0
        num = fact[n]
        den = (inv[r] * inv[n-r]) % MOD
        return (num * den) % MOD
    
    # Calculate W = sum_{m=0}^{floor(N/2)} C(N, m) * C(N-m, m)
    W = 0
    limit = N // 2
    
    for m in range(limit + 1):
        # C(N, m) * C(N-m, m)
        term1 = nCr_mod(N, m)
        term2 = nCr_mod(N - m, m)
        term = (term1 * term2) % MOD
        W = (W + term) % MOD
        
    # Calculate 2^k mod MOD
    pow2k = pow(2, k, MOD)
    
    # Final Answer
    ans = (W * pow2k) % MOD
    
    print(ans)

if __name__ == '__main__':
    solve()