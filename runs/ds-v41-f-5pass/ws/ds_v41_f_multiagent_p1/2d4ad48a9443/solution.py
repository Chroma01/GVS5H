from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        ans = 0
        # blocks: (value, count), values NON-decreasing from index 0 (left / smallest prefix-max)
        # to the end (right / largest prefix-max). Represent prefix-maximum plateaus of window [L,R].
        blocks = deque()
        cost = 0          # = sum over window of (prefix_max - nums[i])
        R = n - 1

        # Process L from right to left. For each L, f(L)=max valid R is non-increasing,
        # so R only moves left  ->  two pointers, O(n) total.
        for L in range(n - 1, -1, -1):
            x = nums[L]
            # add element on the LEFT: merge all leftmost blocks with value <= x into x
            cnt = 1
            while blocks and blocks[0][0] <= x:
                v, c = blocks.popleft()
                cost += (x - v) * c
                cnt += c
            blocks.appendleft((x, cnt))

            # shrink from the RIGHT while cost too large
            while cost > k:
                v, c = blocks.pop()
                cost -= v - nums[R]      # only position R loses its prefix-max contribution
                if c > 1:
                    blocks.append((v, c - 1))
                R -= 1

            ans += R - L + 1

        return ans