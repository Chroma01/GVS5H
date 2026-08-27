from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def count_pairs(left_choices: int, right_choices: int) -> int:
            # Choose a in [1, left_choices], b in [1, right_choices].
            # The corresponding subarray length is a + b - 1, requiring
            # a + b <= k + 1.
            max_left = min(left_choices, k)

            # For a <= k + 1 - right_choices, all right choices are valid.
            full = min(max_left, max(0, k + 1 - right_choices))
            result = full * right_choices

            # For remaining a, valid b choices are k + 1 - a.
            count = max_left - full
            if count:
                first = full + 1
                last = max_left
                result += count * (k + 1) - (first + last) * count // 2

            return result

        def contribution(is_maximum: bool) -> int:
            prev = [-1] * n
            nxt = [n] * n
            stack = []

            if is_maximum:
                # Rightmost equal maximum owns each subarray:
                # previous strictly greater, next greater-or-equal.
                for i, value in enumerate(nums):
                    while stack and nums[stack[-1]] <= value:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)

                stack.clear()

                for i in range(n - 1, -1, -1):
                    value = nums[i]
                    while stack and nums[stack[-1]] < value:
                        stack.pop()
                    if stack:
                        nxt[i] = stack[-1]
                    stack.append(i)
            else:
                # Rightmost equal minimum owns each subarray:
                # previous strictly smaller, next smaller-or-equal.
                for i, value in enumerate(nums):
                    while stack and nums[stack[-1]] >= value:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)

                stack.clear()

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