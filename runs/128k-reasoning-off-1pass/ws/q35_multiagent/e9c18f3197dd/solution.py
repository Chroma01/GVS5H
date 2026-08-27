import math
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        n = len(nums)
        t = len(target)
        
        # Precompute min cost for each subset of targets using a single nums element
        # There are 2^t subsets
        num_subsets = 1 << t
        min_cost_for_subset = [float('inf')] * num_subsets
        
        # For each subset mask, compute LCM of targets in the subset
        # and then find min cost over all nums elements
        for mask in range(1, num_subsets):
            lcm_val = 1
            for j in range(t):
                if mask & (1 << j):
                    lcm_val = math.lcm(lcm_val, target[j])
            
            # Find min cost to make any nums[i] a multiple of lcm_val
            min_cost = float('inf')
            for x in nums:
                cost = (lcm_val - x % lcm_val) % lcm_val
                if cost < min_cost:
                    min_cost = cost
            min_cost_for_subset[mask] = min_cost
        
        # DP to cover all targets
        # dp[mask] = min cost to satisfy the subset of targets in mask
        dp = [float('inf')] * num_subsets
        dp[0] = 0
        
        # Iterate over all masks
        for mask in range(1, num_subsets):
            # Iterate over all submasks of mask
            submask = mask
            while submask > 0:
                # Consider satisfying submask with one nums element, and the rest with dp[mask ^ submask]
                cost = dp[mask ^ submask] + min_cost_for_subset[submask]
                if cost < dp[mask]:
                    dp[mask] = cost
                submask = (submask - 1) & mask
        
        return dp[num_subsets - 1]