import math
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        M = len(target)
        num_masks = 1 << M
        
        # Precompute LCM for each mask
        lcm_for_mask = [1] * num_masks
        for mask in range(1, num_masks):
            # Find the lowest set bit
            # We can iterate bits or use bit manipulation
            # Since M is small, simple iteration is fine
            l = 1
            for j in range(M):
                if mask & (1 << j):
                    l = math.lcm(l, target[j])
            lcm_for_mask[mask] = l
        
        # Precompute best_cost for each mask: min cost to make ANY num a multiple of LCM(mask)
        best_cost = [float('inf')] * num_masks
        
        for num in nums:
            for mask in range(1, num_masks):
                l = lcm_for_mask[mask]
                # Cost to make num a multiple of l
                rem = num % l
                if rem == 0:
                    cost = 0
                else:
                    cost = l - rem
                if cost < best_cost[mask]:
                    best_cost[mask] = cost
        
        # DP over masks
        dp = [float('inf')] * num_masks
        dp[0] = 0
        
        # Iterate over all masks
        for mask in range(1, num_masks):
            # Iterate over all submasks of mask
            s = mask
            while s > 0:
                if dp[mask ^ s] != float('inf') and best_cost[s] != float('inf'):
                    new_cost = dp[mask ^ s] + best_cost[s]
                    if new_cost < dp[mask]:
                        dp[mask] = new_cost
                s = (s - 1) & mask
        
        return dp[num_masks - 1]