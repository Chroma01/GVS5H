from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        target = list(set(target))
        m = len(target)
        full = (1 << m) - 1

        lcm = [1] * (1 << m)
        for mask in range(1, 1 << m):
            bit = mask & -mask
            i = bit.bit_length() - 1
            prev = mask ^ bit
            lcm[mask] = lcm[prev] // gcd(lcm[prev], target[i]) * target[i]

        inf = 10**30
        dp = [inf] * (1 << m)
        dp[0] = 0

        for x in nums:
            ndp = dp[:]

            costs = [0] * (1 << m)
            for subset in range(1, 1 << m):
                L = lcm[subset]
                costs[subset] = ((x + L - 1) // L) * L - x

            for covered in range(1 << m):
                if dp[covered] == inf:
                    continue

                remaining = full ^ covered
                subset = remaining
                while subset:
                    new_mask = covered | subset
                    candidate = dp[covered] + costs[subset]
                    if candidate < ndp[new_mask]:
                        ndp[new_mask] = candidate
                    subset = (subset - 1) & remaining

            dp = ndp

        return dp[full]