class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        def modInverse(a: int) -> int:
            return pow(a, MOD - 2, MOD)
        
        def nCr_mod(n: int, r: int) -> int:
            if r < 0 or r > n:
                return 0
            if r == 0 or r == n:
                return 1
            if r > n // 2:
                r = n - r
            
            numerator = 1
            denominator = 1
            
            for i in range(r):
                numerator = (numerator * (n - i)) % MOD
                denominator = (denominator * (i + 1)) % MOD
                
            return (numerator * modInverse(denominator)) % MOD
        
        def sum_dist_pairs(L: int) -> int:
            # Sum of |i - j| for 1 <= i < j <= L
            # Formula: L * (L^2 - 1) / 6
            if L < 2:
                return 0
            # Perform calculation modulo MOD to avoid large numbers, 
            # but division by 6 requires modular inverse.
            # L * (L^2 - 1) is always divisible by 6 for integer L.
            # We compute (L * (L^2 - 1)) % MOD * inv(6) % MOD.
            val = (L * (L * L - 1)) % MOD
            return (val * modInverse(6)) % MOD
        
        total_cells = m * n
        
        # Calculate the number of ways to choose the remaining k-2 pieces
        # from the remaining total_cells - 2 cells.
        ways_to_place_rest = nCr_mod(total_cells - 2, k - 2)
        
        # Calculate sum of row distances for all pairs of cells
        # For each pair of rows (r1, r2), there are n * n pairs of cells.
        # Sum of |r1 - r2| for all pairs of rows is sum_dist_pairs(m).
        row_sum = sum_dist_pairs(m) * (n * n) % MOD
        
        # Calculate sum of column distances for all pairs of cells
        # For each pair of columns (c1, c2), there are m * m pairs of cells.
        # Sum of |c1 - c2| for all pairs of columns is sum_dist_pairs(n).
        col_sum = sum_dist_pairs(n) * (m * m) % MOD
        
        # Total sum of Manhattan distances over all pairs of cells
        total_dist_sum = (row_sum + col_sum) % MOD
        
        # Final result
        return (ways_to_place_rest * total_dist_sum) % MOD