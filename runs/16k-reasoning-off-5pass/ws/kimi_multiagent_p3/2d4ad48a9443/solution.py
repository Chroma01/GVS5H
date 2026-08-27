from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        cost = 0
        r = n - 1
        # deque of [level, count], levels strictly increasing from left (bottom) to right (top)
        dq = deque()

        for l in range(n - 1, -1, -1):
            # push-left nums[l]: prepend to current window [l+1, r]
            x = nums[l]
            cnt = 1
            while dq and dq[0][0] <= x:
                v, c = dq.popleft()
                cost += (x - v) * c
                cnt += c
            dq.appendleft([x, cnt])

            # shrink from the right while window [l, r] is invalid
            while cost > k:
                v, c = dq[-1]
                cost -= v - nums[r]
                if c == 1:
                    dq.pop()
                else:
                    dq[-1][1] = c - 1
                r -= 1

            ans += r - l + 1

        return ans