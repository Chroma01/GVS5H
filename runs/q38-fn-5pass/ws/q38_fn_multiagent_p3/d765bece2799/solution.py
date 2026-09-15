from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        limit = k - 1

        def tri(t: int) -> int:
            if t < 0:
                return 0
            return (t + 1) * (t + 2) // 2

        def count_pairs(a: int, b: int) -> int:
            # Count x in [0, a-1], y in [0, b-1] with x + y <= limit.
            return (
                tri(limit)
                - tri(limit - a)
                - tri(limit - b)
                + tri(limit - a - b)
            )

        # Minimum contributions: assign each subarray to its rightmost minimum.
        prev_less = [-1] * n
        stack = []
        for i, x in enumerate(nums):
            while stack and nums[stack[-1]] >= x:
                stack.pop()
            if stack:
                prev_less[i] = stack[-1]
            stack.append(i)

        next_le = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] > x:
                stack.pop()
            if stack:
                next_le[i] = stack[-1]
            stack.append(i)

        ans = 0
        for i, x in enumerate(nums):
            left_choices = i - prev_less[i]
            right_choices = next_le[i] - i
            ans += x * count_pairs(left_choices, right_choices)

        # Maximum contributions: assign each subarray to its rightmost maximum.
        prev_greater = [-1] * n
        stack = []
        for i, x in enumerate(nums):
            while stack and nums[stack[-1]] <= x:
                stack.pop()
            if stack:
                prev_greater[i] = stack[-1]
            stack.append(i)

        next_ge = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] < x:
                stack.pop()
            if stack:
                next_ge[i] = stack[-1]
            stack.append(i)

        for i, x in enumerate(nums):
            left_choices = i - prev_greater[i]
            right_choices = next_ge[i] - i
            ans += x * count_pairs(left_choices, right_choices)

        return ans