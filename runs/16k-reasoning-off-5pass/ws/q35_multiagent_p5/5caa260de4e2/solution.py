class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums and cost
        # prefix_nums[i] = sum(nums[0]...nums[i-1])
        # prefix_cost[i] = sum(cost[0]...cost[i-1])
        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)
        
        for i in range(n):
            prefix_nums[i+1] = prefix_nums[i] + nums[i]
            prefix_cost[i+1] = prefix_cost[i] + cost[i]
            
        # dp[j][i] will store the min cost to partition first i elements into j subarrays
        # We use a 2D array. dp[j][i] corresponds to dp[i][j] in our derivation.
        # Dimensions: (n+1) x (n+1)
        # Initialize with infinity
        INF = float('inf')
        dp = [[INF] * (n + 1) for _ in range(n + 1)]
        
        # Base case: 0 elements partitioned into 0 subarrays has cost 0
        dp[0][0] = 0
        
        # Iterate over number of subarrays j from 1 to n
        for j in range(1, n + 1):
            # Iterate over number of elements i from j to n (at least j elements for j subarrays)
            for i in range(j, n + 1):
                # Iterate over the start index k of the last subarray
                # The last subarray is nums[k...i-1] (0-indexed in nums)
                # This subarray is the j-th subarray.
                # The previous partition covers nums[0...k-1] with j-1 subarrays.
                # So k ranges from j-1 to i-1.
                # In terms of prefix sums, the previous state is dp[j-1][k]
                # The current subarray sum_nums = prefix_nums[i] - prefix_nums[k]
                # The current subarray sum_cost = prefix_cost[i] - prefix_cost[k]
                
                # We want to compute:
                # dp[j][i] = min_{k from j-1 to i-1} ( dp[j-1][k] + (sum_nums + k*j) * sum_cost )
                
                best_val = INF
                
                # To optimize, we can iterate k and compute the cost
                # Since n is 1000, O(n^3) might be tight in Python.
                # Let's try to write it efficiently.
                
                p_nums_i = prefix_nums[i]
                p_cost_i = prefix_cost[i]
                
                for k in range(j-1, i):
                    prev_cost = dp[j-1][k]
                    if prev_cost == INF:
                        continue
                        
                    sum_nums = p_nums_i - prefix_nums[k]
                    sum_cost = p_cost_i - prefix_cost[k]
                    
                    current_subarray_cost = (sum_nums + k * j) * sum_cost
                    total = prev_cost + current_subarray_cost
                    
                    if total < best_val:
                        best_val = total
                
                dp[j][i] = best_val
                
        # The answer is the minimum cost to partition all n elements into any number of subarrays j from 1 to n
        ans = min(dp[j][n] for j in range(1, n + 1))
        
        return ans