from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums:
        # P[i] = nums[0] + ... + nums[i-1]
        # C[i] = cost[0] + ... + cost[i-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)

        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        total_cost = C[n]

        # dp[i] = minimum transformed cost for the first i elements,
        # including the cut penalty after i if i is an internal cut.
        INF = 10**30
        dp = [INF] * (n + 1)
        dp[0] = 0

        for i in range(1, n + 1):
            pi = P[i]
            ci = C[i]

            best = INF
            for p in range(i):
                # Segment (p, i] contributes:
                # P[i] * (C[i] - C[p])
                value = dp[p] + pi * (ci - C[p])
                if value < best:
                    best = value

            # If i < n, choosing i as a cut increases the index of all
            # later segments by 1, adding k * (total_cost - C[i]).
            if i < n:
                best += k * (total_cost - ci)

            dp[i] = best

        # Every valid partition has a mandatory base contribution k * total_cost.
        return dp[n] + k * total_cost