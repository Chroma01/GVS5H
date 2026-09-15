from typing import List
from bisect import bisect_left

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        if not intervals:
            return []

        n = len(intervals)
        K = 4

        # Sort by end time, then start time, then original index.
        # Store as (end, start, original_index, weight).
        arr = [(r, l, idx, w) for idx, (l, r, w) in enumerate(intervals)]
        arr.sort()

        ends = [x[0] for x in arr]

        NEG = -10**30

        # scores[c][i] = best score using exactly c intervals among first i sorted intervals
        # tuples[c][i] = lexicographically smallest sorted tuple of original indices for that score
        scores = [[NEG] * (n + 1) for _ in range(K + 1)]
        tuples = [[None] * (n + 1) for _ in range(K + 1)]

        scores[0] = [0] * (n + 1)
        tuples[0] = [()] * (n + 1)

        bl = bisect_left

        for i, (r, l, idx, w) in enumerate(arr, 1):
            # Skip current interval: inherit previous prefix states.
            for c in range(1, K + 1):
                scores[c][i] = scores[c][i - 1]
                tuples[c][i] = tuples[c][i - 1]

            # Number of previous intervals ending strictly before current start.
            # Intervals touching at a boundary are overlapping, so use bisect_left.
            pi = bl(ends, l, 0, i - 1)

            # Take current interval. Descending c is safe and conventional.
            for c in range(K, 0, -1):
                prev_score = scores[c - 1][pi]
                if prev_score == NEG:
                    continue

                cand_score = prev_score + w
                cur_score = scores[c][i]
                if cand_score < cur_score:
                    continue

                prev_tuple = tuples[c - 1][pi]
                pos = bl(prev_tuple, idx)
                cand_tuple = prev_tuple[:pos] + (idx,) + prev_tuple[pos:]

                cur_tuple = tuples[c][i]
                if (
                    cand_score > cur_score
                    or (
                        cand_score == cur_score
                        and (cur_tuple is None or cand_tuple < cur_tuple)
                    )
                ):
                    scores[c][i] = cand_score
                    tuples[c][i] = cand_tuple

        best_score = NEG
        best_tuple = ()

        # Choose best among exact cardinalities 0..4.
        for c in range(K + 1):
            sc = scores[c][n]
            tup = tuples[c][n]
            if sc == NEG or tup is None:
                continue

            if sc > best_score or (sc == best_score and tup < best_tuple):
                best_score = sc
                best_tuple = tup

        return list(best_tuple)