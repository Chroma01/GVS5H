from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def pair_count(limit: int) -> int:
            """Number of positive pairs (a, b) with a + b <= limit."""
            return limit * (limit - 1) // 2 if limit > 1 else 0

        def contribution_for_max() -> int:
            prev = [-1] * n
            nxt = [n] * n

            stack = []
            for i, value in enumerate(nums):
                while stack and nums[stack[-1]] <= value:
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)

            stack = []
            for i in range(n - 1, -1, -1):
                while stack and nums[stack[-1]] < nums[i]:
                    stack.pop()
                if stack:
                    nxt[i] = stack[-1]
                stack.append(i)

            total = 0
            for i, value in enumerate(nums):
                left = i - prev[i]
                right = nxt[i] - i

                count = (
                    pair_count(k + 1)
                    - pair_count(k + 1 - left)
                    - pair_count(k + 1 - right)
                    + pair_count(k + 1 - left - right)
                )
                total += value * count

            return total

        def contribution_for_min() -> int:
            prev = [-1] * n
            nxt = [n] * n

            stack = []
            for i, value in enumerate(nums):
                while stack and nums[stack[-1]] >= value:
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)

            stack = []
            for i in range(n - 1, -1, -1):
                while stack and nums[stack[-1]] > nums[i]:
                    stack.pop()
                if stack:
                    nxt[i] = stack[-1]
                stack.append(i)

            total = 0
            for i, value in enumerate(nums):
                left = i - prev[i]
                right = nxt[i] - i

                count = (
                    pair_count(k + 1)
                    - pair_count(k + 1 - left)
                    - pair_count(k + 1 - right)
                    + pair_count(k + 1 - left - right)
                )
                total += value * count

            return total

        return contribution_for_max() + contribution_for_min()