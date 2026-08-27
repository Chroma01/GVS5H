from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full_mask = (1 << m) - 1
        
        # Precompute LCM for every non-empty subset of target
        lcm_vals = [0] * (1 << m)
        for mask in range(1, full_mask + 1):
            l = 1
            for i in range(m):
                if (mask >> i) & 1:
                    l = l // gcd(l, target[i]) * target[i]  # lcm(l, target[i])
            lcm_vals[mask] = l
        
        INF = float('inf')
        dp = [INF] * (1 << m)
        dp[0] = 0
        
        # Process each element in nums
        for x in nums:
            # Precompute the cost to make x a multiple of each non-empty subset
            costs = [0] * (1 << m)
            for mask in range(1, full_mask + 1):
                L = lcm_vals[mask]
                # Smallest multiple of L that is >= x
                mult = ((x + L - 1) // L) * L
                costs[mask] = mult - x
            
            # Update DP in reverse order so each element is used at most once
            for cmask in range(full_mask, -1, -1):
                if dp[cmask] == INF:
                    continue
                for mask in range(1, full_mask + 1):
                    new_mask = cmask | mask
                    new_cost = dp[cmask] + costs[mask]
                    if new_cost < dp[new_mask]:
                        dp[new_mask] = new_cost
        
        return int(dp[full_mask])