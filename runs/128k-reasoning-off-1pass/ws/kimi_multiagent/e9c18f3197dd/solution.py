from typing import List
import math


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        M = 1 << k

        # lcm[mask] = least common multiple of target[i] for i in mask
        lcm = [1] * M
        for mask in range(1, M):
            lsb = mask & (-mask)
            i = lsb.bit_length() - 1
            prev = lcm[mask ^ lsb]
            t = target[i]
            lcm[mask] = prev * t // math.gcd(prev, t)

        # Precompute submask lists for each mask (nonzero submasks)
        submasks = [[] for _ in range(M)]
        for mask in range(1, M):
            subs = []
            sub = mask
            while sub:
                subs.append(sub)
                sub = (sub - 1) & mask
            submasks[mask] = subs

        INF = float('inf')
        dp = [INF] * M
        dp[0] = 0

        for x in nums:
            # c[mask] = increments needed for x to become a multiple of lcm[mask]
            c = [0] * M
            for mask in range(1, M):
                L = lcm[mask]
                c[mask] = (-x) % L

            # Snapshot dp so each nums element is used at most once.
            old = dp[:]
            for mask in range(1, M):
                best = old[mask]  # don't use this element for mask
                for sub in submasks[mask]:
                    cand = old[mask ^ sub] + c[sub]
                    if cand < best:
                        best = cand
                dp[mask] = best

        return dp[M - 1]