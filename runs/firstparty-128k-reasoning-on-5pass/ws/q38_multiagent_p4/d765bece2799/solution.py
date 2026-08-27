from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        def count_valid_extensions(left_len: int, right_len: int, k: int) -> int:
            # Count pairs (x, y) with:
            # 1 <= x <= left_len, 1 <= y <= right_len,
            # x + y - 1 <= k  <=>  x + y <= k + 1.
            K = k + 1

            # x must be at most K - 1 so that y >= 1 is possible.
            X = left_len
            limit = K - 1
            if X > limit:
                X = limit
            if X <= 0:
                return 0

            # For x <= K - right_len, the full right_len choices are valid.
            t = K - right_len
            if t > X:
                t = X
            elif t < 0:
                t = 0

            ans = t * right_len

            # For the remaining x values, valid y count is K - x.
            if X > t:
                ans += (X - t) * K - (X * (X + 1) - t * (t + 1)) // 2

            return ans

        total = 0
        count = count_valid_extensions

        # Minimum contributions.
        # Assign each subarray to its rightmost minimum:
        # previous strictly smaller, next smaller-or-equal.
        next_bound = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            v = nums[i]
            while stack and nums[stack[-1]] > v:
                stack.pop()
            next_bound[i] = stack[-1] if stack else n
            stack.append(i)

        stack = []
        for i, v in enumerate(nums):
            while stack and nums[stack[-1]] >= v:
                stack.pop()
            left_len = i - (stack[-1] if stack else -1)
            right_len = next_bound[i] - i
            total += v * count(left_len, right_len, k)
            stack.append(i)

        # Maximum contributions.
        # Assign each subarray to its rightmost maximum:
        # previous strictly greater, next greater-or-equal.
        next_bound = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            v = nums[i]
            while stack and nums[stack[-1]] < v:
                stack.pop()
            next_bound[i] = stack[-1] if stack else n
            stack.append(i)

        stack = []
        for i, v in enumerate(nums):
            while stack and nums[stack[-1]] <= v:
                stack.pop()
            left_len = i - (stack[-1] if stack else -1)
            right_len = next_bound[i] - i
            total += v * count(left_len, right_len, k)
            stack.append(i)

        return total