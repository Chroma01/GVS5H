from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        limit = k + 1

        def bounded_pairs(left_count: int, right_count: int) -> int:
            """Count 1 <= left <= left_count, 1 <= right <= right_count,
            with left + right <= k + 1.
            """
            max_left = min(left_count, limit - 1)
            if max_left <= 0:
                return 0

            # For left distances up to full_end, every right distance works.
            full_end = min(max_left, max(0, limit - right_count))
            result = full_end * right_count

            # For the remaining left distances, valid right distances are
            # limit - left.
            remaining = max_left - full_end
            if remaining > 0:
                result += (
                    remaining * limit
                    - (full_end + 1 + max_left) * remaining // 2
                )

            return result

        def contribution_for_maximum() -> int:
            left = [0] * n
            right = [n] * n

            # Previous strictly greater element.
            stack = []
            for i, value in enumerate(nums):
                while stack and nums[stack[-1]] <= value:
                    stack.pop()
                left[i] = i - stack[-1] if stack else i + 1
                stack.append(i)

            # Next greater-or-equal element.
            stack = []
            for i in range(n - 1, -1, -1):
                value = nums[i]
                while stack and nums[stack[-1]] < value:
                    stack.pop()
                if stack:
                    right[i] = stack[-1]
                stack.append(i)

            total = 0
            for i, value in enumerate(nums):
                count = bounded_pairs(left[i], right[i] - i)
                total += value * count
            return total

        def contribution_for_minimum() -> int:
            left = [0] * n
            right = [n] * n

            # Previous strictly smaller element.
            stack = []
            for i, value in enumerate(nums):
                while stack and nums[stack[-1]] >= value:
                    stack.pop()
                left[i] = i - stack[-1] if stack else i + 1
                stack.append(i)

            # Next smaller-or-equal element.
            stack = []
            for i in range(n - 1, -1, -1):
                value = nums[i]
                while stack and nums[stack[-1]] > value:
                    stack.pop()
                if stack:
                    right[i] = stack[-1]
                stack.append(i)

            total = 0
            for i, value in enumerate(nums):
                count = bounded_pairs(left[i], right[i] - i)
                total += value * count
            return total

        return contribution_for_maximum() + contribution_for_minimum()