from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        byHi = [[] for _ in range(n + 2)]
        for i, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            byHi[b].append((a, i))

        gain = [0] * m
        total = 0
        m1 = 0          # largest lo among pairs with hi <= r
        m2 = 0          # second largest (multiset) lo
        owner = -1      # index of pair attaining m1

        for r in range(1, n + 1):
            for lo, i in byHi[r]:
                if lo > m1:
                    m2 = m1
                    m1 = lo
                    owner = i
                elif lo > m2:
                    m2 = lo
            total += r - m1
            if owner >= 0:
                gain[owner] += m1 - m2

        return total + (max(gain) if m else 0)