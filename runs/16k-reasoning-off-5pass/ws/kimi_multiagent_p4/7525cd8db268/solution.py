from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        max1 = [0] * (n + 1)   # largest a among pairs (a, b) with a < b, per b
        max2 = [0] * (n + 1)   # second largest a (strictly less than max1)
        cntMax = [0] * (n + 1) # how many pairs attain max1 at b

        for a, b in conflictingPairs:
            if a > b:
                a, b = b, a
            if a > max1[b]:
                max2[b] = max1[b]
                max1[b] = a
                cntMax[b] = 1
            elif a == max1[b]:
                cntMax[b] += 1
            elif a > max2[b]:
                max2[b] = a

        base = 0
        bestGain = 0
        for b in range(1, n + 1):
            base += b - max1[b]
            if cntMax[b] == 1:
                gain = max1[b] - max2[b]
                if gain > bestGain:
                    bestGain = gain

        return base + bestGain