from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        full = (1 << k) - 1

        # lcm[sub] = LCM of target values whose bits are set in sub
        lcm = [0] * (1 << k)
        for sub in range(1, 1 << k):
            low = sub & (-sub)
            i = low.bit_length() - 1
            prev = lcm[sub ^ low]  # 0 only when sub == low
            a = prev if prev else 1
            b = target[i]
            lcm[sub] = a // gcd(a, b) * b

        INF = float('inf')
        dp = [INF] * (1 << k)
        dp[0] = 0

        for x in nums:
            # cost for this element to become a multiple of each subset's LCM
            costs = [0] * (1 << k)
            for sub in range(1, 1 << k):
                L = lcm[sub]
                costs[sub] = (L - x % L) % L

            old = dp[:]  # snapshot so each nums element is used at most once
            for mask in range(1 << k):
                base = old[mask]
                if base == INF:
                    continue
                rem = full ^ mask
                sub = rem
                while sub:
                    nm = mask | sub
                    c = base + costs[sub]
                    if c < dp[nm]:
                        dp[nm] = c
                    sub = (sub - 1) & rem

        return dp[full]