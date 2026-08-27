class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials up to n
        # We need up to n-1 for binomial coefficient C(n-1, k)
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD
        
        inv_fact = [1] * (n + 1)
        inv_fact[n] = pow(fact[n], MOD - 2, MOD)
        for i in range(n - 1, -1, -1):
            inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD
        
        # Compute C(n-1, k)
        if k > n - 1:
            binom = 0
        else:
            binom = fact[n - 1] * inv_fact[k] % MOD * inv_fact[n - 1 - k] % MOD
        
        # Compute (m-1)^k, handling 0^0 = 1
        if k == 0:
            pow_term = 1
        else:
            pow_term = pow(m - 1, k, MOD)
        
        return binom * m % MOD * pow_term % MOD