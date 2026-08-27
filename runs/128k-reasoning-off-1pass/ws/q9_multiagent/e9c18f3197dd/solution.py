from math import gcd
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        n = len(target)
        full_mask = (1 << n) - 1
        
        # Precompute costs for each non-empty subset of targets
        # cost[mask] will store the minimum operations to satisfy the subset represented by mask
        # using a single number from nums (incremented to the nearest multiple of LCM of subset)
        cost = [float('inf')] * (1 << n)
        
        # Iterate over all non-empty subsets
        for mask in range(1, 1 << n):
            # Calculate LCM for the current subset
            current_lcm = 1
            for i in range(n):
                if mask & (1 << i):
                    val = target[i]
                    current_lcm = (current_lcm * val) // gcd(current_lcm, val)
            
            # Find the minimum cost to turn some nums[j] into a multiple of current_lcm
            # Cost for nums[j] is (current_lcm - nums[j] % current_lcm) % current_lcm
            min_ops = float('inf')
            for num in nums:
                rem = num % current_lcm
                ops = (current_lcm - rem) % current_lcm
                if ops < min_ops:
                    min_ops = ops
            
            cost[mask] = min_ops
        
        # DP to find minimum cost to satisfy all targets
        # dp[mask] = min cost to satisfy the subset of targets in mask
        dp = [float('inf')] * (1 << n)
        dp[0] = 0
        
        for mask in range(1, 1 << n):
            # Iterate over all submasks of mask
            # We can iterate submask from mask down to 0
            sub = mask
            while sub > 0:
                # Transition: satisfy 'sub' with cost[sub], and the rest (mask ^ sub) with dp[mask ^ sub]
                if dp[mask ^ sub] + cost[sub] < dp[mask]:
                    dp[mask] = dp[mask ^ sub] + cost[sub]
                sub = (sub - 1) & mask
        
        return dp[full_mask]