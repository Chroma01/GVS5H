from math import gcd
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full_mask = (1 << m) - 1
        
        # Precompute lcm for every non-empty subset of target
        sub_lcm = [0] * (1 << m)
        for mask in range(1, 1 << m):
            vals = [target[i] for i in range(m) if mask & (1 << i)]
            l = 1
            for v in vals:
                l = l * v // gcd(l, v)
            sub_lcm[mask] = l
        
        INF = float('inf')
        dp = [INF] * (1 << m)
        dp[0] = 0
        
        for n in nums:
            # Cost to make n a multiple of each subset's lcm
            costs = [0] * (1 << m)
            for mask in range(1, 1 << m):
                costs[mask] = (-n) % sub_lcm[mask]
            
            new_dp = dp[:]  # option: skip this n
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                base = dp[mask]
                for sub in range(1, 1 << m):
                    new_mask = mask | sub
                    new_cost = base + costs[sub]
                    if new_cost < new_dp[new_mask]:
                        new_dp[new_mask] = new_cost
            dp = new_dp
        
        return dp[full_mask]