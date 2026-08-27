from typing import List


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        NEG = -10**30

        # A summary is:
        # (length, total_sum, best_prefix, best_suffix, best_subarray)
        EMPTY = (0, 0, NEG, NEG, NEG)

        def merge(a, b):
            if a[0] == 0:
                return b
            if b[0] == 0:
                return a

            length = a[0] + b[0]
            total = a[1] + b[1]
            prefix = max(a[2], a[1] + b[2])
            suffix = max(b[3], b[1] + a[3])
            best = max(a[4], b[4], a[3] + b[2])
            return (length, total, prefix, suffix, best)

        size = 1
        while size < n:
            size <<= 1

        tree = [EMPTY] * (2 * size)

        for i, value in enumerate(nums):
            tree[size + i] = (1, value, value, value, value)

        for i in range(size - 1, 0, -1):
            tree[i] = merge(tree[i << 1], tree[i << 1 | 1])

        def query(left: int, right: int):
            """Return the summary of nums[left:right]."""
            if left >= right:
                return EMPTY

            left += size
            right += size
            left_result = EMPTY
            right_result = EMPTY

            while left < right:
                if left & 1:
                    left_result = merge(left_result, tree[left])
                    left += 1
                if right & 1:
                    right -= 1
                    right_result = merge(tree[right], right_result)
                left >>= 1
                right >>= 1

            return merge(left_result, right_result)

        positions = {}
        for i, value in enumerate(nums):
            positions.setdefault(value, []).append(i)

        answer = tree[1][4]  # No deletion.

        for value, occurrence_positions in positions.items():
            if len(occurrence_positions) == n:
                # Deleting this value would leave an empty array.
                continue

            combined = EMPTY
            previous_end = 0

            for position in occurrence_positions:
                # This block contains no occurrence of 'value'.
                combined = merge(combined, query(previous_end, position))
                previous_end = position + 1

            combined = merge(combined, query(previous_end, n))

            if combined[0] > 0:
                answer = max(answer, combined[4])

        return answer