from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        limit = k + 1

        def triangular(t: int) -> int:
            return t * (t - 1) // 2 if t >= 2 else 0

        def count_pairs(left: int, right: int) -> int:
            # Count positive a, b with a <= left, b <= right, a + b <= k + 1.
            return (
                triangular(limit)
                - triangular(limit - left)
                - triangular(limit - right)
                + triangular(limit - left - right)
            )

        def contribution(find_max: bool) -> int:
            left = [0] * n
            right = [0] * n
            stack = []

            # Find distance to the previous strictly greater/smaller element.
            for i, value in enumerate(nums):
                while stack:
                    top_value = nums[stack[-1]]
                    should_pop = (
                        top_value <= value if find_max else top_value >= value
                    )
                    if not should_pop:
                        break
                    stack.pop()

                left[i] = i - stack[-1] if stack else i + 1
                stack.append(i)

            # Find distance to the next greater-or-equal/smaller-or-equal element.
            stack.clear()
            for i, value in enumerate(nums):
                while stack:
                    j = stack[-1]
                    top_value = nums[j]
                    should_pop = (
                        top_value <= value if find_max else top_value >= value
                    )
                    if not should_pop:
                        break
                    stack.pop()
                    right[j] = i - j
                stack.append(i)

            while stack:
                j = stack.pop()
                right[j] = n - j

            total = 0
            for i, value in enumerate(nums):
                total += value * count_pairs(left[i], right[i])
            return total

        return contribution(True) + contribution(False)