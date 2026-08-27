from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        
        # Prefix sums for nums and cost arrays
        p_nums = [0] * (n + 1)
        p_cost = [0] * (n + 1)
        for i in range(n):
            p_nums[i+1] = p_nums[i] + nums[i]
            p_cost[i+1] = p_cost[i] + cost[i]
            
        # dp[i] will store a tuple: (min_cost, num_partitions)
        # min_cost: minimum cost to partition the first i elements
        # num_partitions: the number of partitions used to achieve min_cost
        dp = [(float('inf'), 0)] * (n + 1)
        dp[0] = (0, 0)
        
        for i in range(1, n + 1):
            for j in range(i):
                prev_cost, prev_partitions = dp[j]
                
                # The subarray nums[j..i-1] is the (prev_partitions + 1)-th subarray
                current_partitions = prev_partitions + 1
                
                # Calculate the cost of this new subarray
                subarray_cost = (p_nums[i] + k * current_partitions) * (p_cost[i] - p_cost[j])
                
                total_cost = prev_cost + subarray_cost
                
                if total_cost < dp[i][0]:
                    dp[i] = (total_cost, current_partitions)
                    
        return dp[n][0]