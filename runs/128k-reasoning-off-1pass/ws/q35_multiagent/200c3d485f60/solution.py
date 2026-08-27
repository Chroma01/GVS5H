class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If m is 1, then all elements must be 1.
        # Then all adjacent pairs are equal. So k must be n-1.
        if m == 1:
            return 1 if k == n - 1 else 0
        
        # We need to compute C(n-1, k) * m * (m-1)^(n-1-k) mod MOD
        
        # Helper function for modular inverse using Fermat's little theorem
        def mod_inverse(a, mod):
            return pow(a, mod - 2, mod)
        
        # Helper function to compute nCr mod p
        def nCr_mod(n, r, mod):
            if r < 0 or r > n:
                return 0
            # Precompute factorials and inverse factorials if needed, but for single call:
            # C(n, r) = n! / (r! * (n-r)!) mod mod
            fact = [1] * (n + 1)
            for i in range(1, n + 1):
                fact[i] = (fact[i - 1] * i) % mod
            
            inv_fact_r = mod_inverse(fact[r], mod)
            inv_fact_nr = mod_inverse(fact[n - r], mod)
            
            return (fact[n] * inv_fact_r % mod) * inv_fact_nr % mod
        
        # Calculate the binomial coefficient C(n-1, k)
        combinations = nCr_mod(n - 1, k, MOD)
        
        # Calculate m * (m-1)^(n-1-k) mod MOD
        # Note: if n-1-k is 0, then (m-1)^0 = 1
        diff_choices = pow(m - 1, n - 1 - k, MOD)
        first_element_choices = m % MOD
        
        result = (combinations * first_element_choices) % MOD
        result = (result * diff_choices) % MOD
        
        return result