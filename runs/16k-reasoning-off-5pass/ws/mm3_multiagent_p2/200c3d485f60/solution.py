class Solution:
    MOD = 10**9 + 7
    
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = self.MOD
        
        # Edge case: impossible to have more equal pairs than n-1
        if k > n - 1:
            return 0
        
        # Precompute factorials, inverse factorials, and powers of (m-1) up to n
        # We need up to n-1 for binomial coefficient C(n-1, k)
        max_n = n  # allocate up to n for safety
        
        fact = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            fact[i] = fact[i-1] * i % MOD
        
        inv_fact = [1] * (max_n + 1)
        inv_fact[max_n] = pow(fact[max_n], MOD - 2, MOD)
        for i in range(max_n, 0, -1):
            inv_fact[i-1] = inv_fact[i] * i % MOD
        
        # Precompute powers of (m-1) up to n
        base = m - 1
        pow_base = [1] * (max_n + 1)
        for i in range(1, max_n + 1):
            pow_base[i] = pow_base[i-1] * base % MOD
        
        # Binomial coefficient C(n-1, k)
        def comb(N, R):
            if R < 0 or R > N:
                return 0
            return fact[N] * inv_fact[R] % MOD * inv_fact[N - R] % MOD
        
        binom = comb(n - 1, k)
        
        # m * (m-1)^(n-k-1)
        exponent = n - k - 1
        # pow_base[exponent] handles exponent=0 correctly (returns 1)
        result = binom * m % MOD
        result = result * pow_base[exponent] % MOD
        
        return result