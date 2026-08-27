class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials for combinations
        # The maximum value needed for factorial is max(m*n, m+1, n+1)
        # Since m*n <= 10^5, we can precompute up to 10^5 + 5
        limit = m * n + 5
        fact = [1] * limit
        inv = [1] * limit
        
        for i in range(1, limit):
            fact[i] = (fact[i-1] * i) % MOD
            
        inv[limit-1] = pow(fact[limit-1], MOD - 2, MOD)
        for i in range(limit-2, -1, -1):
            inv[i] = (inv[i+1] * (i + 1)) % MOD
            
        def nCr_mod(n, r):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = (inv[r] * inv[n-r]) % MOD
            return (num * den) % MOD
        
        # Calculate the sum of Manhattan distances for all pairs of cells in the grid
        # This is split into row contribution and column contribution.
        # Row contribution: For each pair of rows (i, j) with i < j, there are n*n pairs of cells
        # (one in row i, one in row j). The distance is (j-i).
        # Sum over all pairs of rows: n^2 * sum_{0<=i<j<m} (j-i)
        # sum_{0<=i<j<m} (j-i) = binom(m+1, 3)
        # Similarly for columns: m^2 * binom(n+1, 3)
        
        # binom(m+1, 3)
        term_m = nCr_mod(m + 1, 3)
        row_sum = (n * n) % MOD * term_m % MOD
        
        # binom(n+1, 3)
        term_n = nCr_mod(n + 1, 3)
        col_sum = (m * m) % MOD * term_n % MOD
        
        total_base_sum = (row_sum + col_sum) % MOD
        
        # The number of ways to choose k pieces such that a specific pair of cells is included
        # is binom(m*n - 2, k - 2).
        # If k < 2, no pairs exist, sum is 0.
        if k < 2:
            return 0
            
        multiplier = nCr_mod(m * n - 2, k - 2)
        
        return (total_base_sum * multiplier) % MOD