from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # nxt[i] is the first index j > i such that nums[j] > nums[i].
        nxt = [-1] * n
        stack = []

        for i, value in enumerate(nums):
            while stack and nums[stack[-1]] < value:
                nxt[stack.pop()] = i
            stack.append(i)

        # Binary lifting over next-greater links.
        up = [nxt]

        base_sum = array("q", [0]) * n
        for i in range(n):
            j = nxt[i]
            end = n if j == -1 else j
            base_sum[i] = nums[i] * (end - i)

        block_sum = [base_sum]
        step = 1

        while step < n:
            prev_up = up[-1]
            prev_sum = block_sum[-1]

            current_up = [-1] * n
            current_sum = array("q", [0]) * n

            for i in range(n):
                middle = prev_up[i]
                if middle != -1:
                    current_up[i] = prev_up[middle]
                    current_sum[i] = prev_sum[i] + prev_sum[middle]

            up.append(current_up)
            block_sum.append(current_sum)
            step <<= 1

        prefix_sum = [0] * (n + 1)
        for i, value in enumerate(nums):
            prefix_sum[i + 1] = prefix_sum[i] + value

        def prefix_max_sum(left: int, right: int) -> int:
            """Return the sum of prefix maxima on nums[left:right + 1]."""
            current = left
            total = 0

            for level in range(len(up) - 1, -1, -1):
                destination = up[level][current]
                if destination != -1 and destination <= right:
                    total += block_sum[level][current]
                    current = destination

            total += nums[current] * (right - current + 1)
            return total

        def required_operations(left: int, right: int) -> int:
            return (
                prefix_max_sum(left, right)
                - (prefix_sum[right + 1] - prefix_sum[left])
            )

        answer = 0

        # For each right endpoint, feasible left endpoints form a suffix.
        for right in range(n):
            low, high = 0, right

            while low < high:
                middle = (low + high) // 2
                if required_operations(middle, right) <= k:
                    high = middle
                else:
                    low = middle + 1

            answer += right - low + 1

        return answer