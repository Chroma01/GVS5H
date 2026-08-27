from bisect import bisect_left
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Sort intervals by right endpoint, keeping original indices.
        order = sorted(range(n), key=lambda i: (intervals[i][1], intervals[i][0]))
        L = [intervals[i][0] for i in order]
        R = [intervals[i][1] for i in order]
        W = [intervals[i][2] for i in order]
        IDX = order  # original index of the i-th sorted interval

        # p[i] = number of sorted intervals whose right endpoint is strictly
        # less than L[i-1] (boundary touch counts as overlap, hence strict).
        p = [0] * (n + 1)
        for i in range(1, n + 1):
            p[i] = bisect_left(R, L[i - 1], 0, i - 1)

        K = 4
        NEG = (-1, None)  # sentinel for unreachable states

        def better(a, b):
            # a, b: (weight, ascending tuple of original indices) or NEG.
            # Higher weight wins; ties -> lexicographically smaller tuple
            # (Python tuple comparison implements the prefix rule).
            if a[1] is None:
                return b
            if b[1] is None:
                return a
            if a[0] != b[0]:
                return a if a[0] > b[0] else b
            return a if a[1] <= b[1] else b

        # dp[i][k] = best (weight, ascending index tuple) using intervals
        # among the first i sorted intervals with exactly k picks.
        dp = [[NEG] * (K + 1) for _ in range(n + 1)]
        for i in range(n + 1):
            dp[i][0] = (0, ())

        for i in range(1, n + 1):
            wi = W[i - 1]
            oi = IDX[i - 1]
            pi = p[i]
            row = dp[i]
            prev_row = dp[i - 1]
            take_row = dp[pi]
            for k in range(1, K + 1):
                # Option 1: skip interval i
                best = prev_row[k]
                # Option 2: take interval i
                prev_state = take_row[k - 1]
                if prev_state[1] is not None:
                    cand = (prev_state[0] + wi,
                            tuple(sorted(prev_state[1] + (oi,))))
                    best = better(best, cand)
                row[k] = best

        # Answer: best over k = 0..4 at i = n
        ans = dp[n][0]
        for k in range(1, K + 1):
            ans = better(ans, dp[n][k])
        return list(ans[1])