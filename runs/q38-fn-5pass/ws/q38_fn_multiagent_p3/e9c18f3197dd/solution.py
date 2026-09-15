from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        if not nums:
            return 0

        vals = sorted(set(target))
        m = len(vals)
        if m == 0:
            return 0

        size = 1 << m
        full = size - 1
        INF = 10**18
        max_val = max(nums)
        cap = max_val + INF + 1

        lcms = [1] * size
        for mask in range(1, size):
            lb = mask & -mask
            bit = lb.bit_length() - 1
            prev = mask ^ lb
            l = lcms[prev]
            if l >= cap:
                lcms[mask] = cap
            else:
                t = vals[bit]
                val = (l // gcd(l, t)) * t
                lcms[mask] = cap if val > cap else val

        submasks = [[] for _ in range(size)]
        for mask in range(size):
            rem = full ^ mask
            sub = rem
            while sub:
                submasks[mask].append(sub)
                sub = (sub - 1) & rem

        dp = [INF] * size
        dp[0] = 0

        for x in nums:
            costs = [0] * size
            for mask in range(1, size):
                l = lcms[mask]
                c = (l - x % l) % l
                if c > INF:
                    c = INF
                costs[mask] = c

            for mask in range(full, -1, -1):
                base = dp[mask]
                if base >= INF:
                    continue
                for sub in submasks[mask]:
                    c = costs[sub]
                    if c >= INF:
                        continue
                    val = base + c
                    nm = mask | sub
                    if val < dp[nm]:
                        dp[nm] = val
                        if nm == full and val == 0:
                            return 0

        return dp[full]