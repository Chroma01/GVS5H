import sys

MOD = 998244353

def main():
    input_data = sys.stdin.read().split()
    N = int(input_data[0])
    s = input_data[1].strip()
    k = sum(1 for ch in s if ch == '1')
    M = N - k
    
    # Precompute factorials up to N
    fact = [1] * (N + 1)
    for i in range(1, N + 1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact = [1] * (N + 1)
    inv_fact[N] = pow(fact[N], MOD-2, MOD)
    for i in range(N, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD
    
    def C(n, r):
        if r < 0 or r > n:
            return 0
        return fact[n] * inv_fact[r] % MOD * inv_fact[n-r] % MOD
    
    # Precompute powers of 2
    pow2 = [1] * (k + 1)
    for i in range(1, k + 1):
        pow2[i] = pow2[i-1] * 2 % MOD
    
    # Precompute 1/factorials for efficiency
    inv_fact_M = inv_fact[M]
    inv_fact_k = inv_fact[k]
    
    ans = 0
    # Iterate over a and c (counts of 0 and 2 in complement)
    for a in range(M + 1):
        for c in range(M - a + 1):
            b = M - a - c
            # Number of ways for complement: M!/(a! c! b!)
            ways_comp = fact[M] * inv_fact[a] % MOD * inv_fact[c] % MOD * inv_fact[b] % MOD
            
            # For S, we need u >= c - a and v >= a - c
            min_u = max(0, c - a)
            min_v = max(0, a - c)
            
            # Sum over u and v
            for u in range(min_u, k + 1):
                for v in range(min_v, k - u + 1):
                    s_val = k - u - v
                    # k!/(u! v! s!) * 2^s_val
                    ways_S = fact[k] * inv_fact[u] % MOD * inv_fact[v] % MOD * inv_fact[s_val] % MOD * pow2[s_val] % MOD
                    ans = (ans + ways_comp * ways_S) % MOD
    
    print(ans % MOD)

if __name__ == "__main__":
    main()