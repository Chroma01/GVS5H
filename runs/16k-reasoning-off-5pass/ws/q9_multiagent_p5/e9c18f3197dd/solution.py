from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        total_ops = 0
        
        for t in target:
            min_ops_for_t = float('inf')
            
            for n in nums:
                # Calculate the remainder of n divided by t
                remainder = n % t
                
                # If n is already a multiple of t, remainder is 0, cost is 0
                # Otherwise, we need to add (t - remainder) to reach the next multiple
                if remainder == 0:
                    cost = 0
                else:
                    cost = t - remainder
                
                if cost < min_ops_for_t:
                    min_ops_for_t = cost
            
            total_ops += min_ops_for_t
            
        return total_ops