from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        blocks = deque()  # (target prefix-maximum value, count)
        cost = 0
        answer = 0
        right = n - 1

        # Grow each window by moving its left endpoint leftward.
        for left in range(n - 1, -1, -1):
            x = nums[left]
            count = 1

            # x becomes the prefix maximum for all initial target blocks
            # whose current target is no greater than x.
            while blocks and blocks[0][0] <= x:
                value, length = blocks.popleft()
                cost += (x - value) * length
                count += length

            blocks.appendleft((x, count))

            # Remove suffix elements until the window cost is affordable.
            while cost > k:
                value, length = blocks[-1]
                cost -= value - nums[right]

                if length == 1:
                    blocks.pop()
                else:
                    blocks[-1] = (value, length - 1)

                right -= 1

            # Every suffix [left, end], end <= right, is also affordable.
            answer += right - left + 1

        return answer