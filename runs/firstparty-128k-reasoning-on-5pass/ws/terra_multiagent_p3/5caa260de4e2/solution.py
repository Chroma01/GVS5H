from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        prefix_nums = [0] * (n + 1)
        prefix_cost = [0] * (n + 1)

        for i in range(1, n + 1):
            prefix_nums[i] = prefix_nums[i - 1] + nums[i - 1]
            prefix_cost[i] = prefix_cost[i - 1] + cost[i - 1]

        total_cost = prefix_cost[n]
        inf = 10**30

        # dp[i] = minimum cost excluding the unavoidable k * total_cost term,
        # for partitioning nums[0:i].
        dp = [inf] * (n + 1)
        dp[0] = 0

        for i in range(1, n + 1):
            for j in range(i):
                # Final segment is nums[j:i].
                segment_cost = prefix_cost[i] - prefix_cost[j]

                # Starting a segment at j > 0 means a cut after j - 1.
                # That cut raises the segment order of every remaining element.
                cut_surcharge = 0 if j == 0 else k * (total_cost - prefix_cost[j])

                dp[i] = min(
                    dp[i],
                    dp[j] + prefix_nums[i] * segment_cost + cut_surcharge
                )

        return dp[n] + k * total_cost