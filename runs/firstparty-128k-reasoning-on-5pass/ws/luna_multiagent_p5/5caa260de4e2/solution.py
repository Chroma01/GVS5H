from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums for nums and cost.
        pref_nums = [0] * (n + 1)
        pref_cost = [0] * (n + 1)

        for i in range(n):
            pref_nums[i + 1] = pref_nums[i] + nums[i]
            pref_cost[i + 1] = pref_cost[i] + cost[i]

        total_cost = pref_cost[n]
        inf = 10**30
        dp = [inf] * (n + 1)
        dp[0] = 0

        # dp[r] is the minimum transformed cost for nums[0:r].
        for r in range(1, n + 1):
            for l in range(r):
                segment_cost = pref_cost[r] - pref_cost[l]
                segment_base = pref_nums[r] * segment_cost

                # l > 0 means that a cut is made at boundary l.
                cut_penalty = 0
                if l > 0:
                    cut_penalty = k * (total_cost - pref_cost[l])

                dp[r] = min(
                    dp[r],
                    dp[l] + segment_base + cut_penalty
                )

        # The common k * total_cost contribution is paid once.
        return dp[n] + k * total_cost