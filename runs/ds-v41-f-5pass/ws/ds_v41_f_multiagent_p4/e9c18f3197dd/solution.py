from math import gcd
from heapq import nsmallest
from typing import List

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        size = 1 << m
        full = size - 1

        # LCM of every subset of target values.
        lcm = [1] * size
        for mask in range(1, size):
            lsb = mask & (-mask)
            i = lsb.bit_length() - 1
            prev = mask ^ lsb
            l = lcm[prev]
            t = target[i]
            lcm[mask] = l // gcd(l, t) * t

        n = len(nums)

        # cost[i][mask] = increments to make nums[i] a multiple of lcm[mask]
        #               = minimum cost for element i to cover all targets in mask.
        costs = []
        for x in nums:
            row = [0] * size
            for mask in range(1, size):
                L = lcm[mask]
                row[mask] = (-x) % L
            costs.append(row)

        # At most m elements are ever needed. For each (nonempty) subset, keep the
        # K cheapest elements for covering it. A replacement argument shows K = m+1
        # suffices: any element of an optimal assignment that is not among the K
        # cheapest for its covered subset can be swapped for a free, no-worse one.
        K = min(n, m + 1)
        cand = set()
        for mask in range(1, size):
            for idx in nsmallest(K, range(n), key=lambda i: costs[i][mask]):
                cand.add(idx)

        INF = float('inf')
        dp = [INF] * size
        dp[0] = 0
        for i in cand:
            row = costs[i]
            ndp = dp[:]  # option to skip this element
            for old in range(size):
                base = dp[old]
                if base == INF:
                    continue
                for mask in range(1, size):
                    nm = old | mask
                    v = base + row[mask]
                    if v < ndp[nm]:
                        ndp[nm] = v
            dp = ndp

        return dp[full]