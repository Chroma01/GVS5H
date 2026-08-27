class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If k > n - 1, it's impossible to have k adjacent equal pairs in an array of size n
        if k > n - 1:
            return 0
        
        # Precompute factorials and inverse factorials for combinations
        # We need factorials up to n-1
        limit = n
        fact = [1] * limit
        inv = [1] * limit
        
        for i in range(1, limit):
            fact[i] = (fact[i-1] * i) % MOD
            
        # Modular inverse using Fermat's Little Theorem: a^(MOD-2) % MOD
        inv[limit-1] = pow(fact[limit-1], MOD - 2, MOD)
        for i in range(limit-2, -1, -1):
            inv[i] = (inv[i+1] * (i + 1)) % MOD
            
        def nCr_mod(n, r):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = (inv[r] * inv[n-r]) % MOD
            return (num * den) % MOD
        
        # Calculate C(n-1, k)
        combinations = nCr_mod(n - 1, k)
        
        # Calculate (m-1)^(n-1-k)
        power_term = pow(m - 1, n - 1 - k, MOD)
        
        # Final result: m * (m-1)^(n-1-k) * C(n-1, k)
        result = (m * power_term) % MOD
        result = (result * combinations) % MOD
        
        return result