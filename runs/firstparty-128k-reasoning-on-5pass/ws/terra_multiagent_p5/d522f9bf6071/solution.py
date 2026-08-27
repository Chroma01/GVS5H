from typing import List
from bisect import bisect_right


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        # Store (start, end, weight, original_index), ordered by start.
        arr = sorted(
            (left, right, weight, i)
            for i, (left, right, weight) in enumerate(intervals)
        )
        starts = [item[0] for item in arr]

        # nxt[i]: first interval starting strictly after arr[i]'s end.
        # bisect_right is necessary because touching endpoints overlap.
        nxt = [0] * n
        for i in range(n):
            nxt[i] = bisect_right(starts, arr[i][1])

        # dp[i][k] = (best total score, sorted tuple of original indices)
        # using at most k intervals from arr[i:].
        dp = [[(0, ()) for _ in range(5)] for _ in range(n + 1)]

        for i in range(n - 1, -1, -1):
            _, _, weight, original_index = arr[i]

            for k in range(5):
                best = dp[i + 1][k]  # Do not take interval i.

                if k:
                    suffix_score, suffix_indices = dp[nxt[i]][k - 1]
                    candidate = (
                        suffix_score + weight,
                        tuple(sorted(suffix_indices + (original_index,))),
                    )

                    if (
                        candidate[0] > best[0]
                        or (
                            candidate[0] == best[0]
                            and candidate[1] < best[1]
                        )
                    ):
                        best = candidate

                dp[i][k] = best

        return list(dp[0][4][1])