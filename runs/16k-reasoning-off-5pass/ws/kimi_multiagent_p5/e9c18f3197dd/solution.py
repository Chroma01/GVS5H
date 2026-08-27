from math import gcd
from heapq import nsmallest
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        M = 1 << m
        full = M - 1

        # lcm of the target elements in every subset (m <= 4 -> at most 16 masks)
        lcm = [1] * M
        for mask in range(1, M):
            b = mask & -mask                 # lowest set bit
            i = b.bit_length() - 1
            p = lcm[mask ^ b]
            lcm[mask] = p // gcd(p, target[i]) * target[i]

        def cost(x: int, mask: int) -> int:
            # increments needed to raise x to the nearest multiple of lcm[mask]
            L = lcm[mask]
            r = x % L
            return 0 if r == 0 else L - r

        # For each subset keep only the 4 cheapest nums indices.
        # Why safe: an optimal solution partitions the targets into <= m <= 4
        # blocks, each block assigned to a DISTINCT nums element. If a block
        # used an element outside its subset's top-4, then among the 4 cheaper
        # elements at most 3 are used by other blocks, so one is free and can
        # replace it without increasing the total cost.
        cand = set()
        for mask in range(1, M):
            cand.update(nsmallest(4, range(len(nums)),
                                  key=lambda i: cost(nums[i], mask)))

        # DP over candidate elements x masks; each candidate used at most once.
        INF = float('inf')
        dp = [INF] * M
        dp[0] = 0
        for i in cand:
            x = nums[i]
            c = [0] + [cost(x, mask) for mask in range(1, M)]
            ndp = dp[:]                       # option: do not use nums[i]
            for mask in range(1, M):
                best = ndp[mask]
                s = mask
                while s:                      # assign nums[i] to submask s
                    v = dp[mask ^ s] + c[s]
                    if v < best:
                        best = v
                    s = (s - 1) & mask
                ndp[mask] = best
            dp = ndp
        return dp[full]