from typing import List, Optional, Tuple


class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        # Each summary is:
        # (total_sum, maximum_prefix_sum, maximum_suffix_sum, maximum_subarray_sum)
        Summary = Tuple[int, int, int, int]

        def merge(a: Optional[Summary], b: Optional[Summary]) -> Optional[Summary]:
            if a is None:
                return b
            if b is None:
                return a

            total_a, pref_a, suff_a, best_a = a
            total_b, pref_b, suff_b, best_b = b

            total = total_a + total_b
            pref = max(pref_a, total_a + pref_b)
            suff = max(suff_b, total_b + suff_a)
            best = max(best_a, best_b, suff_a + pref_b)
            return total, pref, suff, best

        n = len(nums)
        size = 1
        while size < n:
            size <<= 1

        tree: List[Optional[Summary]] = [None] * (2 * size)

        for i, value in enumerate(nums):
            tree[size + i] = (value, value, value, value)

        for i in range(size - 1, 0, -1):
            tree[i] = merge(tree[i << 1], tree[i << 1 | 1])

        def query(left: int, right: int) -> Optional[Summary]:
            """Return summary for nums[left:right], preserving element order."""
            left += size
            right += size
            result_left: Optional[Summary] = None
            result_right: Optional[Summary] = None

            while left < right:
                if left & 1:
                    result_left = merge(result_left, tree[left])
                    left += 1
                if right & 1:
                    right -= 1
                    result_right = merge(tree[right], result_right)
                left >>= 1
                right >>= 1

            return merge(result_left, result_right)

        answer = tree[1][3]

        positions = {}
        for i, value in enumerate(nums):
            if value < 0:
                positions.setdefault(value, []).append(i)

        for occurrences in positions.values():
            combined: Optional[Summary] = None
            previous = 0

            for index in occurrences:
                if previous < index:
                    combined = merge(combined, query(previous, index))
                previous = index + 1

            if previous < n:
                combined = merge(combined, query(previous, n))

            if combined is not None:
                answer = max(answer, combined[3])

        return answer