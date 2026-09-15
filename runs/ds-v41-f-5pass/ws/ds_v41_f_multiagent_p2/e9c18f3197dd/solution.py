from typing import List
from math import gcd

class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Duplicate target values require the same divisibility condition.
        # One element divisible by a value satisfies all its copies.
        targets = list(set(target))
        m = len(targets)
        full = 1 << m
        INF = 10**18

        # lcm[mask] = LCM of the target values selected by mask.
        lcm = [1] * full
        for mask in range(1, full):
            L = 1
            for i in range(m):
                if mask & (1 << i):
                    L = L // gcd(L, targets[i]) * targets[i]
            lcm[mask] = L

        # dp[mask] = min operations using processed elements to cover mask.
        dp = [INF] * full
        dp[0] = 0

        for num in nums:
            # cost[sub] = increments needed so this num becomes a multiple of lcm[sub].
            cost = [0] * full
            for sub in range(1, full):
                L = lcm[sub]
                cost[sub] = (-num) % L

            new_dp = dp[:]  # do not use this element for any new target

            for mask in range(full):
                base = dp[mask]
                if base == INF:
                    continue

                # Only add targets that are not already covered.
                remaining = (full - 1) ^ mask
                sub = remaining
                while True:
                    nxt = mask | sub
                    val = base + cost[sub]
                    if val < new_dp[nxt]:
                        new_dp[nxt] = val
                    if sub == 0:
                        break
                    sub = (sub - 1) & remaining

            dp = new_dp

        return dp[full - 1]