from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def count_pairs(left_choices: int, right_choices: int) -> int:
            # Choose offsets a and b:
            # 0 <= a < left_choices, 0 <= b < right_choices,
            # and resulting subarray length a + b + 1 is at most k.
            usable_left = min(left_choices, k)

            # For a <= k - right_choices, every b in [0, right_choices) works.
            full = k - right_choices + 1
            if full < 0:
                full = 0
            elif full > usable_left:
                full = usable_left

            remaining = usable_left - full
            # For remaining a values, number of valid b values is k - a.
            return (
                full * right_choices
                + remaining * k
                - (full + usable_left - 1) * remaining // 2
            )

        def contribution(is_minimum: bool) -> int:
            left = [0] * n
            right = [0] * n
            stack = []

            if is_minimum:
                # Assign equal minima to the rightmost occurrence:
                # previous strictly smaller, next smaller-or-equal.
                for i, value in enumerate(nums):
                    while stack and nums[stack[-1]] >= value:
                        stack.pop()
                    left[i] = i - (stack[-1] if stack else -1)
                    stack.append(i)

                stack.clear()
                for i in range(n - 1, -1, -1):
                    value = nums[i]
                    while stack and nums[stack[-1]] > value:
                        stack.pop()
                    right[i] = (stack[-1] if stack else n) - i
                    stack.append(i)
            else:
                # Assign equal maxima to the rightmost occurrence:
                # previous strictly greater, next greater-or-equal.
                for i, value in enumerate(nums):
                    while stack and nums[stack[-1]] <= value:
                        stack.pop()
                    left[i] = i - (stack[-1] if stack else -1)
                    stack.append(i)

                stack.clear()
                for i in range(n - 1, -1, -1):
                    value = nums[i]
                    while stack and nums[stack[-1]] < value:
                        stack.pop()
                    right[i] = (stack[-1] if stack else n) - i
                    stack.append(i)

            total = 0
            for i, value in enumerate(nums):
                total += value * count_pairs(left[i], right[i])
            return total

        return contribution(True) + contribution(False)