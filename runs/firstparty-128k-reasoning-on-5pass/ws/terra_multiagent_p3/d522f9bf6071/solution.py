from typing import List, Tuple
from bisect import bisect_right


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        ordered = sorted(
            (left, right, weight, index)
            for index, (left, right, weight) in enumerate(intervals)
        )
        starts = [item[0] for item in ordered]

        successors = [0] * n
        for i, (_, right, _, _) in enumerate(ordered):
            successors[i] = bisect_right(starts, right)

        # prev[i] stores the best result from sorted position i onward
        # using at most the previous number of selected intervals.
        prev: List[Tuple[int, Tuple[int, ...]]] = [(0, ()) for _ in range(n + 1)]

        for _ in range(4):
            curr: List[Tuple[int, Tuple[int, ...]]] = [(0, ()) for _ in range(n + 1)]

            for i in range(n - 1, -1, -1):
                # Do not choose the current interval.
                best_score, best_indices = curr[i + 1]

                # Choose it and continue at the first strictly non-overlapping interval.
                _, _, weight, original_index = ordered[i]
                next_score, next_indices = prev[successors[i]]
                take_score = weight + next_score
                take_indices = tuple(sorted(next_indices + (original_index,)))

                if take_score > best_score or (
                    take_score == best_score and take_indices < best_indices
                ):
                    curr[i] = (take_score, take_indices)
                else:
                    curr[i] = (best_score, best_indices)

            prev = curr

        return list(prev[0][1])