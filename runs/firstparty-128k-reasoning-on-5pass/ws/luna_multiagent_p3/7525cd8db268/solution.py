from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        by_right = [[] for _ in range(n + 1)]

        for pair_id, (a, b) in enumerate(conflictingPairs):
            left, right = (a, b) if a < b else (b, a)
            by_right[right].append((left, pair_id))

        gains = [0] * len(conflictingPairs)

        largest = 0
        second_largest = 0
        largest_count = 0
        largest_id = -1
        baseline = 0

        for right in range(1, n + 1):
            for left, pair_id in by_right[right]:
                if left > largest:
                    second_largest = largest
                    largest = left
                    largest_count = 1
                    largest_id = pair_id
                elif left == largest:
                    largest_count += 1
                elif left > second_largest:
                    second_largest = left

            baseline += right - largest

            if largest_count == 1:
                gains[largest_id] += largest - second_largest

        return baseline + max(gains)