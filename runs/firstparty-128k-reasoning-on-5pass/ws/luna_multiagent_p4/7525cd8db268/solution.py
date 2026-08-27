from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        events = [[] for _ in range(n + 1)]

        for index, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            events[b].append((a, index))

        gains = [0] * len(conflictingPairs)
        best_left = 0
        second_left = 0
        best_owner = -1
        baseline = 0

        for right in range(1, n + 1):
            for left, index in events[right]:
                if left > best_left:
                    second_left = best_left
                    best_left = left
                    best_owner = index
                elif left == best_left:
                    second_left = best_left
                elif left > second_left:
                    second_left = left

            baseline += right - best_left

            if best_owner != -1 and best_left > second_left:
                gains[best_owner] += best_left - second_left

        return baseline + max(gains)