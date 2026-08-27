from typing import List
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        # Store as (right, left, original_index, weight) and sort by right endpoint.
        # Tie-breaking by left/index is harmless; compatibility only depends on right endpoints.
        arr = [(r, l, i, w) for i, (l, r, w) in enumerate(intervals)]
        arr.sort()
        ends = [r for r, l, idx, w in arr]

        MAXT = 4
        NEG = -1

        # dp_w[t][i]  = maximum weight using exactly t intervals among first i end-sorted intervals
        # dp_idx[t][i] = lexicographically smallest sorted 0-based original-index tuple achieving it
        dp_w = [[NEG] * (n + 1) for _ in range(MAXT + 1)]
        dp_idx = [[None] * (n + 1) for _ in range(MAXT + 1)]

        dp_w[0] = [0] * (n + 1)
        dp_idx[0] = [()] * (n + 1)

        for i, (r, l, idx, w) in enumerate(arr, 1):
            # Number of intervals ending strictly before l.
            # Strictness enforces that shared endpoints are overlapping.
            p = bisect_left(ends, l)

            for t in range(1, MAXT + 1):
                # Skip current interval.
                best_w = dp_w[t][i - 1]
                best_tup = dp_idx[t][i - 1]

                # Take current interval, combined with best exact (t-1) compatible prefix.
                prev_w = dp_w[t - 1][p]
                if prev_w >= 0:
                    cand_w = prev_w + w
                    prev_tup = dp_idx[t - 1][p]

                    # Insert idx into the small sorted tuple.
                    if t == 1:
                        cand_tup = (idx,)
                    elif t == 2:
                        a = prev_tup[0]
                        cand_tup = (idx, a) if idx < a else (a, idx)
                    elif t == 3:
                        a, b = prev_tup
                        if idx < a:
                            cand_tup = (idx, a, b)
                        elif idx < b:
                            cand_tup = (a, idx, b)
                        else:
                            cand_tup = (a, b, idx)
                    else:  # t == 4
                        a, b, c = prev_tup
                        if idx < a:
                            cand_tup = (idx, a, b, c)
                        elif idx < b:
                            cand_tup = (a, idx, b, c)
                        elif idx < c:
                            cand_tup = (a, b, idx, c)
                        else:
                            cand_tup = (a, b, c, idx)

                    if cand_w > best_w or (
                        cand_w == best_w and (best_tup is None or cand_tup < best_tup)
                    ):
                        best_w = cand_w
                        best_tup = cand_tup

                dp_w[t][i] = best_w
                dp_idx[t][i] = best_tup

        # Choose among using 0..4 intervals: maximum weight first, then lexicographically smallest tuple.
        best_w = NEG
        best_tup = None
        for t in range(MAXT + 1):
            w = dp_w[t][n]
            if w < 0:
                continue
            tup = dp_idx[t][n]
            if w > best_w or (w == best_w and (best_tup is None or tup < best_tup)):
                best_w = w
                best_tup = tup

        return list(best_tup) if best_tup is not None else []