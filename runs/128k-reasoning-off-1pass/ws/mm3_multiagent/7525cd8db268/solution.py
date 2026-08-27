from typing import List
import collections

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # For each position i (1..n), collect the smaller endpoint of all pairs
        # whose larger endpoint equals i.
        # We need for each i the largest two distinct smaller endpoints.
        candidates = [[] for _ in range(n + 1)]  # 1-indexed
        for a, b in conflictingPairs:
            if a > b:
                a, b = b, a
            # Now a < b, the larger endpoint is b.
            candidates[b].append(a)
        
        max1 = [0] * (n + 1)  # largest smaller endpoint for position i
        max2 = [0] * (n + 1)  # second largest distinct smaller endpoint
        
        for i in range(1, n + 1):
            lst = candidates[i]
            if not lst:
                continue
            # Sort descending to easily get top two distinct values
            lst.sort(reverse=True)
            max1[i] = lst[0]
            # Find the first value strictly less than max1[i]
            for v in lst[1:]:
                if v < max1[i]:
                    max2[i] = v
                    break
        
        # Base total: sum over i of (i - max1[i])
        base = 0
        for i in range(1, n + 1):
            base += i - max1[i]
        
        # Evaluate gain for removing each original pair.
        # The gain is non-zero only if the removed pair contributed to max1[i] for its larger endpoint i.
        max_gain = 0
        for a, b in conflictingPairs:
            # Determine which is larger
            if a > b:
                a, b = b, a
            # Now a < b; the pair affects position b.
            if max1[b] == a:
                # Gain = max1[b] - max2[b]
                gain = max1[b] - max2[b]
                if gain > max_gain:
                    max_gain = gain
        
        return base + max_gain