from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        m = len(target)
        full = (1 << m) - 1
        size = 1 << m

        # lcm[mask] = lcm of target values whose bits are set in mask
        lcm = [1] * size
        for mask in range(1, size):
            lsb = mask & -mask
            i = lsb.bit_length() - 1
            prev = mask ^ lsb
            l = lcm[prev]
            t = target[i]
            lcm[mask] = (l // gcd(l, t)) * t

        # transitions[mask] = all nonempty subsets of still-unsatisfied targets
        transitions = [[] for _ in range(size)]
        for mask in range(size):
            avail = full ^ mask
            sub = avail
            while sub:
                transitions[mask].append((sub, mask | sub))
                sub = (sub - 1) & avail

        # A feasible solution assigns distinct nums elements to target positions,
        # costing less than target[i] each, so answer < sum(target).
        INF = sum(target) + 1

        dp = [INF] * size
        dp[0] = 0

        for x in nums:
            cost = [0] * size
            for add in range(1, size):
                L = lcm[add]
                r = x % L
                c = 0 if r == 0 else L - r
                if c > INF:
                    c = INF
                cost[add] = c

            new_dp = dp[:]  # leave current nums element unused
            for mask in range(size):
                base = dp[mask]
                if base >= INF:
                    continue
                for add, nxt in transitions[mask]:
                    c = cost[add]
                    if c >= INF:
                        continue
                    val = base + c
                    if val < new_dp[nxt]:
                        new_dp[nxt] = val

            dp = new_dp
            if dp[full] == 0:
                return 0

        return dp[full]