from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        by_right = [[] for _ in range(n + 1)]

        for idx, (a, b) in enumerate(conflictingPairs):
            left, right = (a, b) if a < b else (b, a)
            by_right[right].append((left, idx))

        gains = [0] * m
        best_left = 0
        best_id = -1
        second_left = 0
        second_id = -1
        baseline = 0

        for right in range(1, n + 1):
            for left, idx in by_right[right]:
                if left > best_left:
                    second_left, second_id = best_left, best_id
                    best_left, best_id = left, idx
                elif left > second_left:
                    second_left, second_id = left, idx

            baseline += right - best_left

            if best_id != -1:
                gains[best_id] += best_left - second_left

        return baseline + max(gains)