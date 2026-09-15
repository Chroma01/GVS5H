from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums:
        # P[j] = nums[0] + ... + nums[j-1]
        # C[j] = cost[0] + ... + cost[j-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        total_cost = C[n]
        INF = 10**30

        # dp[j] = minimum transformed cost to reach boundary j.
        # Boundary j means the previous subarray ended just before index j.
        dp = [0] + [INF] * n

        for j in range(1, n + 1):
            pj = P[j]
            cj = C[j]
            best = INF

            for i in range(j):
                ci = C[i]
                # Edge i -> j:
                # P[j] * (C[j] - C[i]) + k * (C[n] - C[i])
                val = dp[i] + pj * (cj - ci) + k * (total_cost - ci)
                if val < best:
                    best = val

            dp[j] = best

        return dp[n]