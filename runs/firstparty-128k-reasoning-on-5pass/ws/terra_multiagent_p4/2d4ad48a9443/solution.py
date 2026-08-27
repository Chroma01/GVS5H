from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)

        # Entries are (target_height, element_count, sum_of_original_values).
        # Heights are strictly increasing from left to right.
        groups = deque()

        right = n - 1
        cost = 0
        answer = 0

        for left in range(n - 1, -1, -1):
            x = nums[left]

            # Prepend nums[left]. It raises itself and every initial plateau
            # with target <= x to target x.
            merged_count = 1
            merged_sum = x

            while groups and groups[0][0] <= x:
                height, count, value_sum = groups.popleft()
                cost -= height * count - value_sum
                merged_count += count
                merged_sum += value_sum

            cost += x * merged_count - merged_sum
            groups.appendleft((x, merged_count, merged_sum))

            # Remove suffix elements until the active window is affordable.
            while cost > k:
                height, count, value_sum = groups[-1]
                value = nums[right]

                cost -= height - value

                if count == 1:
                    groups.pop()
                else:
                    groups[-1] = (height, count - 1, value_sum - value)

                right -= 1

            # All [left..end], left <= end <= right, are also affordable.
            answer += right - left + 1

        return answer