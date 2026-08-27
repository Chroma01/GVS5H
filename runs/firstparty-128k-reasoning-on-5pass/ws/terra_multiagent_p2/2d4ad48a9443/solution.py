from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # (enforced prefix-maximum target, number of consecutive positions)
        # Targets increase strictly from left to right.
        blocks = deque()

        cost = 0
        right = n
        answer = 0

        for left in range(n - 1, -1, -1):
            x = nums[left]

            # Insert x at the left. Every leading block with target <= x
            # must be raised to x; x itself requires no increment.
            merged_count = 1
            old_target_sum = 0

            while blocks and blocks[0][0] <= x:
                value, count = blocks.popleft()
                merged_count += count
                old_target_sum += value * count

            cost += x * (merged_count - 1) - old_target_sum
            blocks.appendleft((x, merged_count))

            # Remove rightmost elements until the window is affordable.
            while cost > k:
                right -= 1
                value, count = blocks[-1]

                cost -= value - nums[right]

                if count == 1:
                    blocks.pop()
                else:
                    blocks[-1] = (value, count - 1)

            answer += right - left

        return answer