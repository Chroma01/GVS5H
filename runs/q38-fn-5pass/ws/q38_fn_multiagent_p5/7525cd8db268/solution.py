from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        if m == 0:
            return n * (n + 1) // 2

        buckets = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            buckets[b].append((a, i))

        total = 0
        gains = [0] * m

        top1 = 0          # largest active smaller endpoint
        top2 = 0          # second largest distinct active smaller endpoint
        count_top1 = 0    # number of active pairs with smaller endpoint == top1
        owner = -1        # pair index if count_top1 == 1, else -1

        for r in range(1, n + 1):
            # Activate all pairs whose larger endpoint is r before evaluating r.
            for x, idx in buckets[r]:
                if x > top1:
                    top2 = top1
                    top1 = x
                    count_top1 = 1
                    owner = idx
                elif x == top1:
                    count_top1 += 1
                    owner = -1
                elif x > top2:
                    top2 = x

            # If exactly one active pair attains the maximum threshold,
            # removing it lowers the threshold from top1 to top2.
            if count_top1 == 1 and owner != -1:
                gains[owner] += top1 - top2

            # Valid subarrays ending at r have left endpoint > top1.
            total += r - top1

        return total + max(gains)