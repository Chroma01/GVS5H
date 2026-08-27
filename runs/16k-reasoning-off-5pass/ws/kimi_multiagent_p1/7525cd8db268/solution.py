from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # For each right endpoint b (the larger value of a pair), track the
        # largest partner a (best), the effective second largest (second),
        # and how many pairs achieve the maximum (cnt, for duplicates).
        best = [0] * (n + 1)
        second = [0] * (n + 1)
        cnt = [0] * (n + 1)

        for x, y in conflictingPairs:
            a, b = (x, y) if x < y else (y, x)
            if a > best[b]:
                second[b] = best[b]
                best[b] = a
                cnt[b] = 1
            elif a == best[b]:
                cnt[b] += 1
            elif a > second[b]:
                second[b] = a

        # If the maximum partner occurs in multiple pairs, removing one of
        # them leaves the constraint unchanged -> effective second = best.
        for b in range(1, n + 1):
            if cnt[b] > 1:
                second[b] = best[b]

        baseline = 0          # valid subarrays with all pairs present
        max_gain = 0          # best extra subarrays from removing one pair
        cur = 0               # current running max of best[1..r]
        rec = -1              # right endpoint that set the current record
        pm = 0                # max(second[rec], best values seen after rec)
        gains = {}            # gain per record position

        for r in range(1, n + 1):
            if best[r] > cur:
                # New record: constraint best[r] becomes the binding one.
                cur = best[r]
                rec = r
                pm = second[r]
                gains[rec] = 0
            else:
                if rec != -1 and best[r] > pm:
                    pm = best[r]
            baseline += r - cur
            if rec != -1:
                gains[rec] += cur - pm

        for g in gains.values():
            if g > max_gain:
                max_gain = g

        return baseline + max_gain