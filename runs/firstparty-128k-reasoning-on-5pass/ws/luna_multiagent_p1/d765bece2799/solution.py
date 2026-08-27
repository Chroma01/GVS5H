from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        limit = k - 1

        def bounded_pairs(a: int, b: int) -> int:
            # Count pairs (x, y) such that:
            # 0 <= x < a, 0 <= y < b, and x + y <= limit.
            def unrestricted(width: int, s: int) -> int:
                if s < 0:
                    return 0
                q = min(width, s + 1)
                return q * (s + 1) - q * (q - 1) // 2

            # Remove pairs with y >= b by shifting y down by b.
            return unrestricted(a, limit) - unrestricted(a, limit - b)

        def extremum_sum(find_max: bool) -> int:
            left = [0] * n
            right = [0] * n

            stack = []

            # Previous strictly greater element for maxima,
            # or previous strictly smaller element for minima.
            for i, value in enumerate(nums):
                if find_max:
                    while stack and nums[stack[-1]] <= value:
                        stack.pop()
                else:
                    while stack and nums[stack[-1]] >= value:
                        stack.pop()

                left[i] = i - (stack[-1] if stack else -1)
                stack.append(i)

            stack = []

            # Next greater-or-equal element for maxima,
            # or next smaller-or-equal element for minima.
            for i in range(n - 1, -1, -1):
                value = nums[i]

                if find_max:
                    while stack and nums[stack[-1]] < value:
                        stack.pop()
                else:
                    while stack and nums[stack[-1]] > value:
                        stack.pop()

                right[i] = (stack[-1] if stack else n) - i
                stack.append(i)

            total = 0
            for i, value in enumerate(nums):
                total += value * bounded_pairs(left[i], right[i])

            return total

        return extremum_sum(True) + extremum_sum(False)