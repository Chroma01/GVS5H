from bisect import bisect_left, insort
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Sort intervals by right endpoint; tie-break by left then original
        # index for deterministic processing.
        order = sorted(range(n), key=lambda i: (intervals[i][1], intervals[i][0], i))
        rights = [intervals[i][1] for i in order]
        lefts = [intervals[i][0] for i in order]
        weights = [intervals[i][2] for i in order]
        orig_idx = order  # position in sorted order -> original index

        # p[i] = number of sorted intervals (among first i) compatible with
        # sorted interval i, i.e. count of intervals with r < l_i.
        # Intervals sharing a boundary are overlapping, so strict inequality.
        p = [0] * n
        for i in range(n):
            p[i] = bisect_left(rights, lefts[i], 0, i)

        NEG = -1  # sentinel for unreachable states
        # dp[i][k] = (best_weight, best_sorted_index_tuple) using first i
        # sorted intervals choosing exactly k non-overlapping intervals.
        dp = [[(0, ())] + [(NEG, None)] * 4 for _ in range(n + 1)]

        def better(a, b):
            # Return the better of (weight, tuple) candidates a and b.
            # Higher weight wins; tie -> lexicographically smaller tuple
            # (Python tuple comparison: shorter prefix is smaller).
            if b[0] == NEG:
                return a
            if a[0] == NEG:
                return b
            if a[0] != b[0]:
                return a if a[0] > b[0] else b
            return a if a[1] <= b[1] else b

        for i in range(1, n + 1):
            j = i - 1  # sorted position of interval under consideration
            pi = p[j]
            for k in range(5):
                # Option 1: skip interval j
                best = dp[i - 1][k]
                # Option 2: take interval j (needs exactly k-1 before it)
                if k >= 1:
                    prev = dp[pi][k - 1]
                    if prev[0] != NEG:
                        new_tuple = list(prev[1])
                        insort(new_tuple, orig_idx[j])
                        cand = (prev[0] + weights[j], tuple(new_tuple))
                        best = better(best, cand)
                dp[i][k] = best

        # At most 4 intervals: take best over k = 0..4.
        ans = dp[n][0]
        for k in range(1, 5):
            ans = better(ans, dp[n][k])
        return list(ans[1])