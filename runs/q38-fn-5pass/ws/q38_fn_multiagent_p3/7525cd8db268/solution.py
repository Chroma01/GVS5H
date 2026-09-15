from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        buckets = [[] for _ in range(n + 1)]

        for idx, (a, b) in enumerate(conflictingPairs):
            if a < b:
                lo, hi = a, b
            else:
                lo, hi = b, a
            buckets[hi].append((lo, idx))

        gains = [0] * m

        max_lo = 0
        second_lo = 0
        max_count = 0
        unique_id = -1

        base_valid = 0

        for r in range(1, n + 1):
            # Insert all pairs whose right endpoint is r before evaluating r.
            for lo, idx in buckets[r]:
                if lo > max_lo:
                    second_lo = max_lo
                    max_lo = lo
                    max_count = 1
                    unique_id = idx
                elif lo == max_lo:
                    max_count += 1
                    unique_id = -1
                elif lo > second_lo:
                    second_lo = lo

            base_valid += r - max_lo

            # If one active pair uniquely determines the strongest constraint,
            # removing it relaxes the constraint from max_lo to second_lo.
            if max_count == 1 and unique_id != -1:
                gains[unique_id] += max_lo - second_lo

        max_gain = max(gains) if gains else 0
        return base_valid + max_gain