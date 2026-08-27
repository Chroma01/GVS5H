class Solution:
    def distanceSum(self, m: int, n: int, k: int) -> int:
        MOD = 10**9 + 7
        
        N = m * n
        
        # If k < 2, no pairs exist, but constraints say k >= 2
        if k < 2:
            return 0
        
        # Precompute factorials and inverse factorials for combinations
        # We need up to N
        max_val = N
        fact = [1] * (max_val + 1)
        inv_fact = [1] * (max_val + 1)
        
        for i in range(1, max_val + 1):
            fact[i] = fact[i-1] * i % MOD
            
        inv_fact[max_val] = pow(fact[max_val], MOD - 2, MOD)
        for i in range(max_val - 1, -1, -1):
            inv_fact[i] = inv_fact[i+1] * (i + 1) % MOD
            
        def comb(n, k):
            if k < 0 or k > n:
                return 0
            num = fact[n]
            den = inv_fact[k] * inv_fact[n-k] % MOD
            return num * den % MOD
        
        # Calculate C(N-2, k-2)
        ways = comb(N - 2, k - 2)
        
        # Calculate sum of |x_i - x_j| for all pairs of cells
        # X coordinates: each row i (0 to m-1) has n cells with x=i
        # So the list of x-coordinates is: [0]*n, [1]*n, ..., [m-1]*n
        # We can compute the sum of absolute differences efficiently.
        # For a sorted array A, sum_{i<j} (A[j] - A[i]) = sum_{i=0}^{N-1} A[i] * (2*i - N + 1)
        # But here we have groups. Let's compute directly using the structure.
        
        # Sum for x-coordinates:
        # The x-coordinates are: n copies of 0, n copies of 1, ..., n copies of m-1
        # Let's create the full list? N <= 10^5, so it's feasible.
        x_coords = []
        for i in range(m):
            x_coords.extend([i] * n)
        
        # Sum of absolute differences for x_coords
        # Sort is already done
        sum_x = 0
        # Using the formula: for sorted array A, sum_{i<j} (A[j]-A[i]) = sum_{i=0}^{N-1} A[i]*(2*i - N + 1)
        # But note: this formula gives the sum for all pairs (i, j) with i < j.
        # Let's verify: 
        # For A = [a0, a1, ..., a_{N-1}], 
        # sum_{i<j} (a_j - a_i) = sum_{j=0}^{N-1} a_j * j - sum_{i=0}^{N-1} a_i * (N - 1 - i)
        # = sum_{i=0}^{N-1} a_i * (i - (N - 1 - i)) = sum_{i=0}^{N-1} a_i * (2*i - N + 1)
        for i, val in enumerate(x_coords):
            sum_x = (sum_x + val * (2 * i - N + 1)) % MOD
            
        # Sum for y-coordinates:
        # The y-coordinates are: for each column j (0 to n-1), there are m cells with y=j
        y_coords = []
        for j in range(n):
            y_coords.extend([j] * m)
            
        sum_y = 0
        for i, val in enumerate(y_coords):
            sum_y = (sum_y + val * (2 * i - N + 1)) % MOD
            
        total_dist_sum = (sum_x + sum_y) % MOD
        
        result = total_dist_sum * ways % MOD
        
        return result