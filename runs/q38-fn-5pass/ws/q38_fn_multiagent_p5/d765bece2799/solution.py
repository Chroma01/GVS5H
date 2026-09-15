from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def count_pairs(left_span: int, right_span: int, limit: int) -> int:
            """
            Count pairs (a, b) such that:
              0 <= a < left_span
              0 <= b < right_span
              a + b <= limit
            """
            if limit < 0:
                return 0

            # Maximum possible a + b is (left_span - 1) + (right_span - 1).
            if limit >= left_span + right_span - 2:
                return left_span * right_span

            # Only a values up to m can contribute.
            m = left_span - 1
            if limit < m:
                m = limit

            # For a <= limit - right_span + 1, all right_span choices are valid.
            full_end = limit - right_span + 1
            if full_end > m:
                full_end = m

            total = 0
            if full_end >= 0:
                total = (full_end + 1) * right_span
                start = full_end + 1
            else:
                start = 0

            # Remaining a values contribute (limit - a + 1) choices.
            if start <= m:
                cnt = m - start + 1
                first = limit - start + 1
                last = limit - m + 1
                total += cnt * (first + last) // 2

            return total

        def sum_min(arr: List[int]) -> int:
            n = len(arr)

            # prev_less[i] = nearest index j < i with arr[j] < arr[i], or -1.
            prev_less = [-1] * n
            stack = []
            for i, x in enumerate(arr):
                while stack and arr[stack[-1]] >= x:
                    stack.pop()
                if stack:
                    prev_less[i] = stack[-1]
                stack.append(i)

            # next_less_equal[i] = nearest index j > i with arr[j] <= arr[i], or n.
            next_less_equal = [n] * n
            stack = []
            for i in range(n - 1, -1, -1):
                x = arr[i]
                while stack and arr[stack[-1]] > x:
                    stack.pop()
                if stack:
                    next_less_equal[i] = stack[-1]
                stack.append(i)

            limit = k - 1
            total = 0
            cp = count_pairs

            for i, x in enumerate(arr):
                left_span = i - prev_less[i]
                right_span = next_less_equal[i] - i
                total += x * cp(left_span, right_span, limit)

            return total

        # Sum of minima plus sum of maxima.
        # Sum of maxima of nums equals -sum of minima of -nums.
        return sum_min(nums) - sum_min([-x for x in nums])