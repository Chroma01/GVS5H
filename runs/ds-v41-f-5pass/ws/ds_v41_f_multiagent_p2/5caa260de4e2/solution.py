from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # 1-indexed prefix sums
        P = [0] * (n + 1)  # P[i] = nums[0] + ... + nums[i-1]
        C = [0] * (n + 1)  # C[i] = cost[0] + ... + cost[i-1]
        for i in range(n):
            P[i + 1] = P[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        Cn = C[n]
        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0

        # dp[i] = min cost to partition the first i elements (0-indexed 0..i-1)
        # Adding a subarray covering j..i-1 (1-indexed j+1..i):
        #   contribution = P[i]*(C[i]-C[j]) + k*(C[n]-C[j])
        for i in range(1, n + 1):
            Pi = P[i]
            Ci = C[i]
            best = INF
            for j in range(i):
                val = dp[j] + Pi * (Ci - C[j]) + k * (Cn - C[j])
                if val < best:
                    best = val
            dp[i] = best

        return dp[n]