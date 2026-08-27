class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Precompute factorials and inverse factorials for combinations
        N = m * n
        limit = N + 5
        fact = [1] * limit
        inv = [1] * limit
        
        for i in range(1, limit):
            fact[i] = (fact[i-1] * i) % MOD
            
        inv[limit-1] = pow(fact[limit-1], MOD - 2, MOD)
        for i in range(limit-2, -1, -1):
            inv[i] = (inv[i+1] * (i+1)) % MOD
            
        def nCr_mod(n, r):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = (inv[r] * inv[n-r]) % MOD
            return (num * den) % MOD
        
        # Helper to calculate sum of |i - j| for all unordered pairs in a 1D array of length L
        # The array is 0-indexed: 0, 1, ..., L-1
        # Returns sum_{0 <= i < j < L} (j - i)
        def sum_dist_1D(L: int) -> int:
            if L < 2:
                return 0
            
            # We need sum_{d=1}^{L-1} d * (number of pairs with distance d)
            # Number of pairs with distance d is (L - d)
            # Total sum = sum_{d=1}^{L-1} d * (L - d)
            #           = L * sum(d) - sum(d^2) for d from 1 to L-1
            # sum(d) = (L-1)*L/2
            # sum(d^2) = (L-1)*L*(2L-1)/6
            
            L_mod = L % MOD
            
            # Calculate sum of d from 1 to L-1
            sum_d = (L_mod * (L_mod - 1) // 2) % MOD
            
            # Calculate sum of d^2 from 1 to L-1
            # Formula: n(n+1)(2n+1)/6 where n = L-1
            # Here n = L-1, so term is (L-1)*L*(2(L-1)+1)/6 = (L-1)*L*(2L-1)/6
            sum_d2 = (L_mod * (L_mod - 1) * (2 * L_mod - 1) // 6) % MOD
            
            total = (L_mod * sum_d - sum_d2) % MOD
            return total
        
        # Calculate contribution from X dimension
        # For X dimension, we have m possible values for x (0 to m-1).
        # For each pair of x-coordinates (i, j) with i < j, the distance is (j - i).
        # There are n * n pairs of cells that have these specific x-coordinates (since y can be anything).
        # So the sum of |x_A - x_B| over all unordered pairs of cells {A, B} is:
        # sum_{0 <= i < j < m} (j - i) * (n * n)
        # = sum_dist_1D(m) * n * n
        
        S_x = sum_dist_1D(m)
        S_y = sum_dist_1D(n)
        
        # Number of ways to choose the remaining k-2 cells from the remaining N-2 cells
        ways = nCr_mod(N - 2, k - 2)
        
        # Total sum = ways * (Sum_X + Sum_Y)
        # Sum_X = S_x * n * n
        # Sum_Y = S_y * m * m
        
        term_x = (S_x * n % MOD * n % MOD) % MOD
        term_y = (S_y * m % MOD * m % MOD) % MOD
        
        total = (ways * (term_x + term_y)) % MOD
        
        return total