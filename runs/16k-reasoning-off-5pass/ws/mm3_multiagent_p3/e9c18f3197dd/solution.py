from math import gcd
from typing import List
from functools import reduce

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full_mask = (1 << m) - 1
        
        # Precompute LCM for every non-empty subset
        lcm_val = [0] * (1 << m)
        for mask in range(1, 1 << m):
            l = 1
            for i in range(m):
                if mask & (1 << i):
                    l = l * target[i] // gcd(l, target[i])
            lcm_val[mask] = l
        
        # DP over subsets: dp[mask] = min cost to cover exactly 'mask'
        INF = float('inf')
        dp = [INF] * (1 << m)
        dp[0] = 0
        
        for num in nums:
            # Process in decreasing order of mask for 0/1 knapsack style
            # We'll compute new values first to avoid using same num twice
            new_dp = dp[:]
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                # Try covering any non-empty subset of uncovered targets
                uncovered = full_mask ^ mask
                sub = uncovered
                while sub:
                    l = lcm_val[sub]
                    # Cost to raise num to next multiple of l
                    mult = (num + l - 1) // l
                    new_val = mult * l
                    cost = new_val - num
                    new_mask = mask | sub
                    if dp[mask] + cost < new_dp[new_mask]:
                        new_dp[new_mask] = dp[mask] + cost
                    sub = (sub - 1) & uncovered
            dp = new_dp
        
        return dp[full_mask]