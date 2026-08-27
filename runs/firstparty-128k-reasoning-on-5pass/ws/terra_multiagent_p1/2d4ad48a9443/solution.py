from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Each block stores:
        # [prefix maximum target, number of elements, sum of original values].
        # Block targets are strictly increasing from left to right.
        blocks = deque()

        cost = 0
        right = n - 1
        answer = 0

        # Process possible left endpoints from right to left.
        for left in range(n - 1, -1, -1):
            x = nums[left]
            merged_count = 1
            merged_sum = x

            # Prepending x raises every consecutive leading block whose
            # prefix-maximum target is at most x.
            while blocks and blocks[0][0] <= x:
                target, count, value_sum = blocks.popleft()
                cost -= target * count - value_sum
                merged_count += count
                merged_sum += value_sum

            blocks.appendleft([x, merged_count, merged_sum])
            cost += x * merged_count - merged_sum

            # Remove elements from the right until the current window fits.
            while cost > k:
                target, count, value_sum = blocks[-1]
                removed_value = nums[right]

                cost -= target - removed_value
                count -= 1
                value_sum -= removed_value
                right -= 1

                if count == 0:
                    blocks.pop()
                else:
                    blocks[-1][1] = count
                    blocks[-1][2] = value_sum

            answer += right - left + 1

        return answer