from typing import List
from collections import deque


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def sum_extrema(want_max: bool) -> int:
            # Groups are ordered by subarray start from oldest to newest.
            # Each group is (extremum value, number of starts having that value).
            groups = deque()
            current_sum = 0
            result = 0

            for i, x in enumerate(nums):
                merged_count = 1

                if want_max:
                    while groups and groups[-1][0] <= x:
                        value, count = groups.pop()
                        current_sum -= value * count
                        merged_count += count
                else:
                    while groups and groups[-1][0] >= x:
                        value, count = groups.pop()
                        current_sum -= value * count
                        merged_count += count

                groups.append((x, merged_count))
                current_sum += x * merged_count

                # The newly added start makes the window too large.
                # Remove the oldest start from the oldest group.
                if i >= k:
                    value, count = groups.popleft()
                    current_sum -= value
                    if count > 1:
                        groups.appendleft((value, count - 1))

                result += current_sum

            return result

        return sum_extrema(True) + sum_extrema(False)