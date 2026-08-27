from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        k = len(target)
        full = (1 << k) - 1

        # Precompute LCM for every non-empty subset of target
        lcm = [0] * (1 << k)
        for mask in range(1, 1 << k):
            lsb = mask & -mask
            i = lsb.bit_length() - 1
            prev = lcm[mask ^ lsb]
            if prev == 0:
                lcm[mask] = target[i]
            else:
                lcm[mask] = prev // gcd(prev, target[i]) * target[i]

        INF = float('inf')
        dp = [INF] * (1 << k)
        dp[0] = 0

        for x in nums:
            # Cost for x to become a multiple of each subset's LCM
            cost = [0] * (1 << k)
            for mask in range(1, 1 << k):
                L = lcm[mask]
                r = x % L
                cost[mask] = 0 if r == 0 else L - r

            new_dp = dp[:]  # option: skip this element
            for mask in range(1 << k):
                if dp[mask] == INF:
                    continue
                # submask of targets not yet covered
                rem = full ^ mask
                sub = rem
                while sub:
                    nm = mask | sub
                    c = dp[mask] + cost[sub]
                    if c < new_dp[nm]:
                        new_dp[nm] = c
                    sub = (sub - 1) & rem
            dp = new_dp

        return dp[full]