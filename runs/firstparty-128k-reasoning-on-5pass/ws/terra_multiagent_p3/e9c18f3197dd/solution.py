from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        target = list(dict.fromkeys(target))
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
                costs[mask] = (-x) % lcm[mask]

            next_dp = dp[:]

            for covered in range(size):
                if dp[covered] == inf:
                    continue

                base = dp[covered]
                for add_mask in range(1, size):
                    combined = covered | add_mask
                    candidate = base + costs[add_mask]
                    if candidate < next_dp[combined]:
                        next_dp[combined] = candidate

            dp = next_dp

        return dp[full_mask]