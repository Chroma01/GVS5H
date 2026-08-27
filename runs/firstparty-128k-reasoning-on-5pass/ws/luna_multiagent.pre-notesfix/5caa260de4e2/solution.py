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

        for end in range(1, n + 1):
            segment_nums_sum = prefix_nums[end]
            best = inf

            for start in range(end):
                segment_cost_sum = prefix_cost[end] - prefix_cost[start]

                current = (
                    dp[start]
                    + segment_nums_sum * segment_cost_sum
                )

                # A segment starting at `start > 0` follows a cut.
                # That cut increases the order index of every later element.
                if start > 0:
                    current += k * (total_cost - prefix_cost[start])

                if current < best:
                    best = current

            dp[end] = best

        # Every element contributes the base order-index term k once.
        return dp[n] + k * total_cost