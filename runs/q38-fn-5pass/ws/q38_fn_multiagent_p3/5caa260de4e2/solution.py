from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums:
        # pref_nums[b] = nums[0] + ... + nums[b-1]
        # pref_cost[b] = cost[0] + ... + cost[b-1]
        pref_nums = [0] * (n + 1)
        pref_cost = [0] * (n + 1)

        for i in range(n):
            pref_nums[i + 1] = pref_nums[i] + nums[i]
            pref_cost[i + 1] = pref_cost[i] + cost[i]

        total_cost = pref_cost[n]

        # dp[b] is the minimum transformed path cost to reach position b.
        # For a cut from a to b, the transformed edge weight is:
        # P[b] * (C[b] - C[a]) + k * (C[n] - C[a])
        #
        # For fixed b, this transition can be written as:
        # P[b] * C[b] + k * C[n] + dp[a] - (P[b] + k) * C[a]
        INF = 10**30
        dp = [INF] * (n + 1)
        dp[0] = 0

        pc = pref_cost
        d = dp

        for b in range(1, n + 1):
            pb = pref_nums[b]
            cb = pc[b]

            base = pb * cb + k * total_cost
            slope = pb + k

            best = INF
            for a in range(b):
                val = d[a] - slope * pc[a]
                if val < best:
                    best = val

            d[b] = base + best

        return d[n]