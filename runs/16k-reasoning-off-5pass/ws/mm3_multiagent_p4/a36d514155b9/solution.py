import sys
from math import comb

MOD = 10**9 + 7

class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        # Total number of cells
        total_cells = m * n
        
        # Precompute factorials up to total_cells
        fact = [1] * (total_cells + 1)
        for i in range(1, total_cells + 1):
            fact[i] = fact[i-1] * i % MOD
        
        # Modular inverse using Fermat's little theorem
        inv_fact = [1] * (total_cells + 1)
        inv_fact[total_cells] = pow(fact[total_cells], MOD - 2, MOD)
        for i in range(total_cells - 1, -1, -1):
            inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
        
        def nCr(N, R):
            if R < 0 or R > N:
                return 0
            return fact[N] * inv_fact[R] % MOD * inv_fact[N-R] % MOD
        
        # Number of placements containing any specific pair of cells
        placements = nCr(total_cells - 2, k - 2)
        
        # Compute S = sum of Manhattan distances over all unordered pairs of cells
        # Row contribution: n^2 * (m^3 - m) / 6
        # Column contribution: m^2 * (n^3 - n) / 6
        inv6 = pow(6, MOD - 2, MOD)
        
        row_part = (n * n) % MOD
        col_part = (m * m) % MOD
        
        m_cubed = (m * m % MOD) * m % MOD
        n_cubed = (n * n % MOD) * n % MOD
        
        row_sum = (m_cubed - m) % MOD
        col_sum = (n_cubed - n) % MOD
        
        S = (row_part * row_sum + col_part * col_sum) % MOD
        S = S * inv6 % MOD
        
        return placements * S % MOD