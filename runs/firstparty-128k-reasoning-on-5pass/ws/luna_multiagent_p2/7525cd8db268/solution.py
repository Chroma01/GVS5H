from typing import List


class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        by_right = [[] for _ in range(n + 1)]

        for idx, pair in enumerate(conflictingPairs):
            a, b = pair
            if a > b:
                a, b = b, a
            by_right[b].append((a, idx))

        # The two largest active lower endpoints, stored as (value, pair_id).
        # A value of 0 represents no active restriction.
        first_val, first_id = 0, -1
        second_val, second_id = 0, -1

        gains = [0] * len(conflictingPairs)
        baseline = 0

        for right in range(1, n + 1):
            for low, pair_id in by_right[right]:
                if low > first_val:
                    second_val, second_id = first_val, first_id
                    first_val, first_id = low, pair_id
                elif low > second_val:
                    second_val, second_id = low, pair_id

            # Without removing a pair, starts 1..first_val are invalid.
            baseline += right - first_val

            # Removing the unique pair supplying first_val exposes second_val.
            # If another pair has the same first_val, second_val equals it and
            # the gain is correctly zero.
            if first_id != -1:
                gains[first_id] += first_val - second_val

        return baseline + max(gains)