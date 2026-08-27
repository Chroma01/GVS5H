import math
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        n_masks = 1 << m
        
        # Precompute LCM for each subset of targets
        lcm_vals = [1] * n_masks
        for mask in range(1, n_masks):
            l = 1
            for i in range(m):
                if (mask >> i) & 1:
                    l = l * target[i] // math.gcd(l, target[i])
            lcm_vals[mask] = l
            
        # Precompute minimum increments for each subset
        # costs[mask] = min operations to make some n in nums a multiple of lcm_vals[mask]
        costs = [float('inf')] * n_masks
        for mask in range(1, n_masks):
            l = lcm_vals[mask]
            min_c = float('inf')
            for n in nums:
                c = (l - n % l) % l
                if c < min_c:
                    min_c = c
            costs[mask] = min_c
            
        # DP over bitmasks to find minimum total cost to cover all targets
        dp = [float('inf')] * n_masks
        dp[0] = 0
        
        for mask in range(1, n_masks):
            sub = mask
            while sub > 0:
                val = dp[mask ^ sub] + costs[sub]
                if val < dp[mask]:
                    dp[mask] = val
                sub = (sub - 1) & mask
                
        return dp[n_masks - 1]