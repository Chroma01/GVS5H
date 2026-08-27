from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums: N[i] = sum(nums[0..i-1]), C[i] = sum(cost[0..i-1])
        N = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            N[i+1] = N[i] + nums[i]
            C[i+1] = C[i] + cost[i]
        
        # dp[i] = min cost to cover first i elements (0..i-1)
        # groups[i] = number of subarrays used in the optimal partition for dp[i]
        INF = float('inf')
        dp = [INF] * (n + 1)
        groups = [0] * (n + 1)
        dp[0] = 0
        groups[0] = 0
        
        for i in range(1, n + 1):
            for j in range(0, i):
                current_groups = groups[j] + 1
                # Cost of the subarray nums[j..i-1] as the current_groups-th subarray:
                # (global prefix sum of nums up to i-1 + k * current_groups) * (local cost sum)
                subarray_cost = (N[i] + k * current_groups) * (C[i] - C[j])
                total = dp[j] + subarray_cost
                if total < dp[i]:
                    dp[i] = total
                    groups[i] = current_groups
        
        return dp[n]