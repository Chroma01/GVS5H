from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        total_ops = 0
        
        for t in target:
            min_ops = float('inf')
            for n in nums:
                # Calculate cost to make n a multiple of t
                # If n is already a multiple, remainder is 0, cost is 0
                remainder = n % t
                cost = (t - remainder) % t
                if cost < min_ops:
                    min_ops = cost
            total_ops += min_ops
            
        return total_ops