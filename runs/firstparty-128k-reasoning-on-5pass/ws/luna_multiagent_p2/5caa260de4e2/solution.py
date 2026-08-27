from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]

        total_cost = prefix_cost[n]
        inf = 10**30
        dp = [inf] * (n + 1)
        dp[0] = 0

        # dp[i] is the minimum transformed cost for nums[0:i].
        for i in range(1, n + 1):
            current_prefix_nums = prefix_nums[i]

            for t in range(i):
                segment_cost = prefix_cost[i] - prefix_cost[t]

                # t == 0 is the virtual initial boundary and has no penalty.
                boundary_penalty = 0
                if t > 0:
                    boundary_penalty = k * (total_cost - prefix_cost[t])

                candidate = (
                    dp[t]
                    + current_prefix_nums * segment_cost
                    + boundary_penalty
                )
                if candidate < dp[i]:
                    dp[i] = candidate

        # Add the constant k * total_cost from the order-term transformation.
        return dp[n] + k * total_cost