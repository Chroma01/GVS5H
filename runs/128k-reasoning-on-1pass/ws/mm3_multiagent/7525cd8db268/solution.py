from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        """
        For each index i (treated as the right end of a subarray) the only restriction
        comes from pairs whose larger endpoint is i.  Let L = min(a,b) and R = max(a,b)
        for a conflicting pair.  For a subarray ending at i we need its start > L for
        every pair with R <= i.  Hence the most restrictive start is
            M[i] = max { L | there exists a pair with R <= i and L = min(pair) }.
        The number of valid subarrays ending at i (with all pairs) is i - M[i].

        While scanning i = 1 … n we keep the two largest L values among all pairs with
        R <= i:  max1 = M[i] and max2 = the second largest L.  Deleting the pair that
        currently contributes max1 improves the count for i from (i - max1) to
        (i - max2), i.e. a gain of (max1 - max2).  The best deletion corresponds to
        the largest total gain over a contiguous segment where the same pair is the
        max1.  This is tracked by resetting a running extra sum whenever max1 changes.

        Complexity: O(n + m) time, O(n + m) memory (m = len(conflictingPairs)).
        """
        # Build a list of left endpoints for each right endpoint.
        lefts = [[] for _ in range(n + 1)]          # lefts[R] contains all L for this R
        for a, b in conflictingPairs:
            if a < b:
                L, R = a, b
            else:
                L, R = b, a
            lefts[R].append(L)

        max1 = 0          # largest L seen so far (M[i])
        max2 = 0          # second largest L seen so far
        base = 0          # sum of i - max1 over all i (valid subarrays with all pairs)
        cur_extra = 0     # accumulated gain for the current max1 segment
        max_extra = 0     # best possible extra gain by deleting one pair

        for i in range(1, n + 1):
            old_max1 = max1
            # Incorporate all pairs whose right endpoint equals i.
            for L in lefts[i]:
                if L > max1:
                    max2 = max1
                    max1 = L
                elif L > max2:
                    max2 = L

            # All subarrays ending at i that satisfy every remaining pair.
            base += i - max1

            # If the pair that gives max1 has changed, start a new segment.
            if max1 != old_max1:
                cur_extra = 0

            # Gain obtained by deleting the pair that currently contributes max1.
            extra = max1 - max2
            cur_extra += extra
            if cur_extra > max_extra:
                max_extra = cur_extra

        return base + max_extra