from typing import List
from bisect import bisect_left

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        def insert_index(t, x):
            if not t:
                return (x,)
            if len(t) == 1:
                if x < t[0]:
                    return (x, t[0])
                return (t[0], x)
            if len(t) == 2:
                if x < t[0]:
                    return (x, t[0], t[1])
                if x < t[1]:
                    return (t[0], x, t[1])
                return (t[0], t[1], x)
            if x < t[0]:
                return (x, t[0], t[1], t[2])
            if x < t[1]:
                return (t[0], x, t[1], t[2])
            if x < t[2]:
                return (t[0], t[1], x, t[2])
            return (t[0], t[1], t[2], x)

        n = len(intervals)
        arr = [(r, l, w, i) for i, (l, r, w) in enumerate(intervals)]
        arr.sort()
        ends = [item[0] for item in arr]

        dp = [[None] * 5 for _ in range(n + 1)]
        dp[0][0] = (0, ())

        for i, (r, l, w, idx) in enumerate(arr, 1):
            p = bisect_left(ends, l, 0, i - 1)
            prev_row = dp[i - 1]
            cur_row = dp[i]
            cur_row[0] = prev_row[0]
            compat_row = dp[p]

            for j in range(1, 5):
                best = prev_row[j]
                prev = compat_row[j - 1]

                if prev is not None:
                    cand_score = prev[0] + w

                    if best is None or cand_score > best[0]:
                        best = (cand_score, insert_index(prev[1], idx))
                    elif cand_score == best[0]:
                        nt = insert_index(prev[1], idx)
                        if nt < best[1]:
                            best = (cand_score, nt)

                cur_row[j] = best

        best = None
        for j in range(5):
            state = dp[n][j]
            if state is None:
                continue
            if (
                best is None
                or state[0] > best[0]
                or (state[0] == best[0] and state[1] < best[1])
            ):
                best = state

        return list(best[1]) if best is not None else []