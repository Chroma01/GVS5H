import heapq
from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # Each target value must divide (be a divisor of) some final element of nums.
        # 1) deduplicate targets
        target = sorted(set(target))
        # 2) drop targets that divide another remaining target (they are auto-covered)
        reduced = []
        for t in target:
            if not any(u != t and u % t == 0 for u in target):
                reduced.append(t)
        target = reduced
        m = len(target)
        if m == 0:
            return 0

        size = 1 << m
        full = size - 1

        # lcm of every subset of (reduced) targets
        lcm_of = [1] * size
        for mask in range(1, size):
            low = mask & (-mask)
            i = low.bit_length() - 1
            a = lcm_of[mask ^ low]
            t = target[i]
            lcm_of[mask] = a // gcd(a, t) * t

        n = len(nums)

        # 3) candidate pruning: an optimal plan uses <= m elements; for every subset
        # keep the m cheapest elements (cost = minimal increments to reach a multiple
        # of lcm of that subset). An exchange argument shows some optimum lies inside
        # this candidate set.
        cand = set()
        for S in range(1, size):
            L = lcm_of[S]
            best = heapq.nsmallest(m, range(n), key=lambda i, L=L: (-nums[i]) % L)
            cand.update(best)

        INF = float('inf')
        dp = [INF] * size
        dp[0] = 0

        subs = list(range(1, size))
        ors = {S: [mask | S for mask in range(size)] for S in subs}

        # 4) 0/1 knapsack over candidate elements: each element used at most once
        for i in cand:
            if dp[full] == 0:
                break
            x = nums[i]
            cost = [0] * size
            for S in subs:
                cost[S] = (-x) % lcm_of[S]
            ndp = dp[:]
            for S in subs:
                c = cost[S]
                orl = ors[S]
                for mask in range(size):
                    v = dp[mask] + c
                    nm = orl[mask]
                    if v < ndp[nm]:
                        ndp[nm] = v
            dp = ndp

        return dp[full]