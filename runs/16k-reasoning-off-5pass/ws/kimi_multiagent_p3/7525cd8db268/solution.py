from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        # Bucket pairs by their right endpoint (max of the two values).
        buckets = [[] for _ in range(n + 1)]
        for i, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            # now a < b; subarray contains both iff l <= a and r >= b
            buckets[b].append((a, i))

        best = 0        # largest forbidden left boundary f(r)
        second = 0      # second largest boundary value (any pair, incl. duplicates)
        best_idx = -1   # index of a pair achieving `best`
        base = 0
        gain = [0] * m

        for r in range(1, n + 1):
            for left, idx in buckets[r]:
                if left > best:
                    second = best
                    best = left
                    best_idx = idx
                elif left > second:
                    # covers duplicates of best as well (left == best > second)
                    second = left
            base += r - best
            if best_idx != -1:
                gain[best_idx] += best - second

        return base + (max(gain) if m else 0)