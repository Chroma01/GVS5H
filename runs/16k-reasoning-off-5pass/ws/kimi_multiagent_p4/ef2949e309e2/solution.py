from typing import List
from collections import Counter

MOD = 10**9 + 7


class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        n = len(nums)
        # Coordinate compress
        vals = sorted(set(nums))
        comp = {v: i for i, v in enumerate(vals)}
        a = [comp[v] for v in nums]
        m = len(vals)

        def c2(x: int) -> int:
            return x * (x - 1) // 2

        # Right side initially contains everything
        rcnt = [0] * m
        for v in a:
            rcnt[v] += 1
        lcnt = [0] * m

        # sumC2 over a side: sum of C(count,2) over all values
        rsumC2 = sum(c2(c) for c in rcnt)
        lsumC2 = 0

        ans = 0

        for i in range(n):
            v = a[i]
            # move a[i] from right to "current" (remove from right)
            rsumC2 -= c2(rcnt[v])
            rcnt[v] -= 1
            rsumC2 += c2(rcnt[v])

            nL = i
            nR = n - i - 1
            if nL >= 2 and nR >= 2:
                lv = lcnt[v]
                rv = rcnt[v]
                nonvL = nL - lv
                nonvR = nR - rv

                # pairs on a side, categorized by # of v's
                L2v = c2(lv)                    # both v
                L1v = lv * nonvL                # exactly one v
                L0v = c2(nonvL)                 # zero v (any, may be equal)
                R2v = c2(rv)
                R1v = rv * nonvR
                R0v = c2(nonvR)

                # zero-v pairs with two distinct values
                L0v_distinct = L0v - (lsumC2 - c2(lv))
                R0v_distinct = R0v - (rsumC2 - c2(rv))

                total = 0

                # k = 4: both left pair and right pair are all v
                total += L2v * R2v

                # k = 3: exactly 3 v's among the 4 picks
                # (2 v from left, 1 v from right) or (1 v from left, 2 v from right)
                total += L2v * R1v + L1v * R2v

                # k = 2: exactly 2 v's; the other two elements are arbitrary non-v
                total += L2v * R0v + L1v * R1v + L0v * R2v

                # k = 1: exactly one v; the other three non-v elements pairwise distinct
                # case A: v from left (left pair has exactly one v), right pair zero-v distinct,
                #         and neither right element equals the left non-v value x.
                # sum over x != v of lcnt[x] * (R0v_distinct - rcnt[x] * (nonvR - rcnt[x]))
                sumA = 0
                for x in range(m):
                    lx = lcnt[x]
                    if lx and x != v:
                        sumA += lx * (R0v_distinct - rcnt[x] * (nonvR - rcnt[x]))
                total += lv * sumA

                # case B: v from right, symmetric
                sumB = 0
                for x in range(m):
                    rx = rcnt[x]
                    if rx and x != v:
                        sumB += rx * (L0v_distinct - lcnt[x] * (nonvL - lcnt[x]))
                total += rv * sumB

                ans = (ans + total) % MOD

            # add a[i] to left
            lsumC2 -= c2(lcnt[v])
            lcnt[v] += 1
            lsumC2 += c2(lcnt[v])

        return ans % MOD