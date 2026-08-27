from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        prefix = [0] * (n + 1)
        for i, value in enumerate(nums):
            prefix[i + 1] = prefix[i] + value

        # ng[i] = first index j > i with nums[j] > nums[i].
        # n is a sentinel representing "no greater element".
        ng = [n] * n
        stack = []

        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            if stack:
                ng[i] = stack[-1]
            stack.append(i)

        # Include the sentinel in every jump table so it is never indexed out
        # of bounds while following a next-greater chain.
        size = n + 1
        levels = n.bit_length()

        jumps = [array("i", ng + [n])]
        base = array("q", [0] * size)

        for i in range(n):
            j = ng[i]
            if j < n:
                base[i] = nums[i] * (j - i) - (prefix[j] - prefix[i])

        costs = [base]

        for _ in range(1, levels):
            previous_jump = jumps[-1]
            previous_cost = costs[-1]

            current_jump = array("i", [0] * size)
            current_cost = array("q", [0] * size)

            for i in range(size):
                middle = previous_jump[i]
                current_jump[i] = previous_jump[middle]
                current_cost[i] = previous_cost[i] + previous_cost[middle]

            jumps.append(current_jump)
            costs.append(current_cost)

        def required(left: int, right: int) -> int:
            # The optimal final value at each position is the prefix maximum.
            # Follow next-greater links and sum complete constant-prefix-max
            # blocks, then handle the final truncated block.
            position = left
            total = 0

            for level in range(levels - 1, -1, -1):
                nxt = jumps[level][position]
                if nxt <= right:
                    total += costs[level][position]
                    position = nxt

            total += (
                nums[position] * (right - position + 1)
                - (prefix[right + 1] - prefix[position])
            )
            return total

        answer = 0

        for right in range(n):
            lo, hi = 0, right

            while lo < hi:
                mid = (lo + hi) // 2
                if required(mid, right) <= k:
                    hi = mid
                else:
                    lo = mid + 1

            answer += right - lo + 1

        return answer