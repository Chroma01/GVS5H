from bisect import bisect_left
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []

        # Sort intervals by right endpoint, keeping original indices.
        # Tie-break by left endpoint then index for deterministic processing.
        order = sorted(range(n), key=lambda i: (intervals[i][1], intervals[i][0], i))
        L = [intervals[i][0] for i in order]
        R = [intervals[i][1] for i in order]
        W = [intervals[i][2] for i in order]
        IDX = order  # original index of the j-th sorted interval

        # prev[j] = largest position p (0-based in sorted order) such that R[p] < L[j],
        # or -1 if none. Strict inequality because touching boundaries counts as overlap.
        prev = [0] * n
        for j in range(n):
            prev[j] = bisect_left(R, L[j], 0, j) - 1

        K = 4
        NEG = -1
        # dp[j][k] = best (total_weight, tuple_of_original_indices) achievable
        # considering sorted intervals [0..j-1] and choosing exactly k of them.
        # Weight NEG means unreachable.
        dp = [[(NEG, ())] * (K + 1) for _ in range(n + 1)]
        dp[0][0] = (0, ())

        for j in range(1, n + 1):
            i = j - 1  # sorted position of current interval
            row = dp[j]
            prev_row = dp[j - 1]
            # Option 1: skip interval i -> states carry over.
            for k in range(K + 1):
                row[k] = prev_row[k]
            # Option 2: take interval i, chaining from the best row at prev[i]+1.
            base_row = dp[prev[i] + 1]
            wi = W[i]
            ii = IDX[i]
            for k in range(1, K + 1):
                b = base_row[k - 1]
                if b[0] == NEG:
                    continue
                cand = (b[0] + wi, b[1] + (ii,))
                cur = row[k]
                # Higher weight wins; on tie, lexicographically smaller tuple wins
                # (Python tuple comparison matches the problem's lexicographic rule,
                # including the shorter-is-smaller prefix rule).
                if cand[0] > cur[0] or (cand[0] == cur[0] and cand[1] < cur[1]):
                    row[k] = cand

        # Best among choosing 1..4 intervals (weights are positive, so the max-weight
        # state is unique in k, but comparing all k is safe).
        ans = (NEG, ())
        for k in range(1, K + 1):
            cand = dp[n][k]
            if cand[0] > ans[0] or (cand[0] == ans[0] and cand[1] < ans[1]):
                ans = cand
        return list(ans[1])