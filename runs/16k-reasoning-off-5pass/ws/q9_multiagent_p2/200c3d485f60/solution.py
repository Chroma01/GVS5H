class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If k is greater than the number of adjacent pairs, it's impossible
        if k > n - 1:
            return 0
        
        # We need to calculate: m * C(n-1, k) * (m-1)^(n-1-k) % MOD
        
        # Step 1: Calculate C(n-1, k) = (n-1)! / (k! * (n-1-k)!)
        # We compute factorials up to n-1
        limit = n - 1
        fact = [1] * (limit + 1)
        for i in range(2, limit + 1):
            fact[i] = (fact[i-1] * i) % MOD
            
        numerator = fact[limit]
        denominator = (fact[k] * fact[limit - k]) % MOD
        
        # Modular inverse using Fermat's Little Theorem: a^(MOD-2) % MOD
        denom_inv = pow(denominator, MOD - 2, MOD)
        comb = (numerator * denom_inv) % MOD
        
        # Step 2: Calculate (m-1)^(n-1-k) % MOD
        power_term = pow(m - 1, n - 1 - k, MOD)
        
        # Step 3: Combine all parts
        # Result = m * comb * power_term % MOD
        result = (m * comb) % MOD
        result = (result * power_term) % MOD
        
        return result