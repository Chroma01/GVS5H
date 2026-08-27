from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]

        total_cost_sum = prefix_cost[n]
        inf = 10**30

        # dp[r] is the minimum of:
        #   sum of segment base costs
        #   + k * (total_cost_sum - prefix_cost[p])
        #     for every internal cut p
        # over partitions of nums[0:r].
        dp = [inf] * (n + 1)
        dp[0] = 0

        for r in range(1, n + 1):
            segment_nums_sum = prefix_nums[r]

            for l in range(r):
                segment_cost_sum = prefix_cost[r] - prefix_cost[l]
                segment_base_cost = segment_nums_sum * segment_cost_sum

                cut_penalty = 0
                if l > 0:
                    cut_penalty = k * (total_cost_sum - prefix_cost[l])

                candidate = dp[l] + segment_base_cost + cut_penalty
                if candidate < dp[r]:
                    dp[r] = candidate

        # The first term k * total_cost_sum is common to every partition.
        return dp[n] + k * total_cost_sum