from bisect import bisect_right
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)

        ordered = sorted(
            (
                (left, right, weight, index)
                for index, (left, right, weight) in enumerate(intervals)
            ),
            key=lambda item: item[0],
        )

        starts = [item[0] for item in ordered]

        next_pos = [0] * n
        for i, (_, right, _, _) in enumerate(ordered):
            next_pos[i] = bisect_right(starts, right)

        scores = [[0] * 5 for _ in range(n + 1)]
        choices = [[()] * 5 for _ in range(n + 1)]

        for i in range(n - 1, -1, -1):
            _, _, weight, original_index = ordered[i]

            scores[i] = scores[i + 1].copy()
            choices[i] = choices[i + 1].copy()

            jump = next_pos[i]

            for limit in range(1, 5):
                take_score = weight + scores[jump][limit - 1]
                suffix_choice = choices[jump][limit - 1]

                insert_pos = bisect_right(suffix_choice, original_index)
                take_choice = (
                    suffix_choice[:insert_pos]
                    + (original_index,)
                    + suffix_choice[insert_pos:]
                )

                skip_score = scores[i][limit]
                skip_choice = choices[i][limit]

                if (
                    take_score > skip_score
                    or (
                        take_score == skip_score
                        and take_choice < skip_choice
                    )
                ):
                    scores[i][limit] = take_score
                    choices[i][limit] = take_choice

        return list(choices[0][4])