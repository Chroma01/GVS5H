from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        pref_nums = [0] * (n + 1)
        pref_cost = [0] * (n + 1)

        for i in range(1, n + 1):
            pref_nums[i] = pref_nums[i - 1] + nums[i - 1]
            pref_cost[i] = pref_cost[i - 1] + cost[i - 1]

        total_cost_sum = pref_cost[n]
        dp = [0] + [10**30] * n

        # dp[i] is the transformed minimum for partitions of nums[:i].
        # Each group contributes k * total_cost_sum, and a cut after j
        # contributes a refund of k * pref_cost[j].
        for i in range(1, n + 1):
            best = 10**30
            for j in range(i):
                candidate = (
                    dp[j]
                    + pref_nums[i] * (pref_cost[i] - pref_cost[j])
                    + k * total_cost_sum
                    - k * pref_cost[j]
                )
                if candidate < best:
                    best = candidate
            dp[i] = best

        return dp[n]