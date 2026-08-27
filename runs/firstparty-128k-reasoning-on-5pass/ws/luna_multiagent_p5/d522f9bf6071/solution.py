from bisect import bisect_right
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        ordered = sorted(enumerate(intervals), key=lambda item: item[1][0])
        starts = [interval[0] for _, interval in ordered]

        # First sorted position whose start is strictly greater than the
        # current interval's end.
        next_pos = [0] * n
        for i, (_, interval) in enumerate(ordered):
            next_pos[i] = bisect_right(starts, interval[1])

        # dp_score[i][k] and dp_indices[i][k] represent the best result
        # obtainable from sorted position i onward using at most k intervals.
        dp_score = [[0] * 5 for _ in range(n + 1)]
        dp_indices = [[()] * 5 for _ in range(n + 1)]

        for i in range(n - 1, -1, -1):
            original_index, interval = ordered[i]
            weight = interval[2]
            following = next_pos[i]

            for capacity in range(5):
                best_score = dp_score[i + 1][capacity]
                best_indices = dp_indices[i + 1][capacity]

                if capacity > 0:
                    suffix_indices = dp_indices[following][capacity - 1]
                    take_score = weight + dp_score[following][capacity - 1]
                    take_indices = tuple(
                        sorted((original_index,) + suffix_indices)
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

                dp_score[i][capacity] = best_score
                dp_indices[i][capacity] = best_indices

        return list(dp_indices[0][4])