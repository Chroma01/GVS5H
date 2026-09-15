from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        if m == 0:
            return n * (n + 1) // 2

        buckets = [[] for _ in range(n + 1)]

        for idx, (x, y) in enumerate(conflictingPairs):
            if x > y:
                x, y = y, x
            buckets[x].append((y, idx))

        gains = [0] * m

        sentinel = n + 1
        min_b = sentinel
        min_count = 0
        min_id = -1
        second_b = sentinel

        baseline = 0

        for left in range(n, 0, -1):
            for b, idx in buckets[left]:
                if b < min_b:
                    second_b = min_b
                    min_b = b
                    min_count = 1
                    min_id = idx
                elif b == min_b:
                    min_count += 1
                    min_id = -1
                elif b < second_b:
                    second_b = b

            if min_b == sentinel:
                baseline += sentinel - left
            else:
                baseline += min_b - left
                if min_count == 1:
                    gains[min_id] += second_b - min_b

        return baseline + max(gains)