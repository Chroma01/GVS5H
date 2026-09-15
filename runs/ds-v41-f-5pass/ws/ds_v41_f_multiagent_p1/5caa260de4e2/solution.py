from typing import List


class Solution:
    def minimumCost(self, nums: List[int], cost: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums
        preN = [0] * n
        preC = [0] * n
        acc = 0
        for i in range(n):
            acc += nums[i]
            preN[i] = acc
        acc = 0
        for i in range(n):
            acc += cost[i]
            preC[i] = acc
        totalCost = preC[-1]

        # dp[i] = min segmentation value for prefix nums[0..i-1], including the
        # k-charges for every group start l>0 inside that prefix.
        # Group start at l (l>0) adds k * (cost from l to n-1) = k*(totalCost - preC[l-1]).
        dp = [0] * (n + 1)  # dp[0] corresponds to the empty prefix (dp[-1] = 0)

        for r in range(n):
            nr = preN[r]
            cr = preC[r]
            best = None
            for l in range(r + 1):  # last group is nums[l..r]
                if l == 0:
                    val = nr * cr  # first group: no k-charge here
                else:
                    pc = preC[l - 1]
                    val = dp[l] + nr * (cr - pc) + k * (totalCost - pc)
                if best is None or val < best:
                    best = val
            dp[r + 1] = best

        # The very first group contributes the base k*totalCost term.
        return dp[n] + k * totalCost