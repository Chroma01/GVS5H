from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i in range(1, n + 1):
            prefix_nums[i] = prefix_nums[i - 1] + nums[i - 1]
            prefix_cost[i] = prefix_cost[i - 1] + cost[i - 1]

        total_weight = prefix_cost[n]
        inf = 10**30
        dp = [inf] * (n + 1)
        dp[0] = 0

        # dp[i] excludes the universal base term k * total_weight.
        # A transition p -> i creates segment [p, i).
        for i in range(1, n + 1):
            current_num_sum = prefix_nums[i]
            for p in range(i):
                segment_cost = current_num_sum * (prefix_cost[i] - prefix_cost[p])

                # A cut after p (p > 0) increases the segment number of
                # every later element by one.
                cut_cost = 0 if p == 0 else k * (total_weight - prefix_cost[p])

                candidate = dp[p] + segment_cost + cut_cost
                if candidate < dp[i]:
                    dp[i] = candidate

        return dp[n] + k * total_weight