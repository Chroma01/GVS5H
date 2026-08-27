from collections import deque
from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dq = deque()  # groups [value, count], strictly decreasing values front -> back
        cost = 0      # min increments to make current window (in original order) non-decreasing
        left = 0      # left pointer in reversed coordinates (b[p] = nums[n-1-p])
        ans = 0

        for j in range(n - 1, -1, -1):
            x = nums[j]
            right = n - 1 - j  # right pointer in reversed coordinates

            # Append x on the right of the reversed window:
            # previous groups with suffix-max value <= x get raised to x.
            cnt = 1
            while dq and dq[-1][0] <= x:
                v, c = dq.pop()
                cost += (x - v) * c
                cnt += c
            dq.append([x, cnt])

            # Shrink from the left while the window is too expensive.
            while cost > k:
                v, c = dq[0]
                y = nums[n - 1 - left]  # actual value of the leftmost element
                cost -= (v - y)         # its contribution was (group value - y)
                if c == 1:
                    dq.popleft()
                else:
                    dq[0][1] = c - 1
                left += 1

            # All subarrays b[left..right], b[left+1..right], ..., b[right..right] are valid.
            ans += right - left + 1

        return ans