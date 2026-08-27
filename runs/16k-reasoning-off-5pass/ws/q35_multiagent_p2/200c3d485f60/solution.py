class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If m is 1, then the only possible array is all 1s.
        # This array has n-1 equal adjacent pairs.
        # So if k == n-1, answer is 1, else 0.
        if m == 1:
            return 1 if k == n - 1 else 0
        
        # The formula is: C(n-1, k) * m * (m-1)^(n-1-k) mod MOD
        
        # Calculate C(n-1, k) mod MOD
        # We need factorials up to n-1
        N = n - 1
        # Since n <= 10^5, we can compute factorials iteratively
        
        fact = [1] * (N + 1)
        inv_fact = [1] * (N + 1)
        
        for i in range(1, N + 1):
            fact[i] = fact[i-1] * i % MOD
            
        # Compute inverse factorial of N using Fermat's little theorem
        inv_fact[N] = pow(fact[N], MOD - 2, MOD)
        for i in range(N - 1, -1, -1):
            inv_fact[i] = inv_fact[i+1] * (i + 1) % MOD
            
        def nCr_mod(n, r, mod):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = inv_fact[r] * inv_fact[n - r] % mod
            return num * den % mod
        
        combinations = nCr_mod(N, k, MOD)
        
        # Calculate m * (m-1)^(n-1-k) mod MOD
        # Note: m-1 is at least 1 here because m >= 2 (handled m==1 above)
        unequal_choices = pow(m - 1, N - k, MOD)
        total_ways = m * unequal_choices % MOD
        
        result = combinations * total_ways % MOD
        return result