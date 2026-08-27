class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Total number of cells in the grid
        total_cells = m * n
        
        # Precompute factorials and inverse factorials up to total_cells
        # Since total_cells <= 10^5, this is efficient.
        limit = total_cells
        fact = [1] * (limit + 1)
        inv = [1] * (limit + 1)
        
        for i in range(1, limit + 1):
            fact[i] = (fact[i-1] * i) % MOD
            
        inv[limit] = pow(fact[limit], MOD - 2, MOD)
        for i in range(limit - 1, -1, -1):
            inv[i] = (inv[i+1] * (i + 1)) % MOD
            
        def nCr_mod(n, r):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = (inv[r] * inv[n-r]) % MOD
            return (num * den) % MOD
        
        # Calculate W = C(total_cells - 2, k - 2)
        # This represents the number of ways to place the remaining k-2 pieces
        # after fixing a specific pair of pieces.
        if k > total_cells:
            return 0
            
        W = nCr_mod(total_cells - 2, k - 2)
        
        # Calculate S_m = sum_{d=1}^{m-1} d(m-d) = m(m^2-1)/6
        # This is the sum of distances between all pairs of row indices.
        inv6 = pow(6, MOD - 2, MOD)
        
        if m < 2:
            Sm = 0
        else:
            Sm = (m * (m * m - 1)) % MOD
            Sm = (Sm * inv6) % MOD
            
        # Calculate S_n = sum_{d=1}^{n-1} d(n-d) = n(n^2-1)/6
        # This is the sum of distances between all pairs of column indices.
        if n < 2:
            Sn = 0
        else:
            Sn = (n * (n * n - 1)) % MOD
            Sn = (Sn * inv6) % MOD
            
        # The total sum of Manhattan distances over all pairs of cells in the grid is:
        # n^2 * Sm + m^2 * Sn
        # Sm and Sn are sums over unordered pairs of indices (i < j).
        # The factor n^2 accounts for the number of column pairs for each row pair.
        # The factor m^2 accounts for the number of row pairs for each column pair.
        
        term1 = (n * n) % MOD
        term1 = (term1 * Sm) % MOD
        
        term2 = (m * m) % MOD
        term2 = (term2 * Sn) % MOD
        
        total_sum = (term1 + term2) % MOD
        total_sum = (total_sum * W) % MOD
        
        return total_sum