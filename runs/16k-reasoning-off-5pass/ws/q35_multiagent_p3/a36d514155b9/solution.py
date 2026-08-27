class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        # Total number of cells
        total_cells = m * n
        
        # If k < 2, no pairs exist, sum is 0. But constraints say k >= 2.
        if k < 2:
            return 0
            
        # Calculate C(total_cells - 2, k - 2) mod MOD
        # C(n, r) = n! / (r! * (n-r)!)
        # We need to compute this efficiently.
        # Since total_cells <= 10^5, we can compute factorials and inverse factorials.
        
        N = total_cells - 2
        R = k - 2
        
        if R < 0 or R > N:
            return 0
            
        # Compute C(N, R) mod MOD
        # We'll compute numerator and denominator separately and use modular inverse for denominator
        
        # Numerator: N * (N-1) * ... * (N-R+1)
        # Denominator: R!
        
        # To avoid computing full factorials if not needed, we can compute iteratively.
        # But since N <= 10^5, precomputing factorials is fine.
        
        # Let's compute factorials up to N
        fact = [1] * (N + 1)
        for i in range(2, N + 1):
            fact[i] = (fact[i-1] * i) % MOD
            
        # Modular inverse using Fermat's little theorem: a^(MOD-2) mod MOD
        def mod_inverse(a, mod):
            return pow(a, mod - 2, mod)
            
        denom = (fact[R] * fact[N - R]) % MOD
        comb = (fact[N] * mod_inverse(denom, MOD)) % MOD
        
        # Sum of absolute differences for 1D array of size L: L*(L^2 - 1)//6
        # For rows (size m): sum_x = m*(m^2 - 1)//6
        # For columns (size n): sum_y = n*(n^2 - 1)//6
        
        # We need to compute these modulo MOD. Division by 6 is multiplication by mod_inverse(6, MOD)
        inv6 = mod_inverse(6, MOD)
        
        sum_x = (m * (m*m - 1)) % MOD
        sum_x = (sum_x * inv6) % MOD
        
        sum_y = (n * (n*n - 1)) % MOD
        sum_y = (sum_y * inv6) % MOD
        
        # Total sum of Manhattan distances over all unordered pairs of cells:
        # = n * sum_x + m * sum_y
        # Because for each pair of rows, there are n columns, so the x-difference is counted n times.
        # Similarly, for each pair of columns, there are m rows, so the y-difference is counted m times.
        
        total_dist_sum = (n * sum_x + m * sum_y) % MOD
        
        # Final answer: comb * total_dist_sum
        ans = (comb * total_dist_sum) % MOD
        
        return ans