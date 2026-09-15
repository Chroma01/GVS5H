import heapq
from math import gcd
from typing import List


class Solution:
    def minimumIncrements(self, nums: List[int], target: List[int]) -> int:
        # 1) Deduplicate targets and drop any target that divides another target.
        #    If a value is made a multiple of t', and t | t', it is automatically
        #    a multiple of t, so t is redundant.
        uniq = sorted(set(target))
        ts = [t for t in uniq if not any(o != t and o % t == 0 for o in uniq)]
        m = len(ts)
        full = (1 << m) - 1

        # 2) LCM of every non-empty subset of (reduced) targets.
        lcmv = [1] * (full + 1)
        for s in range(1, full + 1):
            l = 1
            ss = s
            while ss:
                b = ss & (-ss)
                i = b.bit_length() - 1
                l = l // gcd(l, ts[i]) * ts[i]
                ss ^= b
            lcmv[s] = l

        # 3) Candidate reduction.  An optimal solution uses at most m groups,
        #    so for a group assigned subset s its element is among the m cheapest
        #    elements for s (at most m-1 other elements are used by other groups).
        n = len(nums)
        cand = set()
        for s in range(1, full + 1):
            l = lcmv[s]
            cand.update(heapq.nsmallest(m, range(n), key=lambda i, l=l: (-nums[i]) % l))
        cand = sorted(cand)

        # 4) Layered DP over candidate elements; each element used at most once.
        INF = float('inf')
        dp = [INF] * (full + 1)
        dp[0] = 0
        for i in cand:
            x = nums[i]
            dp2 = dp[:]  # option: do not use this element
            for s in range(1, full + 1):
                cost = (-x) % lcmv[s]  # round x up to next multiple of LCM(s)
                for mask in range(full + 1):
                    v = dp[mask]
                    if v == INF:
                        continue
                    t = mask | s
                    nv = v + cost
                    if nv < dp2[t]:
                        dp2[t] = nv
            dp = dp2

        return dp[full]