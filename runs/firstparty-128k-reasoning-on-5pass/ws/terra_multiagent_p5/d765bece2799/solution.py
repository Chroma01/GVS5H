from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def pair_count(left_choices: int, right_choices: int) -> int:
            left_choices = min(left_choices, k)
            right_choices = min(right_choices, k)

            total = left_choices * right_choices
            excess = left_choices + right_choices - k

            if excess > 1:
                total -= excess * (excess - 1) // 2

            return total

        def contribution_for_maximum() -> int:
            prev_greater = [-1] * n
            stack = []

            # Previous strictly greater.
            for i, value in enumerate(nums):
                while stack and nums[stack[-1]] <= value:
                    stack.pop()
                if stack:
                    prev_greater[i] = stack[-1]
                stack.append(i)

            next_greater_equal = [n] * n
            stack = []

            # Next greater-or-equal.
            for i in range(n - 1, -1, -1):
                value = nums[i]
                while stack and nums[stack[-1]] < value:
                    stack.pop()
                if stack:
                    next_greater_equal[i] = stack[-1]
                stack.append(i)

            result = 0
            for i, value in enumerate(nums):
                left_choices = i - prev_greater[i]
                right_choices = next_greater_equal[i] - i
                result += value * pair_count(left_choices, right_choices)

            return result

        def contribution_for_minimum() -> int:
            prev_smaller = [-1] * n
            stack = []

            # Previous strictly smaller.
            for i, value in enumerate(nums):
                while stack and nums[stack[-1]] >= value:
                    stack.pop()
                if stack:
                    prev_smaller[i] = stack[-1]
                stack.append(i)

            next_smaller_equal = [n] * n
            stack = []

            # Next smaller-or-equal.
            for i in range(n - 1, -1, -1):
                value = nums[i]
                while stack and nums[stack[-1]] > value:
                    stack.pop()
                if stack:
                    next_smaller_equal[i] = stack[-1]
                stack.append(i)

            result = 0
            for i, value in enumerate(nums):
                left_choices = i - prev_smaller[i]
                right_choices = next_smaller_equal[i] - i
                result += value * pair_count(left_choices, right_choices)

            return result

        return contribution_for_maximum() + contribution_for_minimum()