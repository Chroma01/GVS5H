class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If k > n-1, it's impossible
        if k > n - 1:
            return 0
        
        # We need to compute: m * C(n-1, k) * (m-1)^(n-1-k) mod MOD
        
        # Step 1: Compute C(n-1, k) mod MOD
        # C(n, k) = n! / (k! * (n-k)!) mod MOD
        # We'll compute factorials and their modular inverses
        
        N = n - 1  # total positions for adjacent pairs
        
        # Precompute factorials up to N
        fact = [1] * (N + 1)
        for i in range(1, N + 1):
            fact[i] = fact[i-1] * i % MOD
        
        # Function to compute modular inverse using Fermat's little theorem
        def mod_inv(a: int) -> int:
            return pow(a, MOD - 2, MOD)
        
        # Compute C(N, k) = fact[N] * inv(fact[k]) * inv(fact[N-k])
        comb = fact[N] * mod_inv(fact[k]) % MOD * mod_inv(fact[N - k]) % MOD
        
        # Step 2: Compute (m-1)^(n-1-k) mod MOD
        exp = n - 1 - k
        unequal_choices = pow(m - 1, exp, MOD)
        
        # Step 3: Multiply everything together
        result = m % MOD * comb % MOD * unequal_choices % MOD
        
        return result