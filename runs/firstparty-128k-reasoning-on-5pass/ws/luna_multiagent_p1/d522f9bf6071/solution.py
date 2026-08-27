from bisect import bisect_left
from typing import List


class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        items = sorted(
            (right, left, weight, index)
            for index, (left, right, weight) in enumerate(intervals)
        )
        ends = [right for right, _, _, _ in items]
        n = len(items)

        # dp[i][k] = (best score, lexicographically smallest tuple)
        # using exactly k intervals among the first i sorted intervals.
        dp = [[(0, ())] + [(-1, ()) for _ in range(4)]]

        for i, (right, left, weight, index) in enumerate(items):
            current = dp[i].copy()

            # Only intervals ending strictly before left are compatible.
            predecessor_count = bisect_left(ends, left)
            predecessor = dp[predecessor_count]

            for count in range(1, 5):
                previous_score, previous_indices = predecessor[count - 1]
                if previous_score < 0:
                    continue

                position = bisect_left(previous_indices, index)
                candidate_indices = (
                    previous_indices[:position]
                    + (index,)
                    + previous_indices[position:]
                )
                candidate_score = previous_score + weight

                best_score, best_indices = current[count]
                if (
                    candidate_score > best_score
                    or (
                        candidate_score == best_score
                        and candidate_indices < best_indices
                    )
                ):
                    current[count] = (candidate_score, candidate_indices)

            dp.append(current)

        best_score, best_indices = dp[n][0]
        for count in range(1, 5):
            score, indices = dp[n][count]
            if score > best_score or (
                score == best_score and indices < best_indices
            ):
                best_score, best_indices = score, indices

        return list(best_indices)