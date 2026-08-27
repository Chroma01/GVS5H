from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # nxt[i] is the first index to the right whose value is
        # strictly greater than nums[i].
        nxt = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            if stack:
                nxt[i] = stack[-1]
            stack.append(i)

        # Binary lifting over the chain of successive greater elements.
        # For every jump, weight[p][i] is the contribution of all complete
        # prefix-maximum blocks traversed by that jump.
        levels = n.bit_length()

        up = [array("i", nxt + [n])]
        base_weight = [0] * (n + 1)
        for i in range(n):
            base_weight[i] = nums[i] * (nxt[i] - i)
        weight = [array("q", base_weight)]

        for _ in range(1, levels):
            prev_up = up[-1]
            prev_weight = weight[-1]

            cur_up = array("i", [0]) * (n + 1)
            cur_weight = array("q", [0]) * (n + 1)

            for i in range(n):
                mid = prev_up[i]
                cur_up[i] = prev_up[mid]
                cur_weight[i] = prev_weight[i] + prev_weight[mid]

            up.append(cur_up)
            weight.append(cur_weight)

        prefix = [0] * (n + 1)
        for i, value in enumerate(nums):
            prefix[i + 1] = prefix[i] + value

        def repair_cost(left: int, right: int) -> int:
            """Cost to make nums[left:right+1] non-decreasing."""
            node = left
            repaired_sum = 0

            for p in range(levels - 1, -1, -1):
                jump = up[p][node]
                if jump <= right:
                    repaired_sum += weight[p][node]
                    node = jump

            repaired_sum += nums[node] * (right - node + 1)
            original_sum = prefix[right + 1] - prefix[left]
            return repaired_sum - original_sum

        # The smallest valid left endpoint is monotone non-decreasing
        # as the right endpoint advances.
        left = 0
        answer = 0

        for right in range(n):
            while left <= right and repair_cost(left, right) > k:
                left += 1
            answer += right - left + 1

        return answer