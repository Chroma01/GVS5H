from typing import List
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Sort by right endpoint, carrying (r, l, w, original index).
        arr = sorted(((iv[1], iv[0], iv[2], i) for i, iv in enumerate(intervals)))
        ends = [a[0] for a in arr]

        # dp[i][k] = (best weight, lexicographically smallest sorted tuple of
        # original indices achieving it) using the first i intervals in
        # right-endpoint order, with at most k picks.
        EMPTY = (0, ())
        dp = [[EMPTY] * 5 for _ in range(n + 1)]

        for i in range(1, n + 1):
            r, l, w, idx = arr[i - 1]
            # number of intervals whose right endpoint is strictly less than l
            p = bisect_left(ends, l)
            row_prev = dp[i - 1]
            row_p = dp[p]
            row = dp[i]
            # k == 0 stays EMPTY
            for k in range(1, 5):
                bw, bt = row_prev[k]        # skip interval i
                pw, pt = row_p[k - 1]       # take interval i
                cw = pw + w
                if cw < bw:
                    row[k] = (bw, bt)
                else:
                    # compute the merged index tuple exactly once
                    ct = (idx,) if not pt else tuple(sorted(pt + (idx,)))
                    if cw > bw or ct < bt:
                        row[k] = (cw, ct)
                    else:
                        row[k] = (bw, bt)

        return list(dp[n][4][1])