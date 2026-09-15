from typing import List
from bisect import bisect_left


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Keep original 0-based index; sort by right endpoint.
        arr = [(l, r, w, i) for i, (l, r, w) in enumerate(intervals)]
        arr.sort(key=lambda x: x[1])
        rs = [x[1] for x in arr]

        # dp[i][c] = best (weight, sorted_index_tuple) using EXACTLY c intervals
        # among the first i intervals of the right-endpoint-sorted order.
        dp = [[None] * 5 for _ in range(n + 1)]
        dp[0][0] = (0, ())

        for i in range(1, n + 1):
            l, r, w, idx = arr[i - 1]
            dp[i][0] = (0, ())
            p = bisect_left(rs, l)  # count of intervals with right endpoint < l
            for c in range(1, min(4, i) + 1):
                best = dp[i - 1][c]          # do not use interval i
                prev = dp[p][c - 1]          # best among strictly-left intervals
                if prev is not None:
                    pw, pt = prev
                    lst = list(pt)
                    j = 0
                    while j < len(lst) and lst[j] < idx:
                        j += 1
                    lst.insert(j, idx)
                    cand = (pw + w, tuple(lst))
                    if (best is None or cand[0] > best[0]
                            or (cand[0] == best[0] and cand[1] < best[1])):
                        best = cand
                dp[i][c] = best

        # Best over choosing exactly 0..4 intervals.
        best_state = None
        for c in range(5):
            st = dp[n][c]
            if st is not None and (best_state is None or st[0] > best_state[0]
                                   or (st[0] == best_state[0] and st[1] < best_state[1])):
                best_state = st
        return list(best_state[1])