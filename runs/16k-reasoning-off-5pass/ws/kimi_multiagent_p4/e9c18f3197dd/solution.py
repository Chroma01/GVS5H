from typing import List
from math import gcd


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        full = (1 << k) - 1

        # cost[mask]: minimum increments to make some single element of nums
        # a common multiple of all target values in mask.
        INF = float('inf')
        cost = [INF] * (1 << k)

        for mask in range(1, 1 << k):
            # LCM of the targets in this mask
            l = 1
            for i in range(k):
                if mask & (1 << i):
                    l = l * target[i] // gcd(l, target[i])
            # Cheapest nums element to raise to a multiple of l:
            # for value n, cost = (-n) % l  (0 if already a multiple)
            best = INF
            for n in nums:
                c = (-n) % l
                if c < best:
                    best = c
                    if best == 0:
                        break
            cost[mask] = best

        # dp[mask]: min cost to cover all targets in mask, partitioning into groups
        dp = [INF] * (1 << k)
        dp[0] = 0
        for mask in range(1, 1 << k):
            sub = mask
            while sub:
                rest = mask ^ sub
                if dp[rest] + cost[sub] < dp[mask]:
                    dp[mask] = dp[rest] + cost[sub]
                sub = (sub - 1) & mask

        return dp[full]