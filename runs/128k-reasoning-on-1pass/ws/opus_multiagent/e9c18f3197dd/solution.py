from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1

        # Precompute lcm for every subset of targets
        L = [1] * (full + 1)
        for S in range(1, full + 1):
            lb = S & -S
            b = lb.bit_length() - 1
            a = L[S ^ lb]
            t = target[b]
            L[S] = a * t // gcd(a, t)

        INF = float('inf')
        dp = [INF] * (full + 1)
        dp[0] = 0

        # Precompute, for each mask, the nonempty submasks of its complement
        trans = []
        for mask in range(full + 1):
            comp = full ^ mask
            subs = []
            s = comp
            while s:
                subs.append((s, mask | s))
                s = (s - 1) & comp
            trans.append(subs)

        rng = range(1, full + 1)
        for num in nums:
            cost = [0] * (full + 1)
            for S in rng:
                l = L[S]
                cost[S] = (l - num % l) % l
            ndp = dp[:]
            for mask in range(full + 1):
                d = dp[mask]
                if d == INF:
                    continue
                for s, nm in trans[mask]:
                    v = d + cost[s]
                    if v < ndp[nm]:
                        ndp[nm] = v
            dp = ndp
            if dp[full] == 0:
                break

        return dp[full]