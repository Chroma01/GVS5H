from typing import List
from collections import deque

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        dq = deque()  # groups of (level, count), levels strictly increasing front->back
        window_sum = 0
        level_sum = 0  # sum of level * count over groups
        ans = 0
        r = 0  # window is [l, r)

        def push(x):
            nonlocal window_sum, level_sum
            cnt = 1
            while dq and dq[-1][0] <= x:
                lv, c = dq.pop()
                level_sum -= lv * c
                cnt += c
            dq.append((x, cnt))
            level_sum += x * cnt
            window_sum += x

        def pop_left(x):
            nonlocal window_sum, level_sum
            window_sum -= x
            lv, c = dq[0]
            if c == 1:
                dq.popleft()
            else:
                dq[0] = (lv, c - 1)
            level_sum -= lv

        for l in range(n):
            while r < n:
                x = nums[r]
                # simulate push cost
                add = x
                for lv, c in reversed(dq):
                    if lv <= x:
                        add += (x - lv) * c
                    else:
                        break
                if level_sum + add - (window_sum + x) > k:
                    break
                push(x)
                r += 1
            ans += r - l
            if r == l:
                r += 1
            else:
                pop_left(nums[l])
        return ans