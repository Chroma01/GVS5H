from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        buckets = [[] for _ in range(n + 1)]

        for pair_id, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            buckets[b].append((a, pair_id))

        gains = [0] * len(conflictingPairs)

        max_left = 0
        second_left = 0
        max_count = 0
        unique_max_id = -1
        base = 0

        for right in range(1, n + 1):
            for left, pair_id in buckets[right]:
                if left > max_left:
                    second_left = max_left
                    max_left = left
                    max_count = 1
                    unique_max_id = pair_id
                elif left == max_left:
                    max_count += 1
                elif left > second_left:
                    second_left = left

            base += right - max_left

            if max_count == 1:
                gains[unique_max_id] += max_left - second_left

        return base + max(gains)