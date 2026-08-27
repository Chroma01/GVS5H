class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If k > n - 1, it's impossible to have k equal adjacent pairs in an array of size n
        if k > n - 1:
            return 0
        
        # Calculate (n-1)!
        fact_n_minus_1 = 1
        for i in range(1, n):
            fact_n_minus_1 = (fact_n_minus_1 * i) % MOD
            
        # Calculate k!
        fact_k = 1
        for i in range(1, k + 1):
            fact_k = (fact_k * i) % MOD
            
        # Calculate (n-1-k)!
        fact_n_minus_1_minus_k = 1
        for i in range(1, n - k):
            fact_n_minus_1_minus_k = (fact_n_minus_1_minus_k * i) % MOD
            
        # Calculate modular inverse of (k! * (n-1-k)!) using Fermat's Little Theorem
        denom = (fact_k * fact_n_minus_1_minus_k) % MOD
        denom_inv = pow(denom, MOD - 2, MOD)
        
        # Calculate C(n-1, k) = (n-1)! / (k! * (n-1-k)!)
        comb = (fact_n_minus_1 * denom_inv) % MOD
        
        # Calculate (m-1)^(n-1-k)
        power_term = pow(m - 1, n - 1 - k, MOD)
        
        # Final result: C(n-1, k) * m * (m-1)^(n-1-k)
        result = (comb * m) % MOD
        result = (result * power_term) % MOD
        
        return result