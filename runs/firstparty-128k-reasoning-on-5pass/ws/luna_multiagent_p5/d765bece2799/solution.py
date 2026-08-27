from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def triangle(x: int) -> int:
            if x <= 0:
                return 0
            return x * (x - 1) // 2

        def contribution(is_min: bool) -> int:
            prev = [-1] * n
            nxt = [n] * n

            stack = []
            for i, value in enumerate(nums):
                while stack:
                    top = stack[-1]
                    if (nums[top] >= value) if is_min else (nums[top] <= value):
                        stack.pop()
                    else:
                        break
                prev[i] = stack[-1] if stack else -1
                stack.append(i)

            stack = []
            for i in range(n - 1, -1, -1):
                value = nums[i]
                while stack:
                    top = stack[-1]
                    if (nums[top] > value) if is_min else (nums[top] < value):
                        stack.pop()
                    else:
                        break
                nxt[i] = stack[-1] if stack else n
                stack.append(i)

            limit = k + 1
            total = 0

            for i, value in enumerate(nums):
                left_choices = i - prev[i]
                right_choices = nxt[i] - i

                # Count positive pairs (a, b) such that:
                # a <= left_choices, b <= right_choices,
                # and a + b <= k + 1.
                count = (
                    triangle(limit)
                    - triangle(limit - left_choices)
                    - triangle(limit - right_choices)
                    + triangle(limit - left_choices - right_choices)
                )
                total += value * count

            return total

        return contribution(True) + contribution(False)