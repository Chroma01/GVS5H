class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Total number of cells
        total_cells = m * n
        
        # If k < 2, no pairs exist, but constraints say k >= 2
        # We need C(total_cells - 2, k - 2)
        
        # Precompute factorials and inverse factorials for combinations
        # Max value needed is total_cells - 2, which is <= 10^5 - 2
        max_n = total_cells
        fact = [1] * (max_n + 1)
        inv_fact = [1] * (max_n + 1)
        
        for i in range(1, max_n + 1):
            fact[i] = (fact[i-1] * i) % MOD
            
        # Fermat's little theorem for modular inverse: a^(MOD-2) mod MOD
        inv_fact[max_n] = pow(fact[max_n], MOD - 2, MOD)
        for i in range(max_n - 1, -1, -1):
            inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD
            
        def comb(n, r):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = (inv_fact[r] * inv_fact[n-r]) % MOD
            return (num * den) % MOD
        
        # Number of arrangements that include a specific pair of cells
        # C(total_cells - 2, k - 2)
        arrangements_for_pair = comb(total_cells - 2, k - 2)
        
        # Sum of Manhattan distances between all unordered pairs of distinct cells
        # S = S_x + S_y
        # S_x = n * (sum of |i-j| for all pairs of rows 0..m-1)
        # S_y = m * (sum of |j-l| for all pairs of columns 0..n-1)
        
        # Formula for sum of |i-j| for i,j in 0..L-1, i < j: L*(L-1)*(L+1)//6
        # We compute this modulo MOD, so we need modular inverse of 6
        
        inv6 = pow(6, MOD - 2, MOD)
        
        def sum_abs_diff(L):
            # Returns L*(L-1)*(L+1)/6 mod MOD
            if L < 2:
                return 0
            res = (L % MOD) * ((L - 1) % MOD) % MOD
            res = res * ((L + 1) % MOD) % MOD
            res = res * inv6 % MOD
            return res
        
        sum_x_rows = sum_abs_diff(m)
        sum_y_cols = sum_abs_diff(n)
        
        S_x = (n % MOD) * sum_x_rows % MOD
        S_y = (m % MOD) * sum_y_cols % MOD
        
        total_distance_sum = (S_x + S_y) % MOD
        
        ans = (arrangements_for_pair * total_distance_sum) % MOD
        
        return ans