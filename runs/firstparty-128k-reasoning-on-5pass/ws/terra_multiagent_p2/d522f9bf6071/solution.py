from bisect import bisect_left
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        # Store as (end, start, weight, original_index).
        ordered = sorted(
            (right, left, weight, index)
            for index, (left, right, weight) in enumerate(intervals)
        )
        ends = [end for end, _, _, _ in ordered]

        # pred[i] is the count of intervals ending strictly before
        # ordered[i] starts, so they form its compatible prefix.
        pred = [0] * n
        for i, (_, start, _, _) in enumerate(ordered):
            pred[i] = bisect_left(ends, start)

        empty = ()
        prev_weight = [0] * (n + 1)
        prev_choice = [empty] * (n + 1)

        for _ in range(4):
            cur_weight = [0] * (n + 1)
            cur_choice = [empty] * (n + 1)

            for i in range(1, n + 1):
                _, _, weight, original_index = ordered[i - 1]

                # Skip current interval.
                best_weight = cur_weight[i - 1]
                best_choice = cur_choice[i - 1]

                # Take current interval after a compatible selection
                # of at most one fewer interval.
                compatible_prefix = pred[i - 1]
                take_weight = prev_weight[compatible_prefix] + weight

                candidate = list(prev_choice[compatible_prefix])
                pos = 0
                while pos < len(candidate) and candidate[pos] < original_index:
                    pos += 1
                candidate.insert(pos, original_index)
                take_choice = tuple(candidate)

                if take_weight > best_weight or (
                    take_weight == best_weight and take_choice < best_choice
                ):
                    best_weight = take_weight
                    best_choice = take_choice

                cur_weight[i] = best_weight
                cur_choice[i] = best_choice

            prev_weight = cur_weight
            prev_choice = cur_choice

        return list(prev_choice[n])