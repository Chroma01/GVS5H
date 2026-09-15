from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        def count_valid(left_choices: int, right_choices: int, max_len: int) -> int:
            """
            Count pairs (p, q) such that:
              1 <= p <= left_choices
              1 <= q <= right_choices
              p + q - 1 <= max_len
            """
            if max_len <= 0:
                return 0

            # p cannot exceed max_len because q >= 1.
            m = min(left_choices, max_len)
            if m <= 0:
                return 0

            # For p <= max_len - right_choices + 1, q can take all right_choices values.
            full = min(m, max_len - right_choices + 1)
            if full < 0:
                full = 0

            total = full * right_choices

            # Remaining p values have q capped by max_len - p + 1.
            if m > full:
                cnt = m - full
                total += cnt * (max_len + 1) - (
                    m * (m + 1) // 2 - full * (full + 1) // 2
                )

            return total

        def sum_min() -> int:
            # Assign each subarray minimum to its leftmost occurrence.
            # For element i to be the chosen minimum:
            #   left boundary: previous index with value <= nums[i]
            #   right boundary: next index with value < nums[i]
            prev = [-1] * n
            stack = []
            for i, x in enumerate(nums):
                while stack and nums[stack[-1]] > x:
                    stack.pop()
                prev[i] = stack[-1] if stack else -1
                stack.append(i)

            nxt = [n] * n
            stack = []
            for i in range(n - 1, -1, -1):
                x = nums[i]
                while stack and nums[stack[-1]] >= x:
                    stack.pop()
                nxt[i] = stack[-1] if stack else n
                stack.append(i)

            total = 0
            for i, x in enumerate(nums):
                left_choices = i - prev[i]
                right_choices = nxt[i] - i
                total += x * count_valid(left_choices, right_choices, k)
            return total

        def sum_max() -> int:
            # Assign each subarray maximum to its leftmost occurrence.
            # For element i to be the chosen maximum:
            #   left boundary: previous index with value >= nums[i]
            #   right boundary: next index with value > nums[i]
            prev = [-1] * n
            stack = []
            for i, x in enumerate(nums):
                while stack and nums[stack[-1]] < x:
                    stack.pop()
                prev[i] = stack[-1] if stack else -1
                stack.append(i)

            nxt = [n] * n
            stack = []
            for i in range(n - 1, -1, -1):
                x = nums[i]
                while stack and nums[stack[-1]] <= x:
                    stack.pop()
                nxt[i] = stack[-1] if stack else n
                stack.append(i)

            total = 0
            for i, x in enumerate(nums):
                left_choices = i - prev[i]
                right_choices = nxt[i] - i
                total += x * count_valid(left_choices, right_choices, k)
            return total

        return sum_min() + sum_max()