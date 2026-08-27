class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Edge case: if m is 1, then all elements must be 1.
        # This means all adjacent pairs are equal, so k must be n-1.
        if m == 1:
            return 1 if k == n - 1 else 0
        
        # If n is 1, then k must be 0.
        # There are m choices for the single element.
        if n == 1:
            return m % MOD
        
        # Number of ways to choose which k of the n-1 gaps are equal
        # C(n-1, k)
        # We need to compute combinations modulo MOD
        
        # Precompute factorials for combinations
        # Since n <= 10^5, we can precompute up to n
        max_val = n  # we need factorials up to n-1, so n is sufficient
        
        fact = [1] * (max_val + 1)
        inv_fact = [1] * (max_val + 1)
        
        for i in range(1, max_val + 1):
            fact[i] = (fact[i-1] * i) % MOD
            
        # Fermat's little theorem for modular inverse: a^(MOD-2) % MOD
        inv_fact[max_val] = pow(fact[max_val], MOD - 2, MOD)
        for i in range(max_val - 1, -1, -1):
            inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD
            
        def comb(a, b):
            if b < 0 or b > a:
                return 0
            num = fact[a]
            den = (inv_fact[b] * inv_fact[a-b]) % MOD
            return (num * den) % MOD
        
        # C(n-1, k)
        ways_choose_gaps = comb(n - 1, k)
        
        # Number of ways to assign values to blocks:
        # There are n - k blocks.
        # First block: m choices
        # Each subsequent block: m-1 choices (must be different from previous)
        # Total: m * (m-1)^(n-k-1)
        num_blocks = n - k
        ways_assign_values = (m * pow(m - 1, num_blocks - 1, MOD)) % MOD
        
        return (ways_choose_gaps * ways_assign_values) % MOD