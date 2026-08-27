class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # If k > n - 1, it's impossible to have k adjacent equal pairs
        if k > n - 1:
            return 0
        
        # We need to compute C(n-1, k) * m * (m-1)^(n-1-k) % MOD
        
        # Helper function for modular exponentiation
        def power(base, exp):
            result = 1
            base %= MOD
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % MOD
                base = (base * base) % MOD
                exp //= 2
            return result
        
        # Helper function for modular inverse using Fermat's Little Theorem
        def modInverse(n):
            return power(n, MOD - 2)
        
        # Helper function for factorial
        def factorial(num):
            res = 1
            for i in range(2, num + 1):
                res = (res * i) % MOD
            return res
        
        # Calculate C(n-1, k) = (n-1)! / (k! * (n-1-k)!)
        N = n - 1
        num = factorial(N)
        den = (factorial(k) * factorial(N - k)) % MOD
        combinations = (num * modInverse(den)) % MOD
        
        # Calculate m * (m-1)^(N-k)
        term2 = (m * power(m - 1, N - k)) % MOD
        
        # Final result
        return (combinations * term2) % MOD