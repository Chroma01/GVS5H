from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        limit = k + 1

        def tri(t: int) -> int:
            # Number of positive integer pairs (x, y) with x + y <= t.
            if t < 2:
                return 0
            return t * (t - 1) // 2

        base = tri(limit)

        def count_pairs(a: int, b: int) -> int:
            # Count x, y with 1 <= x <= a, 1 <= y <= b, x + y <= limit.
            return (
                base
                - tri(limit - a)
                - tri(limit - b)
                + tri(limit - a - b)
            )

        # Previous strictly smaller element.
        prev_less = [-1] * n
        stack = []
        for i, x in enumerate(nums):
            while stack and nums[stack[-1]] >= x:
                stack.pop()
            if stack:
                prev_less[i] = stack[-1]
            stack.append(i)

        # Next smaller-or-equal element.
        next_le = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] > x:
                stack.pop()
            if stack:
                next_le[i] = stack[-1]
            stack.append(i)

        # Previous strictly greater element.
        prev_greater = [-1] * n
        stack = []
        for i, x in enumerate(nums):
            while stack and nums[stack[-1]] <= x:
                stack.pop()
            if stack:
                prev_greater[i] = stack[-1]
            stack.append(i)

        # Next greater-or-equal element.
        next_ge = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] < x:
                stack.pop()
            if stack:
                next_ge[i] = stack[-1]
            stack.append(i)

        ans = 0

        for i, x in enumerate(nums):
            # Contribution as the chosen minimum.
            left_min = i - prev_less[i]
            right_min = next_le[i] - i
            ans += x * count_pairs(left_min, right_min)

            # Contribution as the chosen maximum.
            left_max = i - prev_greater[i]
            right_max = next_ge[i] - i
            ans += x * count_pairs(left_max, right_max)

        return ans