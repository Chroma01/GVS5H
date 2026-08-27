class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Helper to calculate modular inverse using Fermat's Little Theorem
        def modInverse(a, m):
            return pow(a, m - 2, m)
        
        # Helper to calculate nCr % MOD
        def nCr_mod(n, r, mod):
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
        
        # Calculate the number of ways to choose the remaining k-2 pieces
        # Total cells N = m * n
        N = m * n
        ways = nCr_mod(N - 2, k - 2, MOD)
        
        # Function to calculate sum of distances for a 1D line of length L
        # Sum_{1<=i<j<=L} (j-i) = Sum_{d=1}^{L-1} d * (L-d)
        # = L * Sum(d) - Sum(d^2)
        # = L * (L-1)*L/2 - (L-1)*L*(2L-1)/6
        def calc_1D_sum(L):
            if L < 2:
                return 0
            # Calculate L * (L-1) * L / 2
            term1 = (L * (L - 1)) % MOD
            term1 = (term1 * L) % MOD
            term1 = (term1 * modInverse(2, MOD)) % MOD
            
            # Calculate (L-1) * L * (2L-1) / 6
            term2 = (L - 1) % MOD
            term2 = (term2 * L) % MOD
            term2 = (term2 * ((2 * L - 1) % MOD)) % MOD
            term2 = (term2 * modInverse(6, MOD)) % MOD
            
            return (term1 - term2 + MOD) % MOD
        
        # Calculate sum of horizontal distances
        # For each pair of columns with distance d, there are m * m pairs of cells
        sum_horiz = (calc_1D_sum(n) * (m * m % MOD)) % MOD
        
        # Calculate sum of vertical distances
        # For each pair of rows with distance d, there are n * n pairs of cells
        sum_vert = (calc_1D_sum(m) * (n * n % MOD)) % MOD
        
        # Total sum of distances over all pairs of cells in the grid
        total_dist_sum = (sum_horiz + sum_vert) % MOD
        
        # Final answer is total_dist_sum * ways
        return (total_dist_sum * ways) % MOD