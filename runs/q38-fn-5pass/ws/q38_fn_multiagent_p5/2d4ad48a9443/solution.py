from typing import List
from array import array


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        pref = [0] * (n + 1)
        for i, x in enumerate(nums):
            pref[i + 1] = pref[i] + x

        levels_count = n.bit_length() + 1
        up = [array('l', [n]) * n for _ in range(levels_count)]
        jump_cost = [array('q', [0]) * n for _ in range(levels_count)]

        stack = []
        up0 = up[0]
        cost0 = jump_cost[0]

        # nxt[i] = first index j > i with nums[j] > nums[i], or n.
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] <= x:
                stack.pop()

            j = stack[-1] if stack else n
            up0[i] = j
            cost0[i] = x * (j - i) - (pref[j] - pref[i])
            stack.append(i)

        del stack

        # Binary lifting over next-greater jumps.
        for p in range(1, levels_count):
            prev_up = up[p - 1]
            prev_cost = jump_cost[p - 1]
            cur_up = up[p]
            cur_cost = jump_cost[p]

            for i in range(n):
                mid = prev_up[i]
                if mid < n:
                    cur_up[i] = prev_up[mid]
                    cur_cost[i] = prev_cost[i] + prev_cost[mid]
                else:
                    cur_up[i] = n
                    cur_cost[i] = prev_cost[i]

        level_data = [(up[p], jump_cost[p]) for p in range(levels_count - 1, -1, -1)]

        def window_cost(l: int, r: int, limit: int,
                        level_data=level_data, nums=nums, pref=pref) -> int:
            total = 0
            i = l

            for up_p, cost_p in level_data:
                j = up_p[i]
                if j <= r:
                    total += cost_p[i]
                    if total > limit:
                        return total
                    i = j

            total += nums[i] * (r - i + 1) - (pref[r + 1] - pref[i])
            return total

        wc = window_cost
        ans = 0
        r = -1

        for l in range(n):
            if r < l:
                r = l - 1

            while r + 1 < n and wc(l, r + 1, k) <= k:
                r += 1

            ans += r - l + 1

        return ans