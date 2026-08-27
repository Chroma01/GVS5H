from bisect import bisect_left, bisect_right
from typing import List, Tuple


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        # Sort geometrically for weighted interval scheduling.
        ordered = sorted(
            (left, right, weight, index)
            for index, (left, right, weight) in enumerate(intervals)
        )
        starts = [item[0] for item in ordered]

        # next_pos[i] is the first interval starting strictly after interval i ends.
        next_pos = [0] * n
        for i, (_, right, _, _) in enumerate(ordered):
            next_pos[i] = bisect_right(starts, right)

        empty: Tuple[int, ...] = ()

        # prev[i] = best result using at most k-1 intervals from suffix i.
        prev: List[Tuple[int, Tuple[int, ...]]] = [(0, empty)] * (n + 1)

        for _ in range(1, 5):
            curr: List[Tuple[int, Tuple[int, ...]]] = [(0, empty)] * (n + 1)

            for i in range(n - 1, -1, -1):
                # Option 1: skip this interval.
                best_weight, best_indices = curr[i + 1]

                # Option 2: take this interval, then jump to compatible intervals.
                _, _, weight, original_index = ordered[i]
                future_weight, future_indices = prev[next_pos[i]]

                insert_at = bisect_left(future_indices, original_index)
                chosen_indices = (
                    future_indices[:insert_at]
                    + (original_index,)
                    + future_indices[insert_at:]
                )
                chosen_weight = weight + future_weight

                if (
                    chosen_weight > best_weight
                    or (
                        chosen_weight == best_weight
                        and chosen_indices < best_indices
                    )
                ):
                    curr[i] = (chosen_weight, chosen_indices)
                else:
                    curr[i] = (best_weight, best_indices)

            prev = curr

        return list(prev[0][1])