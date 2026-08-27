from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Prefix sums of nums.
        pref = [0] * (n + 1)
        for i, value in enumerate(nums):
            pref[i + 1] = pref[i] + value

        # ng[i] is the first index j > i such that nums[j] > nums[i].
        ng = [n] * n
        stack = []

        for i, value in enumerate(nums):
            while stack and nums[stack[-1]] < value:
                ng[stack.pop()] = i
            stack.append(i)

        # Each index starts a block whose target value is nums[i] and whose
        # endpoint is ng[i] - 1. Binary lifting combines consecutive blocks.
        log = n.bit_length()

        up = [array("i", ng + [n])]
        block_sum = [
            array(
                "q",
                [nums[i] * (ng[i] - i) for i in range(n)] + [0],
            )
        ]

        for _ in range(1, log):
            prev_up = up[-1]
            prev_sum = block_sum[-1]

            cur_up = array("i", [0]) * (n + 1)
            cur_sum = array("q", [0]) * (n + 1)

            for i in range(n):
                middle = prev_up[i]
                cur_up[i] = prev_up[middle]
                cur_sum[i] = prev_sum[i] + prev_sum[middle]

            cur_up[n] = n
            up.append(cur_up)
            block_sum.append(cur_sum)

        def required_cost(left: int, right: int) -> int:
            """Minimum increments needed for nums[left:right + 1]."""
            pos = left
            target_sum = 0

            for level in range(log - 1, -1, -1):
                nxt = up[level][pos]
                if nxt <= right:
                    target_sum += block_sum[level][pos]
                    pos = nxt

            target_sum += nums[pos] * (right - pos + 1)
            original_sum = pref[right + 1] - pref[left]
            return target_sum - original_sum

        answer = 0
        left = 0

        for right in range(n):
            while left <= right and required_cost(left, right) > k:
                left += 1

            answer += right - left + 1

        return answer