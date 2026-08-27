from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dq = deque()  # each item: [value, count]; values strictly increasing front -> back
        cost = 0      # min operations to make current window nums[l..r] non-decreasing
        ans = 0
        r = n - 1

        for l in range(n - 1, -1, -1):
            x = nums[l]

            # Prepend x at the front of the window.
            # All front blocks with value <= x get their running max raised to x.
            total = 1  # the new element itself
            while dq and dq[0][0] <= x:
                v, c = dq.popleft()
                cost += (x - v) * c
                total += c
            dq.appendleft([x, total])

            # Shrink from the right while the window is too expensive.
            # Removing position r only removes its own deficit (back_value - nums[r]);
            # all other positions' running maxima are unaffected.
            while cost > k and r >= l:
                v, c = dq[-1]
                cost -= v - nums[r]
                if c == 1:
                    dq.pop()
                else:
                    dq[-1][1] = c - 1
                r -= 1

            # All subarrays nums[l..r'], l <= r' <= r, are valid.
            ans += r - l + 1

        return ans