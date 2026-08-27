from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        ending = [[] for _ in range(n + 1)]

        for idx, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            ending[b].append((a, idx))

        gains = [0] * m
        baseline = 0

        top_value = 0
        top_id = -1
        second_value = 0
        second_id = -1

        for right in range(1, n + 1):
            for left, idx in ending[right]:
                if left > top_value:
                    second_value, second_id = top_value, top_id
                    top_value, top_id = left, idx
                elif left > second_value:
                    second_value, second_id = left, idx

            baseline += right - top_value

            if top_id != -1 and top_value > second_value:
                gains[top_id] += top_value - second_value

        return baseline + max(gains)