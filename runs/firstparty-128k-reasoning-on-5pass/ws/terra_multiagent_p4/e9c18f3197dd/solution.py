from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        target = list(set(target))
        m = len(target)
        size = 1 << m
        full_mask = size - 1

        lcm = [1] * size
        for mask in range(1, size):
            bit = mask & -mask
            index = bit.bit_length() - 1
            previous = mask ^ bit
            lcm[mask] = lcm[previous] // gcd(lcm[previous], target[index]) * target[index]

        inf = 10**30
        dp = [inf] * size
        dp[0] = 0

        for x in nums:
            costs = [0] * size
            for mask in range(1, size):
                remainder = x % lcm[mask]
                costs[mask] = (lcm[mask] - remainder) % lcm[mask]

            next_dp = dp[:]
            for covered in range(size):
                if dp[covered] == inf:
                    continue
                for subset in range(1, size):
                    new_mask = covered | subset
                    candidate = dp[covered] + costs[subset]
                    if candidate < next_dp[new_mask]:
                        next_dp[new_mask] = candidate

            dp = next_dp

        return dp[full_mask]