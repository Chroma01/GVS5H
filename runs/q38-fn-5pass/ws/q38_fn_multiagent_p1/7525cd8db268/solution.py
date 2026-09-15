from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        if m == 0:
            return n * (n + 1) // 2

        buckets = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            if a < b:
                x, y = a, b
            else:
                x, y = b, a
            buckets[y].append((x, i))

        gains = [0] * m

        # max1: largest active smaller endpoint x
        # count1: number of active pairs having x == max1
        # owner: pair id if count1 == 1, otherwise -1
        # max2: second largest distinct active x value
        max1 = 0
        max2 = 0
        count1 = 0
        owner = -1

        base = 0

        for r in range(1, n + 1):
            # Activate all pairs whose larger endpoint is r.
            # Query only after the whole bucket is processed to handle ties
            # among pairs becoming active at the same right endpoint.
            for x, idx in buckets[r]:
                if x > max1:
                    max2 = max1
                    max1 = x
                    count1 = 1
                    owner = idx
                elif x == max1:
                    count1 += 1
                    owner = -1
                elif x > max2:
                    max2 = x

            # With all pairs present, valid left endpoints for right endpoint r
            # are max1 + 1 through r.
            base += r - max1

            # If exactly one active pair attains max1, removing it lowers the
            # bound from max1 to max2 for this r.
            if count1 == 1 and owner != -1:
                gains[owner] += max1 - max2

        return base + max(gains)