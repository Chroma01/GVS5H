from bisect import bisect_left, bisect_right
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        ordered = sorted(enumerate(intervals), key=lambda item: item[1][0])
        starts = [item[1][0] for item in ordered]
        ends = [item[1][1] for item in ordered]
        weights = [item[1][2] for item in ordered]
        original_indices = [item[0] for item in ordered]

        # Intervals sharing a boundary overlap, so the next start must be
        # strictly greater than the current end.
        next_pos = [bisect_right(starts, ends[i]) for i in range(n)]

        neg_inf = -1

        # scores[k][i] and sequences[k][i] describe the best solution using
        # exactly k intervals from sorted positions i through n - 1.
        scores = [[neg_inf] * (n + 1) for _ in range(5)]
        sequences = [[None] * (n + 1) for _ in range(5)]

        for i in range(n + 1):
            scores[0][i] = 0
            sequences[0][i] = ()

        for i in range(n - 1, -1, -1):
            for k in range(1, 5):
                # Skip the current interval.
                best_score = scores[k][i + 1]
                best_sequence = sequences[k][i + 1]

                # Take the current interval.
                nxt = next_pos[i]
                suffix_score = scores[k - 1][nxt]

                if suffix_score != neg_inf:
                    index = original_indices[i]
                    suffix = sequences[k - 1][nxt]

                    # Keep selected original indices sorted for lexicographic
                    # comparison, regardless of start-position ordering.
                    insertion = bisect_left(suffix, index)
                    take_sequence = (
                        suffix[:insertion]
                        + (index,)
                        + suffix[insertion:]
                    )
                    take_score = weights[i] + suffix_score

                    if (
                        take_score > best_score
                        or (
                            take_score == best_score
                            and (
                                best_sequence is None
                                or take_sequence < best_sequence
                            )
                        )
                    ):
                        best_score = take_score
                        best_sequence = take_sequence

                scores[k][i] = best_score
                sequences[k][i] = best_sequence

        # Compare solutions containing exactly 0 through 4 intervals.
        answer_score = neg_inf
        answer_sequence = ()

        for k in range(5):
            sequence = sequences[k][0]
            if sequence is None:
                continue

            if (
                scores[k][0] > answer_score
                or (
                    scores[k][0] == answer_score
                    and sequence < answer_sequence
                )
            ):
                answer_score = scores[k][0]
                answer_sequence = sequence

        return list(answer_sequence)