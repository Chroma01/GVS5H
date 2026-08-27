from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        buckets = [[] for _ in range(n + 1)]

        for idx, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            buckets[b].append((a, idx))

        gains = [0] * m
        total = 0

        max_left = 0
        max_count = 0
        max_owner = -1
        second_left = 0

        for r in range(1, n + 1):
            for left, idx in buckets[r]:
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

            total += r - max_left

            if max_count == 1:
                gains[max_owner] += max_left - second_left

        return total + max(gains)