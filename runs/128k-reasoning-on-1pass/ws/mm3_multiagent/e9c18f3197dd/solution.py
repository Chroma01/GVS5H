from typing import List
import math

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        max_mask = 1 << k
        # precompute LCM for each non‑empty mask
        lcms = [1] * max_mask
        for mask in range(1, max_mask):
            l = 1
            for i in range(k):
                if mask >> i & 1:
                    l = l // math.gcd(l, target[i]) * target[i]
            lcms[mask] = l
        INF = 10**30
        dp = [INF] * max_mask
        dp[0] = 0
        for x in nums:
            # cost to raise x to the next multiple of L for each mask
            # mask 0 -> cost 0 (do nothing)
            costs = [0] * max_mask
            for mask in range(1, max_mask):
                L = lcms[mask]
                # ceil(x / L) * L - x
                costs[mask] = ((x + L - 1) // L) * L - x
            # DP transition
            ndp = [INF] * max_mask
            for mask in range(max_mask):
                cur = dp[mask]
                if cur == INF:
                    continue
                # try to assign this element to any subset sub
                for sub in range(max_mask):
                    new_mask = mask | sub
                    new_cost = cur + costs[sub]
                    if new_cost < ndp[new_mask]:
                        ndp[new_mask] = new_cost
            dp = ndp
        full_mask = max_mask - 1
        return dp[full_mask]