from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        events = [[] for _ in range(n + 1)]

        for idx, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            events[b].append((a, idx))

        m = len(conflictingPairs)
        gains = [0] * m

        max_left = 0
        second_left = 0
        max_count = 0
        max_id = -1
        baseline = 0

        for right in range(1, n + 1):
            for left, idx in events[right]:
                if left > max_left:
                    second_left = max_left
                    max_left = left
                    max_count = 1
                    max_id = idx
                elif left == max_left:
                    max_count += 1
                    max_id = -1
                elif left > second_left:
                    second_left = left

            baseline += right - max_left

            if max_count == 1:
                gains[max_id] += max_left - second_left

        return baseline + max(gains)