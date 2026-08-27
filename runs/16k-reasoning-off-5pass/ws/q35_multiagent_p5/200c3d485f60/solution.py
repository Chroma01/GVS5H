class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If m == 1, then all elements must be 1.
        # Then all n-1 adjacent pairs are equal.
        # So if k == n-1, answer is 1, else 0.
        # This is naturally handled by the formula below because (m-1) = 0,
        # so if n-1-k > 0, (m-1)^(n-1-k) = 0.
        
        # We need to compute:
        # C(n-1, k) * m * (m-1)^(n-1-k) mod MOD
        
        # First, handle edge case: if k > n-1, it's impossible
        if k > n - 1:
            return 0
        
        # Calculate (m-1)^(n-1-k) mod MOD
        # Note: if m-1 == 0 and exponent > 0, pow(0, exp, MOD) returns 0, which is correct.
        # If exponent is 0, pow(0, 0, MOD) returns 1, which is also correct.
        unequal_ways = pow(m - 1, n - 1 - k, MOD)
        
        # Calculate m mod MOD
        m_mod = m % MOD
        
        # Calculate C(n-1, k) mod MOD
        # C(n, k) = n! / (k! * (n-k)!) mod MOD
        # We'll compute factorials and their modular inverses
        
        N = n - 1
        K = k
        
        # If K < 0 or K > N, C(N, K) = 0
        if K < 0 or K > N:
            comb = 0
        else:
            # Compute numerator: N!
            # Compute denominator: K! * (N-K)!
            # Use Fermat's Little Theorem for modular inverse since MOD is prime
            
            # Precompute factorials up to N
            fact = [1] * (N + 1)
            for i in range(1, N + 1):
                fact[i] = (fact[i-1] * i) % MOD
            
            numerator = fact[N]
            denom = (fact[K] * fact[N - K]) % MOD
            
            # Modular inverse of denom using pow(denom, MOD-2, MOD)
            denom_inv = pow(denom, MOD - 2, MOD)
            
            comb = (numerator * denom_inv) % MOD
        
        # Final answer: C(n-1, k) * m * (m-1)^(n-1-k)
        ans = (comb * m_mod) % MOD
        ans = (ans * unequal_ways) % MOD
        
        return ans