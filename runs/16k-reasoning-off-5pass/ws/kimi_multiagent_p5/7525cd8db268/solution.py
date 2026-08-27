from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Normalize each pair: u = min(a,b) + 1 (smallest allowed left endpoint contribution),
        # v = max(a,b) (pair becomes active once r >= v).
        m = len(conflictingPairs)
        buckets = [[] for _ in range(n + 1)]
        us = [0] * m
        for i, (a, b) in enumerate(conflictingPairs):
            if a < b:
                u, v = a + 1, b
            else:
                u, v = b + 1, a
            us[i] = u
            buckets[v].append(i)

        base = 0
        gain = [0] * m
        max1 = 0          # current maximum u (0 means no constraint, L = 1)
        max2 = 0          # current second distinct u
        cnt1 = 0          # number of active pairs achieving max1
        idx1 = -1         # index of the pair achieving max1 (valid when cnt1 == 1)

        for r in range(1, n + 1):
            for i in buckets[r]:
                u = us[i]
                if u > max1:
                    max2 = max1
                    max1 = u
                    cnt1 = 1
                    idx1 = i
                elif u == max1:
                    cnt1 += 1
                elif u > max2:
                    max2 = u
            # With all pairs active, smallest allowed left endpoint is max1 (since u = min+1,
            # and max1 == 0 corresponds to L = 1).
            base += r - max1 + 1
            # If exactly one pair attains the max, removing it relaxes L from max1 to max2.
            if cnt1 == 1:
                gain[idx1] += max1 - max2

        return base + max(gain)