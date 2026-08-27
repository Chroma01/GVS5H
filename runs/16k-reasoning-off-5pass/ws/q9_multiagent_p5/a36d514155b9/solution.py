class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        def modInverse(a: int, mod: int) -> int:
            return pow(a, mod - 2, mod)
        
        def nCr_mod(n: int, r: int, mod: int) -> int:
            if r < 0 or r > n:
                return 0
            if r == 0 or r == n:
                return 1
            if r > n // 2:
                r = n - r
            
            num = 1
            den = 1
            for i in range(r):
                num = (num * (n - i)) % mod
                den = (den * (i + 1)) % mod
            
            return (num * modInverse(den, mod)) % mod
        
        def sum_diff(m_val: int) -> int:
            # Sum_{1 <= i < j <= m_val} (j - i)
            # = Sum_{d=1}^{m_val-1} d * (m_val - d)
            # = m_val * Sum(d) - Sum(d^2)
            if m_val <= 1:
                return 0
            
            N = m_val - 1
            sum_d = (N * (N + 1)) // 2
            sum_d2 = (N * (N + 1) * (2 * N + 1)) // 6
            
            return (m_val * sum_d - sum_d2) % MOD
        
        total_cells = m * n
        
        # Calculate combinations C(total_cells - 2, k - 2)
        # If k < 2, result is 0, but constraints say k >= 2.
        # If total_cells < 2, result is 0, but constraints say m*n >= 2.
        combinations = nCr_mod(total_cells - 2, k - 2, MOD)
        
        # Calculate sum of differences for rows and columns
        sum_row_diffs = sum_diff(m)
        sum_col_diffs = sum_diff(n)
        
        # Total sum of distances over all pairs of cells
        # Row contribution: n^2 * sum_row_diffs
        # Col contribution: m^2 * sum_col_diffs
        total_cell_dist_sum = ( (n * n) % MOD * sum_row_diffs + (m * m) % MOD * sum_col_diffs ) % MOD
        
        # Final answer
        return (total_cell_dist_sum * combinations) % MOD