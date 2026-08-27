from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        if m == 0:
            return n * (n + 1) // 2

        by_r = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            if a < b:
                l, r = a, b
            else:
                l, r = b, a
            by_r[r].append((l, i))

        gain = [0] * m
        max1 = 0
        max2 = 0
        cnt1 = 0
        uid = -1
        base = 0

        for r in range(1, n + 1):
            for l, i in by_r[r]:
                if l > max1:
                    max2 = max1
                    max1 = l
                    cnt1 = 1
                    uid = i
                elif l == max1:
                    cnt1 += 1
                    uid = -1
                elif l > max2:
                    max2 = l

            base += r - max1
            if cnt1 == 1:
                gain[uid] += max1 - max2

        return base + max(gain)