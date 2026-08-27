from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        size = 1 << m
        full = size - 1
        INF = 10 ** 30

        # lcm[mask] = LCM of target values whose bits are set in mask
        lcm = [1] * size
        for mask in range(1, size):
            lsb = mask & -mask
            i = lsb.bit_length() - 1
            prev = mask ^ lsb
            lcm[mask] = lcm[prev] // gcd(lcm[prev], target[i]) * target[i]

        # Precompute all valid transitions:
        # from a covered mask, we may add any nonempty submask of the uncovered bits.
        trans = [[] for _ in range(size)]
        for prev in range(size):
            rem = full ^ prev
            sub = rem
            while sub:
                trans[prev].append((prev | sub, sub))
                sub = (sub - 1) & rem

        # dp[mask] = minimum cost after processing some prefix of nums
        # to explicitly cover the target positions in mask.
        dp = [INF] * size
        dp[0] = 0

        for x in nums:
            # cost[mask] = increments needed to make x a multiple of lcm[mask]
            cost = [0] * size
            for mask in range(1, size):
                c = (-x) % lcm[mask]
                if c > INF:
                    c = INF
                cost[mask] = c

            # Fresh table so the current nums element is used at most once.
            ndp = dp[:]

            for prev in range(size):
                base = dp[prev]
                if base >= INF:
                    continue
                for new_mask, add in trans[prev]:
                    val = base + cost[add]
                    if val < ndp[new_mask]:
                        ndp[new_mask] = val

            dp = ndp
            if dp[full] == 0:
                return 0

        return dp[full]