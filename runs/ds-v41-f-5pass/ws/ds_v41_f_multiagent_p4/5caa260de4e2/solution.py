from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums: Pn[r] = nums[0]+...+nums[r-1], Pc[r] = cost[0]+...+cost[r-1]
        Pn = [0] * (n + 1)
        Pc = [0] * (n + 1)
        for i in range(n):
            Pn[i + 1] = Pn[i] + nums[i]
            Pc[i + 1] = Pc[i] + cost[i]

        # Telescoped constant: every segment (edge) contributes +k*Pc[n].
        K = k * Pc[n]

        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0

        # dp[r] = min_{j<r} dp[j] + Pn[r]*(Pc[r]-Pc[j]) + K - k*Pc[j]
        # Edge j->r corresponds to segment j+1..r (1-based).
        for r in range(1, n + 1):
            Pnr = Pn[r]
            Pcr = Pc[r]
            best = INF
            for j in range(r):
                val = dp[j] + Pnr * (Pcr - Pc[j]) + K - k * Pc[j]
                if val < best:
                    best = val
            dp[r] = best

        return dp[n]