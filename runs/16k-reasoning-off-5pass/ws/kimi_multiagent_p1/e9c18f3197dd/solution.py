from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1

        # lcm[mask] = least common multiple of target values in this subset
        lcm = [0] * (1 << m)
        for mask in range(1, 1 << m):
            lsb = mask & (-mask)
            i = lsb.bit_length() - 1
            prev = lcm[mask ^ lsb]
            t = target[i]
            if prev == 0:
                lcm[mask] = t
            else:
                lcm[mask] = prev // gcd(prev, t) * t

        INF = float('inf')
        # dp[mask] = min total increments to cover exactly `mask` of targets
        # using processed nums elements, each element used at most once.
        dp = [INF] * (1 << m)
        dp[0] = 0

        for x in nums:
            # cost of using this element to cover subset s:
            # raise x to the smallest multiple of lcm[s] that is >= x
            cost = [0] * (1 << m)
            for s in range(1, 1 << m):
                L = lcm[s]
                cost[s] = ((x + L - 1) // L) * L - x

            ndp = dp[:]  # option: don't use this element
            for mask in range(1 << m):
                base = dp[mask]
                if base == INF:
                    continue
                avail = full ^ mask
                s = avail
                while s:
                    v = base + cost[s]
                    nm = mask | s
                    if v < ndp[nm]:
                        ndp[nm] = v
                    s = (s - 1) & avail
            dp = ndp

        return dp[full]