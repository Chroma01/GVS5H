from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        q = k - 1

        def bounded_count(left_capacity: int, right_capacity: int) -> int:
            def triangle(s: int) -> int:
                if s < 0:
                    return 0
                return (s + 1) * (s + 2) // 2

            return (
                triangle(q)
                - triangle(q - left_capacity)
                - triangle(q - right_capacity)
                + triangle(q - left_capacity - right_capacity)
            )

        def contribution(is_minimum: bool) -> int:
            left = [-1] * n
            right = [n] * n
            stack = []

            if is_minimum:
                # Previous strictly smaller: equal values are assigned to the rightmost one.
                for i, value in enumerate(nums):
                    while stack and nums[stack[-1]] >= value:
                        stack.pop()
                    if stack:
                        left[i] = stack[-1]
                    stack.append(i)

                stack.clear()

                # Next smaller-or-equal.
                for i in range(n - 1, -1, -1):
                    while stack and nums[stack[-1]] > nums[i]:
                        stack.pop()
                    if stack:
                        right[i] = stack[-1]
                    stack.append(i)
            else:
                # Previous strictly larger: equal values are assigned to the rightmost one.
                for i, value in enumerate(nums):
                    while stack and nums[stack[-1]] <= value:
                        stack.pop()
                    if stack:
                        left[i] = stack[-1]
                    stack.append(i)

                stack.clear()

                # Next larger-or-equal.
                for i in range(n - 1, -1, -1):
                    while stack and nums[stack[-1]] < nums[i]:
                        stack.pop()
                    if stack:
                        right[i] = stack[-1]
                    stack.append(i)

            total = 0
            for i, value in enumerate(nums):
                left_capacity = i - left[i]
                right_capacity = right[i] - i
                total += value * bounded_count(left_capacity, right_capacity)

            return total

        return contribution(True) + contribution(False)