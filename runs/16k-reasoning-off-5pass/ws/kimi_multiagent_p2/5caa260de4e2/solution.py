from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums: SN[i] = sum(nums[0..i-1]), SC[i] = sum(cost[0..i-1])
        SN = [0] * (n + 1)
        SC = [0] * (n + 1)
        for idx in range(n):
            SN[idx + 1] = SN[idx] + nums[idx]
            SC[idx + 1] = SC[idx] + cost[idx]

        totalCost = SC[n]
        INF = float('inf')
        # dp[j] = minimum total cost to partition suffix nums[j..n-1],
        # where the first subarray of this suffix has index 1.
        dp = [INF] * (n + 1)
        dp[n] = 0

        for j in range(n - 1, -1, -1):
            best = INF
            scj = SC[j]
            # Choose the first subarray nums[j..i-1]; the rest (i..n-1) is
            # partitioned optimally, but all its subarray indices shift by +1,
            # adding k * (sum of cost[i..n-1]) to the total.
            for i in range(j + 1, n + 1):
                cand = (SN[i] + k) * (SC[i] - scj) + dp[i] + k * (totalCost - SC[i])
                if cand < best:
                    best = cand
            dp[j] = best

        return dp[0]