from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def count_pairs(left_choices: int, right_choices: int) -> int:
            # Count pairs (a, b) where:
            # 1 <= a <= left_choices
            # 1 <= b <= right_choices
            # a + b - 1 <= k
            upper_left = min(left_choices, k)

            # For a <= k + 1 - right_choices, every b in [1, right_choices]
            # is valid.
            full_count = min(upper_left, max(0, k + 1 - right_choices))
            result = full_count * right_choices

            # For all remaining a, valid b values are [1, k + 1 - a].
            remaining = upper_left - full_count
            if remaining:
                first_a = full_count + 1
                last_a = upper_left
                result += remaining * (k + 1) - (first_a + last_a) * remaining // 2

            return result

        def contribution(is_maximum: bool) -> int:
            prev = [-1] * n
            nxt = [n] * n
            stack = []

            if is_maximum:
                # Previous strictly greater element.
                for i, value in enumerate(nums):
                    while stack and nums[stack[-1]] <= value:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)

                stack.clear()

                # Next greater-or-equal element.
                for i in range(n - 1, -1, -1):
                    value = nums[i]
                    while stack and nums[stack[-1]] < value:
                        stack.pop()
                    if stack:
                        nxt[i] = stack[-1]
                    stack.append(i)
            else:
                # Previous strictly smaller element.
                for i, value in enumerate(nums):
                    while stack and nums[stack[-1]] >= value:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)

                stack.clear()

                # Next smaller-or-equal element.
                for i in range(n - 1, -1, -1):
                    value = nums[i]
                    while stack and nums[stack[-1]] > value:
                        stack.pop()
                    if stack:
                        nxt[i] = stack[-1]
                    stack.append(i)

            total = 0
            for i, value in enumerate(nums):
                left_choices = i - prev[i]
                right_choices = nxt[i] - i
                total += value * count_pairs(left_choices, right_choices)

            return total

        return contribution(True) + contribution(False)