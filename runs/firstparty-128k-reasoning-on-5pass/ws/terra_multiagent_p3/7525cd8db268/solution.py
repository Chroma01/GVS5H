from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        buckets = [[] for _ in range(n + 1)]

        for idx, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            buckets[b].append((a, idx))

        gains = [0] * len(conflictingPairs)

        max_left = 0
        second_left = 0
        max_count = 0
        max_owner = -1
        baseline = 0

        for right in range(1, n + 1):
            for left, idx in buckets[right]:
                if left > max_left:
                    second_left = max_left
                    max_left = left
                    max_count = 1
                    max_owner = idx
                elif left == max_left:
                    max_count += 1
                    max_owner = -1
                elif left > second_left:
                    second_left = left

            baseline += right - max_left

            if max_count == 1:
                gains[max_owner] += max_left - second_left

        return baseline + max(gains)