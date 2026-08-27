from typing import List
from collections import deque


class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        b = nums[::-1]
        n = len(b)
        stack = deque()  # groups [value, count], values non-increasing from bottom to top
        cost = 0
        l = 0
        ans = 0
        for r in range(n):
            x = b[r]
            cnt = 0
            while stack and stack[-1][0] < x:
                v, c = stack.pop()
                cost += (x - v) * c
                cnt += c
            stack.append([x, cnt + 1])

            while cost > k:
                bv = stack[0][0]
                cost -= bv - b[l]
                stack[0][1] -= 1
                if stack[0][1] == 0:
                    stack.popleft()
                l += 1

            ans += r - l + 1
        return ans


if __name__ == "__main__":
    s = Solution()
    assert s.countNonDecreasingSubarrays([6, 3, 1, 2, 4, 4], 7) == 17
    assert s.countNonDecreasingSubarrays([6, 3, 1, 3, 6], 4) == 12

    # brute force verification
    import random

    def brute(nums, k):
        n = len(nums)
        total = 0
        for i in range(n):
            mx = -1
            c = 0
            for j in range(i, n):
                if nums[j] > mx:
                    mx = nums[j]
                c += mx - nums[j]
                if c <= k:
                    total += 1
        return total

    random.seed(1)
    for _ in range(300):
        n = random.randint(1, 9)
        arr = [random.randint(1, 8) for _ in range(n)]
        kk = random.randint(1, 12)
        assert s.countNonDecreasingSubarrays(arr, kk) == brute(arr, kk), (arr, kk)
    print("ok")