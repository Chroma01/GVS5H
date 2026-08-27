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
        dp = [0] + [10**30] * n

        for end in range(1, n + 1):
            best = prefix_nums[end] * prefix_cost[end]

            for prev in range(1, end):
                candidate = (
                    dp[prev]
                    + prefix_nums[end] * (prefix_cost[end] - prefix_cost[prev])
                    + k * (total_cost_sum - prefix_cost[prev])
                )
                if candidate < best:
                    best = candidate

            dp[end] = best

        return dp[n] + k * total_cost_sum