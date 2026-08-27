class Solution:
    def countGoodArrays(self, n: int, m: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Helper function for modular exponentiation
        def mod_pow(base, exp, mod):
            result = 1
            base %= mod
            while exp > 0:
                if exp % 2 == 1:
                    result = (result * base) % mod
                base = (base * base) % mod
                exp //= 2
            return result
        
        # Helper function for modular inverse using Fermat's little theorem
        def mod_inv(a, mod):
            return mod_pow(a, mod - 2, mod)
        
        # Helper function to compute combinations C(n, k) mod p
        def comb(n, k, mod):
            if k < 0 or k > n:
                return 0
            if k == 0 or k == n:
                return 1
            # C(n, k) = n! / (k! * (n-k)!)
            # We compute numerator and denominator separately
            # To avoid large factorials, we can compute iteratively
            # But for n up to 10^5, we can precompute or compute directly
            
            # Compute C(n, k) using multiplicative formula with modular inverse
            # C(n, k) = product_{i=1}^{k} (n - i + 1) / i
            num = 1
            den = 1
            for i in range(1, k + 1):
                num = (num * (n - i + 1)) % mod
                den = (den * i) % mod
            return (num * mod_inv(den, mod)) % mod
        
        # The answer is C(n-1, k) * m * (m-1)^(n-1-k) mod MOD
        # Number of ways to choose which k positions out of n-1 are equal
        ways_to_choose_equal_positions = comb(n - 1, k, MOD)
        
        # Number of ways to assign values:
        # First element: m choices
        # Each subsequent block start (where value changes): m-1 choices
        # There are n - k blocks, so n - k - 1 changes after the first block
        # Total value assignments: m * (m-1)^(n-k-1)
        value_assignments = (m * mod_pow(m - 1, n - k - 1, MOD)) % MOD
        
        result = (ways_to_choose_equal_positions * value_assignments) % MOD
        return result