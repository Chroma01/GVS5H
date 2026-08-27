from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1

        # Compute the LCM required for every subset of target indices.
        subset_lcm = [1] * (1 << m)
        for mask in range(1, 1 << m):
            bit = mask & -mask
            idx = bit.bit_length() - 1
            prev = mask ^ bit
            a = subset_lcm[prev]
            b = target[idx]
            subset_lcm[mask] = a // gcd(a, b) * b

        inf = 10**100
        dp = [inf] * (1 << m)
        dp[0] = 0

        for value in nums:
            costs = [0] * (1 << m)
            for mask in range(1, 1 << m):
                multiple = subset_lcm[mask]
                costs[mask] = ((value + multiple - 1) // multiple) * multiple - value

            # Skip this number, or assign it to a subset of currently
            # uncovered targets. Transitions use the previous dp state.
            ndp = dp[:]
            for covered in range(1 << m):
                base = dp[covered]
                if base == inf:
                    continue

                remaining = full ^ covered
                sub = remaining
                while sub:
                    new_mask = covered | sub
                    candidate = base + costs[sub]
                    if candidate < ndp[new_mask]:
                        ndp[new_mask] = candidate
                    sub = (sub - 1) & remaining

            dp = ndp
            if dp[full] == 0:
                return 0

        return dp[full]