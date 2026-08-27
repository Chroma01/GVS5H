from collections import deque
from typing import List


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        groups = deque()  # [target value, count], ordered left to right
        cost = 0
        right = len(nums) - 1
        answer = 0

        for left in range(len(nums) - 1, -1, -1):
            x = nums[left]
            merged_count = 1

            # Raise all leading target groups below x to x.
            while groups and groups[0][0] < x:
                value, count = groups.popleft()
                cost += (x - value) * count
                merged_count += count

            if groups and groups[0][0] == x:
                groups[0][1] += merged_count
            else:
                groups.appendleft([x, merged_count])

            # Remove elements from the right while the window is too costly.
            while cost > k:
                value, count = groups[-1]
                cost -= value - nums[right]

                if count == 1:
                    groups.pop()
                else:
                    groups[-1][1] -= 1

                right -= 1

            answer += right - left + 1

        return answer