from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        total_ops = 0
        for t in target:
            min_ops = float('inf')
            for n in nums:
                rem = n % t
                if rem == 0:
                    cost = 0
                else:
                    cost = t - rem
                if cost < min_ops:
                    min_ops = cost
            total_ops += min_ops
        return total_ops