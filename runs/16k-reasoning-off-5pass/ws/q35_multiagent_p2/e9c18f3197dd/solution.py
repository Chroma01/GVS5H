import math
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        n = len(nums)
        
        # Precompute LCM for all non-empty subsets of target
        # lcm_for_mask[mask] stores the LCM of targets in the subset represented by mask
        lcm_for_mask = [0] * (1 << m)
        
        for mask in range(1, 1 << m):
            lcm_val = 1
            for j in range(m):
                if mask & (1 << j):
                    lcm_val = math.lcm(lcm_val, target[j])
            lcm_for_mask[mask] = lcm_val
        
        # dp[mask] = minimum cost to cover the set of targets in mask
        INF = float('inf')
        dp = [INF] * (1 << m)
        dp[0] = 0
        
        # For each number in nums, update the dp table
        for num in nums:
            # Create a copy of dp to avoid using the same num multiple times in one step incorrectly
            # Actually, we can update in place if we iterate masks in decreasing order? 
            # But since we're adding a new num, we should consider: for each existing covered set (mask),
            # we can use this num to cover any additional subset (submask) of the remaining targets.
            # The new state would be mask | submask, and the cost added is the cost to cover submask with this num.
            # To avoid using the same num multiple times for different submasks in the same "layer", 
            # we should use a temporary dp array or iterate carefully.
            # Since n is large, we'll use a temporary array for each num? That would be O(n * 2^m) which is 5e4 * 16 = 8e5, acceptable.
            
            new_dp = dp[:]
            for mask in range(1 << m):
                if dp[mask] == INF:
                    continue
                # Consider all non-empty submasks of the complement of mask
                complement = ((1 << m) - 1) ^ mask
                # Iterate over all submasks of complement
                submask = complement
                while submask > 0:
                    # Calculate cost to cover submask with current num
                    lcm_val = lcm_for_mask[submask]
                    # Smallest multiple of lcm_val >= num
                    # cost = (lcm_val - (num % lcm_val)) % lcm_val
                    remainder = num % lcm_val
                    if remainder == 0:
                        cost = 0
                    else:
                        cost = lcm_val - remainder
                    
                    new_mask = mask | submask
                    if dp[mask] + cost < new_dp[new_mask]:
                        new_dp[new_mask] = dp[mask] + cost
                    submask = (submask - 1) & complement
            
            dp = new_dp
        
        return dp[(1 << m) - 1]