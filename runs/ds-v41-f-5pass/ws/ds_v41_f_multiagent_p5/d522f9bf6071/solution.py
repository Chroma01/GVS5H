from typing import List
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # (right, left, weight, original_index), sorted by right endpoint.
        items = sorted((r, l, w, i) for i, (l, r, w) in enumerate(intervals))
        r_list = [it[0] for it in items]
        w_list = [it[2] for it in items]
        idx_list = [it[3] for it in items]

        # pred[i] = number of sorted intervals with right endpoint < left of interval i,
        # i.e. exactly the intervals fully compatible (placed before) interval i.
        pred = [0] * (n + 1)
        for i in range(1, n + 1):
            pred[i] = bisect_left(r_list, items[i - 1][1])

        # prev_row is dp[k-1]; dp[0] = choose nothing with score 0 and empty tuple.
        prev_row = [(0, ())] * (n + 1)
        ans_score, ans_idx = -1, ()

        for k in range(1, 5):
            cur_row = [(-1, None)] * (n + 1)  # (-1, None) = unreachable state
            for i in range(1, n + 1):
                best = cur_row[i - 1]  # skip interval i
                p = pred[i]
                ps, pidx = prev_row[p]
                if pidx is not None:  # a valid k-1 selection compatible with i exists
                    new_idx = tuple(sorted(pidx + (idx_list[i - 1],)))
                    cand = (ps + w_list[i - 1], new_idx)
                    if cand[0] > best[0] or (cand[0] == best[0] and cand[1] < best[1]):
                        best = cand
                cur_row[i] = best

            score, idx_tuple = cur_row[n]
            if idx_tuple is not None and (
                score > ans_score
                or (score == ans_score and idx_tuple < ans_idx)
            ):
                ans_score, ans_idx = score, idx_tuple
            prev_row = cur_row

        return list(ans_idx)