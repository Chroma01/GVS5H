from bisect import bisect_left
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Sort intervals by right endpoint, carrying original indices.
        order = sorted(range(n), key=lambda i: intervals[i][1])
        L = [intervals[i][0] for i in order]
        R = [intervals[i][1] for i in order]
        W = [intervals[i][2] for i in order]
        orig = order  # orig[i] = original index of i-th interval in sorted order

        # p[i] = largest index j < i such that R[j] < L[i] (strict: touching overlaps).
        p = [-1] * n
        for i in range(n):
            p[i] = bisect_left(R, L[i], 0, i) - 1

        # dp[i][k] = (max weight, lexicographically smallest sorted tuple of
        # original indices) using intervals among first i (sorted), at most k taken.
        # Comparison: higher weight wins; ties broken by smaller tuple.
        NEG = (-1, ())  # weight -1 marks "no selection yet"; weights are >= 1
        dp = [[NEG] * 5 for _ in range(n + 1)]
        for k in range(5):
            dp[0][k] = (0, ())

        def better(a, b):
            # Return the better of two (weight, path) candidates.
            if a[0] != b[0]:
                return a if a[0] > b[0] else b
            return a if a[1] <= b[1] else b

        for i in range(1, n + 1):
            j = p[i - 1] + 1  # number of intervals compatible before interval i-1
            for k in range(5):
                # Option 1: skip interval i-1.
                best = dp[i - 1][k]
                # Option 2: take interval i-1 (needs a free slot).
                if k >= 1:
                    prev_w, prev_path = dp[j][k - 1]
                    if prev_w >= 0:
                        w = prev_w + W[i - 1]
                        # Insert original index into sorted tuple (path length <= 3).
                        oi = orig[i - 1]
                        new_path = tuple(sorted(prev_path + (oi,)))
                        best = better(best, (w, new_path))
                dp[i][k] = best

        return list(dp[n][4][1])