class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums for nums and cost
        # S[i] is sum of nums[0...i-1]
        # C[i] is sum of cost[0...i-1]
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i+1] = S[i] + nums[i]
            C[i+1] = C[i] + cost[i]
            
        # dp[i][m] = min cost for prefix i with exactly m subarrays
        # Initialize with infinity
        # dp[i] is a list of size i+1, representing m from 0 to i
        # We only need m >= 1 for valid partitions, but keep index 0 for base case
        dp = [[float('inf')] * (i + 1) for i in range(n + 1)]
        dp[0][0] = 0
        
        # Iterate over the end of the prefix
        for i in range(1, n + 1):
            # Iterate over the number of subarrays m
            # m can be at most i (each element is its own subarray)
            for m in range(1, i + 1):
                # Iterate over the start of the last subarray j
                # The last subarray is nums[j...i-1]
                # It is the m-th subarray.
                # The previous part nums[0...j-1] must be partitioned into m-1 subarrays.
                # So j must be at least m-1 (since we need at least m-1 elements for m-1 subarrays)
                # and j < i.
                # We iterate j from m-1 to i-1.
                
                # To optimize, we can precompute the constant part for the current i, m
                # Cost of last subarray = (S[i] - S[j] + k * m) * (C[i] - C[j])
                #                       = S[i]*C[i] - S[i]*C[j] - S[j]*C[i] + S[j]*C[j] + k*m*C[i] - k*m*C[j]
                # We want to minimize: dp[j][m-1] + S[i]*C[i] - S[i]*C[j] - S[j]*C[i] + S[j]*C[j] + k*m*C[i] - k*m*C[j]
                # Group terms:
                # Constant for fixed i, m: S[i]*C[i] + k*m*C[i]
                # Variable part depending on j: dp[j][m-1] + S[j]*C[j] - C[j]*(S[i] + k*m) - S[j]*C[i]
                
                const_part = S[i] * C[i] + k * m * C[i]
                
                # We need min over j in [m-1, i-1] of:
                # dp[j][m-1] + S[j]*C[j] - C[j]*(S[i] + k*m) - S[j]*C[i]
                
                # Let val(j) = dp[j][m-1] + S[j]*C[j]
                # Then we minimize: val(j) - C[j]*(S[i] + k*m) - S[j]*C[i]
                
                # Since n is 1000, we can just loop.
                # Optimization: use local variables for speed
                
                best_prev = float('inf')
                
                # Precompute the coefficient for C[j]
                coeff_C = S[i] + k * m
                
                for j in range(m - 1, i):
                    prev_cost = dp[j][m-1]
                    if prev_cost == float('inf'):
                        continue
                    
                    # Calculate the cost contribution from j
                    # term = prev_cost + S[j]*C[j] - C[j]*coeff_C - S[j]*C[i]
                    term = prev_cost + S[j] * C[j] - C[j] * coeff_C - S[j] * C[i]
                    
                    if term < best_prev:
                        best_prev = term
                
                if best_prev != float('inf'):
                    dp[i][m] = best_prev + const_part
                    
        # The answer is the min cost for prefix n with any number of subarrays m >= 1
        return min(dp[n][1:])