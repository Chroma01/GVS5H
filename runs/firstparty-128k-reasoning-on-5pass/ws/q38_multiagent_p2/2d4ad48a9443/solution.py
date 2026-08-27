from typing import List
import random


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0

        pref = [0] * (n + 1)
        for i, x in enumerate(nums):
            pref[i + 1] = pref[i] + x

        # nxt[i] = first index j > i with nums[j] > nums[i], or n.
        nxt = [n] * (n + 1)
        stack = []
        for i in range(n - 1, -1, -1):
            xi = nums[i]
            while stack and nums[stack[-1]] <= xi:
                stack.pop()
            if stack:
                nxt[i] = stack[-1]
            stack.append(i)
        del stack

        # path[i] = sum of running maxima from i to n-1 when starting at i.
        path = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            path[i] = nums[i] * (nxt[i] - i) + path[nxt[i]]

        # Binary lifting over the next-greater chain.
        B = n.bit_length()
        up = [nxt]
        for _ in range(1, B):
            prev = up[-1]
            up.append([prev[prev[i]] for i in range(n + 1)])

        up_levels = tuple(up[b] for b in range(B - 1, -1, -1))

        def bad(l, r, up_levels=up_levels, path=path, nums=nums, pref=pref, k=k):
            p = l
            for upb in up_levels:
                np = upb[p]
                if np <= r:
                    p = np
            running_max_sum = path[l] - path[p] + nums[p] * (r - p + 1)
            return running_max_sum > pref[r + 1] - pref[l] + k

        ans = 0
        left = 0
        for right in range(n):
            while left <= right and bad(left, right):
                left += 1
            ans += right - left + 1
        return ans


if __name__ == "__main__":
    sol = Solution()

    # Provided examples.
    assert sol.countNonDecreasingSubarrays([6, 3, 1, 2, 4, 4], 7) == 17
    assert sol.countNonDecreasingSubarrays([6, 3, 1, 3, 6], 4) == 12

    # Edge cases.
    assert sol.countNonDecreasingSubarrays([5], 1) == 1
    assert sol.countNonDecreasingSubarrays([5], 0) == 1
    assert sol.countNonDecreasingSubarrays([2, 2, 2], 0) == 6
    assert sol.countNonDecreasingSubarrays([1, 2, 3, 4], 0) == 10
    assert sol.countNonDecreasingSubarrays([4, 3, 2, 1], 0) == 4
    assert sol.countNonDecreasingSubarrays([4, 3, 2, 1], 1) == 7
    assert sol.countNonDecreasingSubarrays([2, 1], 1) == 3
    assert sol.countNonDecreasingSubarrays([3, 1], 2) == 3

    def brute(nums, k):
        n = len(nums)
        ans = 0
        for l in range(n):
            run = nums[l]
            smax = 0
            s = 0
            for r in range(l, n):
                x = nums[r]
                if x > run:
                    run = x
                smax += run
                s += x
                if smax - s <= k:
                    ans += 1
        return ans

    # Randomized brute-force validation.
    random.seed(123456)
    for _ in range(2000):
        n = random.randint(1, 8)
        nums = [random.randint(1, 20) for _ in range(n)]
        k = random.randint(0, 100)
        expected = brute(nums, k)
        got = sol.countNonDecreasingSubarrays(nums, k)
        if got != expected:
            raise AssertionError((nums, k, expected, got))