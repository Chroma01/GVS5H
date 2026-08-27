class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials for combinations
        fact = [1] * n
        inv_fact = [1] * n
        
        for i in range(1, n):
            fact[i] = fact[i - 1] * i % MOD
        
        # Modular inverse using Fermat's Little Theorem
        inv_fact[n - 1] = pow(fact[n - 1], MOD - 2, MOD)
        for i in range(n - 2, -1, -1):
            inv_fact[i] = inv_fact[i + 1] * (i + 1) % MOD
        
        def comb(a, b):
            if b < 0 or b > a:
                return 0
            return fact[a] * inv_fact[b] % MOD * inv_fact[a - b] % MOD
        
        # Number of ways to choose which k of the n-1 gaps are "equal"
        ways_choose_gaps = comb(n - 1, k)
        
        # Number of ways to assign values: first block has m choices,
        # each subsequent block has m-1 choices (must differ from previous)
        # There are n - k blocks total
        value_assignments = m * pow(m - 1, n - k - 1, MOD) % MOD
        
        return ways_choose_gaps * value_assignments % MOD