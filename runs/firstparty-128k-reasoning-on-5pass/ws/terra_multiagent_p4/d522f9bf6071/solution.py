from bisect import bisect_right
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        ordered = sorted(
            (left, right, weight, index)
            for index, (left, right, weight) in enumerate(intervals)
        )
        starts = [item[0] for item in ordered]
        jumps = [bisect_right(starts, right) for _, right, _, _ in ordered]

        # dp[k][i] = (maximum score, sorted tuple of original indices)
        # using at most k intervals from ordered[i:].
        dp = [[(0, ()) for _ in range(n + 1)] for _ in range(5)]

        for k in range(1, 5):
            current = dp[k]
            previous = dp[k - 1]

            for i in range(n - 1, -1, -1):
                skip_score, skip_indices = current[i + 1]

                _, _, weight, original_index = ordered[i]
                next_score, next_indices = previous[jumps[i]]
                take_indices = tuple(sorted(next_indices + (original_index,)))
                take_score = weight + next_score

                if take_score > skip_score or (
                    take_score == skip_score and take_indices < skip_indices
                ):
                    current[i] = (take_score, take_indices)
                else:
                    current[i] = (skip_score, skip_indices)

        return list(dp[4][0][1])