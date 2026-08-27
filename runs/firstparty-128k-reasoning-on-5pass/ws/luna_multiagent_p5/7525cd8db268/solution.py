from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        ending = [[] for _ in range(n + 1)]

        for idx, (a, b) in enumerate(conflictingPairs):
            l, r = (a, b) if a < b else (b, a)
            ending[r].append((l, idx))

        gains = [0] * m
        best_left = 0
        best_id = -1
        second_left = 0
        baseline = 0

        for r in range(1, n + 1):
            for left, idx in ending[r]:
                if left > best_left:
                    second_left = best_left
                    best_left = left
                    best_id = idx
                elif left > second_left:
                    second_left = left

            baseline += r - best_left

            if best_id != -1 and best_left > second_left:
                gains[best_id] += best_left - second_left

        return baseline + max(gains)