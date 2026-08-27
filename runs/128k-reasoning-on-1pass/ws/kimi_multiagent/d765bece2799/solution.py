from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def countPairs(L: int, R: int, k: int) -> int:
            # Number of (a, b) with 1 <= a <= L, 1 <= b <= R, a + b <= k + 1
            # (subarray length = a + b - 1 <= k)
            if L > R:
                L, R = R, L
            s = k + 1
            if s >= L + R:          # every extension pair is valid
                return L * R
            if s <= L + 1:          # neither bound binds: full triangle
                return s * (s - 1) // 2
            if s <= R + 1:          # only the L-bound binds: trapezoid
                return L * s - L * (L + 1) // 2
            # both bounds bind: rectangle minus mirrored triangle
            s2 = L + R + 1 - s
            return L * R - s2 * (s2 - 1) // 2

        def sumMax(arr: List[int]) -> int:
            n = len(arr)
            # prev_g[i] = nearest index j < i with arr[j] > arr[i] (strictly greater)
            prev_g = [-1] * n
            stack: List[int] = []
            for i, v in enumerate(arr):
                while stack and arr[stack[-1]] <= v:
                    stack.pop()
                prev_g[i] = stack[-1] if stack else -1
                stack.append(i)

            total = 0
            stack.clear()
            # next greater-or-equal: nearest index j > i with arr[j] >= arr[i]
            for i in range(n - 1, -1, -1):
                v = arr[i]
                while stack and arr[stack[-1]] < v:
                    stack.pop()
                r = stack[-1] if stack else n
                L = i - prev_g[i]   # valid left extensions
                R = r - i           # valid right extensions
                total += v * countPairs(L, R, k)
                stack.append(i)
            return total

        # sum of minimums = -sumMax(-nums)
        return sumMax(nums) - sumMax([-x for x in nums])