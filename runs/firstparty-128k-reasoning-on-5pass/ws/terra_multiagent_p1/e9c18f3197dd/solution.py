from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Duplicate target values need only one multiple.
        target = list(set(target))
        m = len(target)
        size = 1 << m
        full = size - 1

        # lcm[mask] is the least value whose multiples satisfy all targets in mask.
        lcm = [1] * size
        for mask in range(1, size):
            bit = mask & -mask
            i = bit.bit_length() - 1
            prev = mask ^ bit
            lcm[mask] = lcm[prev] // gcd(lcm[prev], target[i]) * target[i]

        inf = float("inf")
        dp = [inf] * size
        dp[0] = 0

        for x in nums:
            cost = [0] * size
            for mask in range(1, size):
                cost[mask] = (-x) % lcm[mask]

            # Skip this number by retaining all existing states.
            ndp = dp[:]

            for covered in range(size):
                if dp[covered] == inf:
                    continue

                remaining = full ^ covered
                sub = remaining
                while sub:
                    nxt = covered | sub
                    ndp[nxt] = min(ndp[nxt], dp[covered] + cost[sub])
                    sub = (sub - 1) & remaining

            dp = ndp

        return dp[full]