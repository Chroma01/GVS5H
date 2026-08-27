from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i in range(1, n + 1):
            prefix_nums[i] = prefix_nums[i - 1] + nums[i - 1]
            prefix_cost[i] = prefix_cost[i - 1] + cost[i - 1]

        total_cost_sum = prefix_cost[n]
        inf = 10**30
        dp = [inf] * (n + 1)
        dp[0] = 0

        # dp[i] excludes the fixed base contribution k * total_cost_sum.
        for i in range(1, n + 1):
            p_i = prefix_nums[i]
            c_i = prefix_cost[i]

            # One segment containing elements 0 through i - 1.
            dp[i] = p_i * c_i

            # Final segment starts after a cut following element j - 1.
            for j in range(1, i):
                candidate = (
                    dp[j]
                    + p_i * (c_i - prefix_cost[j])
                    + k * (total_cost_sum - prefix_cost[j])
                )
                if candidate < dp[i]:
                    dp[i] = candidate

        return dp[n] + k * total_cost_sum