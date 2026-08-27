from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Each block is [running_prefix_maximum, number_of_positions].
        # Block heights strictly increase from front to back.
        blocks = deque()

        cost = 0
        answer = 0
        right = n - 1

        # Build each window by extending its left endpoint right-to-left.
        for left in range(n - 1, -1, -1):
            x = nums[left]
            length = 1

            # x becomes the prefix maximum for every initial block whose
            # existing maximum is at most x.
            while blocks and blocks[0][0] <= x:
                height, count = blocks.popleft()
                cost += (x - height) * count
                length += count

            blocks.appendleft([x, length])

            # Remove right endpoints until this subarray is affordable.
            while cost > k:
                height, count = blocks[-1]
                cost -= height - nums[right]
                right -= 1

                if count == 1:
                    blocks.pop()
                else:
                    blocks[-1][1] -= 1

            answer += right - left + 1

        return answer