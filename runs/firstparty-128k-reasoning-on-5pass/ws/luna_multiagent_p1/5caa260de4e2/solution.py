from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i in range(n):
            prefix_nums[i + 1] = prefix_nums[i] + nums[i]
            prefix_cost[i + 1] = prefix_cost[i] + cost[i]

        # dp[l] is the minimum cost for partitioning nums[l:],
        # when the first subarray in this suffix has order 1.
        dp = [0] * (n + 1)

        for l in range(n - 1, -1, -1):
            best = 10**30

            for end in range(l + 1, n + 1):
                segment_cost_sum = prefix_cost[end] - prefix_cost[l]
                suffix_cost_sum = prefix_cost[n] - prefix_cost[end]

                first_segment_cost = (
                    prefix_nums[end] + k
                ) * segment_cost_sum

                # Every segment in the suffix increases its order by one
                # when the current segment is prepended.
                candidate = (
                    first_segment_cost
                    + dp[end]
                    + k * suffix_cost_sum
                )

                best = min(best, candidate)

            dp[l] = best

        return dp[0]