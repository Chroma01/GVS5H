from typing import List

class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)
        # 1-indexed prefix sums: A[t] = nums[0..t-1], B[t] = cost[0..t-1]
        A = [0] * (n + 1)
        B = [0] * (n + 1)
        for i in range(n):
            A[i + 1] = A[i] + nums[i]
            B[i + 1] = B[i] + cost[i]

        Bn = B[n]
        INF = float('inf')
        # dp[j] = min over segment split of first j elements of:
        #   sum_segments A[r+1]*(B[r+1]-B[l])  +  k * (sum of cut penalties)
        # where a cut after prefix index p>0 contributes k*(B[n]-B[p]).
        dp = [INF] * (n + 1)
        dp[0] = 0

        for j in range(1, n + 1):
            Aj = A[j]
            best = INF
            # last segment covers elements p..j-1 (prefix indices p..j)
            for p in range(j):
                val = dp[p] + Aj * (B[j] - B[p])
                if p > 0:
                    val += k * (Bn - B[p])   # cut penalty before this segment
                if val < best:
                    best = val
            dp[j] = best

        # add back the base k * totalCost term
        return dp[n] + k * Bn