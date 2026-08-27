class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Total number of cells
        total_cells = m * n
        
        # If k < 2, there are no pairs, so sum is 0
        if k < 2:
            return 0
        
        # Calculate sum of |i - j| for all unordered pairs of indices from 1 to L
        # Formula: L * (L^2 - 1) // 6
        # We need to compute this modulo MOD. Since we divide by 6, we multiply by modular inverse of 6.
        
        def sum_abs_diff(L: int) -> int:
            # L * (L^2 - 1) / 6
            # Compute numerator modulo MOD
            num = (L % MOD) * ((L * L - 1) % MOD) % MOD
            # Modular inverse of 6 modulo 10^9+7
            inv6 = pow(6, MOD - 2, MOD)
            return (num * inv6) % MOD
        
        # Sum of row differences for all unordered pairs of cells
        # For each pair of rows (i, j), there are n * n pairs of cells.
        # But note: the sum_abs_diff(m) gives sum over unordered pairs of rows.
        # For each such unordered pair of rows, the number of cell pairs is n * n.
        sum_row_diffs = sum_abs_diff(m)
        S_row = (sum_row_diffs * (n % MOD) % MOD * (n % MOD)) % MOD
        
        # Sum of column differences for all unordered pairs of cells
        sum_col_diffs = sum_abs_diff(n)
        S_col = (sum_col_diffs * (m % MOD) % MOD * (m % MOD)) % MOD
        
        # Total sum of Manhattan distances over all unordered pairs of cells
        S_total = (S_row + S_col) % MOD
        
        # Number of ways to place remaining k-2 pieces in total_cells - 2 cells
        # C(total_cells - 2, k - 2)
        N = total_cells - 2
        K = k - 2
        
        # If K < 0 or K > N, then C(N, K) = 0
        if K < 0 or K > N:
            return 0
        
        # Compute C(N, K) % MOD
        # Since N <= 10^5, we can compute factorials or compute directly
        # We'll compute numerator and denominator separately
        
        # Precompute factorials up to N if needed, but since N is small, we can compute directly
        # C(N, K) = N! / (K! * (N-K)!)
        
        # To avoid large numbers, we compute modulo MOD
        # We need modular inverse for denominator
        
        def nCr_mod(n: int, r: int, mod: int) -> int:
            if r < 0 or r > n:
                return 0
            if r == 0 or r == n:
                return 1
            if r > n // 2:
                r = n - r
            
            # Compute numerator: n * (n-1) * ... * (n-r+1)
            num = 1
            for i in range(r):
                num = (num * ((n - i) % mod)) % mod
            
            # Compute denominator: r!
            den = 1
            for i in range(1, r + 1):
                den = (den * i) % mod
            
            # Modular inverse of denominator
            inv_den = pow(den, mod - 2, mod)
            
            return (num * inv_den) % mod
        
        ways = nCr_mod(N, K, MOD)
        
        result = (S_total * ways) % MOD
        return result