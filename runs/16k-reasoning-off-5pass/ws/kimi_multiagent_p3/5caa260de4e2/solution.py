from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        S = [0] * (n + 1)
        C = [0] * (n + 1)
        for i in range(n):
            S[i + 1] = S[i] + nums[i]
            C[i + 1] = C[i] + cost[i]

        totalC = C[n]
        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0

        # dp[i] = min over j < i of:
        #   dp[j] + (S[i] + k) * (C[i] - C[j]) + k * (totalC - C[j])
        # The k*(totalC - C[j]) term is the surcharge for making a cut at j:
        # every later segment's index increases by 1, adding k * (sum of cost
        # over all later elements). A fictitious cut at j=0 adds k*totalC once
        # for every partition, so we subtract it at the end.
        for i in range(1, n + 1):
            Si_k = S[i] + k
            Ci = C[i]
            best = INF
            for j in range(i):
                val = dp[j] + Si_k * (Ci - C[j]) + k * (totalC - C[j])
                if val < best:
                    best = val
            dp[i] = best

        return dp[n] - k * totalC