from typing import List
from bisect import bisect_left, insort


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        # Sort intervals by right endpoint; keep original indices.
        order = sorted(range(n), key=lambda j: intervals[j][1])
        rights = [intervals[j][1] for j in order]

        # dp[i][k] = best (weight, sorted-tuple-of-original-indices) using the
        # first i intervals in sorted order and choosing exactly k of them.
        # None means the state is infeasible.
        dp = [[None] * 5 for _ in range(n + 1)]
        dp[0][0] = (0, ())

        for i in range(1, n + 1):
            j = order[i - 1]
            l, r, w = intervals[j]
            # p = number of intervals with right endpoint strictly < l
            p = bisect_left(rights, l)
            dp[i][0] = (0, ())
            for k in range(1, 5):
                best = dp[i - 1][k]  # skip interval i
                prev = dp[p][k - 1]  # take interval i, extend best of first p
                if prev is not None:
                    tup = list(prev[1])
                    insort(tup, j)
                    cand = (prev[0] + w, tuple(tup))
                    if (best is None or cand[0] > best[0]
                            or (cand[0] == best[0] and cand[1] < best[1])):
                        best = cand
                dp[i][k] = best

        # Global max weight over k = 0..4, then lexicographically smallest tuple.
        bestW = -1
        bestT = None
        for k in range(5):
            st = dp[n][k]
            if st is None:
                continue
            if st[0] > bestW or (st[0] == bestW and (bestT is None or st[1] < bestT)):
                bestW = st[0]
                bestT = st[1]

        return list(bestT)