from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums: P[j] = nums[0] + ... + nums[j-1]
        #               C[j] = cost[0] + ... + cost[j-1]
        P = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(1, n + 1):
            P[i] = P[i - 1] + nums[i - 1]
            C[i] = C[i - 1] + cost[i - 1]

        const = k * C[n]
        INF = 10**30
        dp = [0] * (n + 1)

        for j in range(1, n + 1):
            pj = P[j]
            cj = C[j]
            best = INF
            for t in range(j):
                val = dp[t] + pj * (cj - C[t]) - k * C[t]
                if val < best:
                    best = val
            dp[j] = best + const

        return dp[n]