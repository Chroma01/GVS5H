from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        target = list(dict.fromkeys(target))
        m = len(target)
        full = (1 << m) - 1

        lcm = [1] * (1 << m)
        for mask in range(1, 1 << m):
            bit = mask & -mask
            index = bit.bit_length() - 1
            previous = mask ^ bit
            lcm[mask] = lcm[previous] // gcd(lcm[previous], target[index]) * target[index]

        inf = 10**30
        dp = [inf] * (1 << m)
        dp[0] = 0

        for x in nums:
            costs = [0] * (1 << m)
            for mask in range(1, 1 << m):
                costs[mask] = ((x + lcm[mask] - 1) // lcm[mask]) * lcm[mask] - x

            next_dp = dp[:]

            for covered in range(1 << m):
                if dp[covered] == inf:
                    continue

                remaining = full ^ covered
                subset = remaining
                while subset:
                    new_mask = covered | subset
                    next_dp[new_mask] = min(
                        next_dp[new_mask],
                        dp[covered] + costs[subset]
                    )
                    subset = (subset - 1) & remaining

            dp = next_dp

        return dp[full]