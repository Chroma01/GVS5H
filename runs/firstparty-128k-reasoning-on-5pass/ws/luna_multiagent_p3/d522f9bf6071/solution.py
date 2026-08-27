from bisect import bisect_right
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        ordered = sorted(
            (left, right, weight, index)
            for index, (left, right, weight) in enumerate(intervals)
        )

        starts = [left for left, _, _, _ in ordered]

        # Intervals must start strictly after the current interval ends.
        next_pos = [
            bisect_right(starts, ordered[i][1])
            for i in range(n)
        ]

        # dp_score[i][k] and dp_indices[i][k] represent the best result
        # using at most k intervals from sorted position i onward.
        dp_score = [[0] * 5 for _ in range(n + 1)]
        dp_indices = [[()] * 5 for _ in range(n + 1)]

        for i in range(n - 1, -1, -1):
            _, _, weight, original_index = ordered[i]
            nxt = next_pos[i]

            for k in range(1, 5):
                # Skip the current interval.
                best_score = dp_score[i + 1][k]
                best_indices = dp_indices[i + 1][k]

                # Take the current interval.
                take_score = weight + dp_score[nxt][k - 1]
                take_indices = tuple(
                    sorted((original_index,) + dp_indices[nxt][k - 1])
                )

                if (
                    take_score > best_score
                    or (
                        take_score == best_score
                        and take_indices < best_indices
                    )
                ):
                    best_score = take_score
                    best_indices = take_indices

                dp_score[i][k] = best_score
                dp_indices[i][k] = best_indices

        return list(dp_indices[0][4])