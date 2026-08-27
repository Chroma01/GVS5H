class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Total number of cells
        total_cells = m * n
        
        # We need to compute C(total_cells - 2, k - 2) mod MOD
        # Since total_cells <= 10^5, we can compute factorials up to 10^5
        
        N = total_cells - 2
        K = k - 2
        
        # If K < 0 or K > N, then C(N, K) = 0, but constraints say k >= 2 and k <= m*n, so K >= 0 and K <= N
        # Compute factorials and inverse factorials for combinations
        max_val = total_cells  # up to 10^5
        
        fact = [1] * (max_val + 1)
        inv_fact = [1] * (max_val + 1)
        
        for i in range(1, max_val + 1):
            fact[i] = (fact[i-1] * i) % MOD
            
        # Fermat's little theorem for modular inverse: a^(MOD-2) mod MOD
        inv_fact[max_val] = pow(fact[max_val], MOD - 2, MOD)
        for i in range(max_val - 1, -1, -1):
            inv_fact[i] = (inv_fact[i+1] * (i + 1)) % MOD
            
        def comb(n, r):
            if r < 0 or r > n:
                return 0
            num = fact[n]
            den = (inv_fact[r] * inv_fact[n-r]) % MOD
            return (num * den) % MOD
        
        # Number of arrangements containing any specific pair of cells
        arrangements_with_pair = comb(N, K)
        
        # Compute sum of Manhattan distances over all unordered pairs of distinct cells
        # Sum = n^2 * S_rows + m^2 * S_cols
        # S_rows = sum_{0<=i<j<m} (j - i) = m*(m^2 - 1)//6
        # S_cols = sum_{0<=i<j<n} (j - i) = n*(n^2 - 1)//6
        
        # We need to compute these sums modulo MOD, but the division by 6 requires modular inverse
        inv6 = pow(6, MOD - 2, MOD)
        
        S_rows = (m * (m*m - 1)) % MOD
        S_rows = (S_rows * inv6) % MOD
        
        S_cols = (n * (n*n - 1)) % MOD
        S_cols = (S_cols * inv6) % MOD
        
        # Total sum of Manhattan distances
        total_dist_sum = (n*n % MOD * S_rows) % MOD
        total_dist_sum = (total_dist_sum + m*m % MOD * S_cols) % MOD
        
        # Final answer
        ans = (arrangements_with_pair * total_dist_sum) % MOD
        
        return ans