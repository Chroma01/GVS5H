class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If k is greater than the number of adjacent pairs (n-1), it's impossible
        if k > n - 1:
            return 0
        
        # Precompute factorials and inverse factorials up to n
        # We need factorials up to n-1 for C(n-1, k)
        limit = n
        fact = [1] * (limit + 1)
        inv = [1] * (limit + 1)
        
        for i in range(1, limit + 1):
            fact[i] = (fact[i-1] * i) % MOD
            
        # Fermat's Little Theorem for modular inverse: a^(MOD-2) % MOD
        inv[limit] = pow(fact[limit], MOD - 2, MOD)
        for i in range(limit - 1, -1, -1):
            inv[i] = (inv[i+1] * (i + 1)) % MOD
            
        # Calculate C(n-1, k)
        def nCr_mod(n, r):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = (inv[r] * inv[n-r]) % MOD
            return (num * den) % MOD
        
        combinations = nCr_mod(n - 1, k)
        
        # Calculate (m-1)^(n-1-k)
        power_term = pow(m - 1, n - 1 - k, MOD)
        
        # Final result: m * (m-1)^(n-1-k) * C(n-1, k)
        result = (m * power_term) % MOD
        result = (result * combinations) % MOD
        
        return result