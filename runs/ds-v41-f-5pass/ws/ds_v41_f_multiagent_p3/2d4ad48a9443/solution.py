from typing import List
from collections import deque

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        c = nums[::-1]
        # Blocks are stored from rightmost position to leftmost position.
        # Values in the deque are increasing from front to back.
        dq = deque()  # entries are [suffix_max_value, count]
        suffix_sum = 0
        window_sum = 0
        left = 0
        ans = 0

        for right, x in enumerate(c):
            cnt = 1
            while dq and dq[0][0] <= x:
                v, block_cnt = dq.popleft()
                suffix_sum -= v * block_cnt
                cnt += block_cnt

            dq.appendleft([x, cnt])
            suffix_sum += x * cnt
            window_sum += x

            while suffix_sum - window_sum > k:
                v, block_cnt = dq[-1]
                suffix_sum -= v
                block_cnt -= 1
                if block_cnt == 0:
                    dq.pop()
                else:
                    dq[-1][1] = block_cnt
                window_sum -= c[left]
                left += 1

            ans += right - left + 1

        return ans