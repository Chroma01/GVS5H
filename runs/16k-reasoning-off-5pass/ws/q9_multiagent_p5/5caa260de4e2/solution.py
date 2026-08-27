from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Precompute prefix sums for nums and cost
        # prefix_nums[i] stores sum(nums[0]...nums[i-1])
        # prefix_cost[i] stores sum(cost[0]...cost[i-1])
        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)
        
        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]
            
        # dp[i] represents the minimum cost to partition the prefix nums[0...i-1]
        # Initialize with a large number, dp[0] is 0 (cost of empty partition)
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        # Iterate through all possible end points of the last subarray
        for i in range(1, n + 1):
            # Iterate through all possible start points of the last subarray
            # The last subarray is nums[j...i-1]
            for j in range(i):
                # The number of subarrays in the partition ending at i is (i - j)
                # Let this be the index of the current subarray (1-based)
                subarray_index = i - j
                
                # Cost of the current subarray:
                # (Sum(nums[0]...nums[i-1]) + k * subarray_index) * (Sum(cost[j]...cost[i-1]))
                # Note: The problem states the first term uses nums[0]...nums[r] (prefix sum up to end of subarray)
                
                sum_nums_prefix = prefix_nums[i]
                sum_cost_segment = prefix_cost[i] - prefix_cost[j]
                
                current_subarray_cost = (sum_nums_prefix + k * subarray_index) * sum_cost_segment
                
                if dp[j] + current_subarray_cost < dp[i]:
                    dp[i] = dp[j] + current_subarray_cost
                    
        return dp[n]