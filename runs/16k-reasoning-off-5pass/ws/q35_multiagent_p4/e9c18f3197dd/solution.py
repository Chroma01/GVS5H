import math
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        n_targets = len(target)
        total_masks = 1 << n_targets
        
        # Precompute LCM for all non-empty subsets of target
        # lcm_for_mask[mask] = LCM of elements in the subset represented by mask
        lcm_for_mask = [0] * total_masks
        
        for mask in range(1, total_masks):
            lcm_val = 1
            for i in range(n_targets):
                if mask & (1 << i):
                    lcm_val = math.lcm(lcm_val, target[i])
            lcm_for_mask[mask] = lcm_val
        
        # dp[mask] = minimum operations to cover the subset of targets indicated by mask
        INF = float('inf')
        dp = [INF] * total_masks
        dp[0] = 0
        
        # For each number in nums, update the DP table
        for n in nums:
            # We'll create a new_dp to avoid using the same number multiple times in one step
            # But actually, we can iterate and update in a way that each number is used at most once.
            # Standard knapsack-like: iterate masks in reverse? 
            # Actually, since we can choose to not use the current number, or use it to cover a submask,
            # we should do: new_dp = dp[:] and then update new_dp from dp.
            new_dp = dp[:]
            
            # For each existing state (mask) that is reachable
            for mask in range(total_masks):
                if dp[mask] == INF:
                    continue
                
                # Try all possible non-empty submasks that the current number can cover
                # Instead of iterating all submasks, we can iterate all masks and compute cost
                # But note: for a given submask, the cost is fixed: ceil(n / lcm) * lcm - n
                # We iterate over all submasks (non-empty)
                for submask in range(1, total_masks):
                    lcm_val = lcm_for_mask[submask]
                    # Calculate the smallest multiple of lcm_val that is >= n
                    # cost = (ceil(n / lcm_val) * lcm_val) - n
                    # Using integer arithmetic: 
                    #   if n % lcm_val == 0, cost = 0
                    #   else, cost = lcm_val - (n % lcm_val)
                    rem = n % lcm_val
                    if rem == 0:
                        cost = 0
                    else:
                        cost = lcm_val - rem
                    
                    new_mask = mask | submask
                    new_cost = dp[mask] + cost
                    if new_cost < new_dp[new_mask]:
                        new_dp[new_mask] = new_cost
            
            dp = new_dp
        
        return dp[total_masks - 1]