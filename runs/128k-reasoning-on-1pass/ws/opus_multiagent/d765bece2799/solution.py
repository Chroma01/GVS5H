from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def f(t: int) -> int:
            # number of (x,y) with x,y >= 0 and x+y <= t
            if t < 0:
                return 0
            return (t + 1) * (t + 2) // 2

        def sum_of_maxes(arr: List[int], k: int) -> int:
            n = len(arr)
            m = k - 1
            L = [-1] * n   # nearest index to the left with strictly greater value
            R = [n] * n    # nearest index to the right with value >= arr[i]
            stack = []
            for i in range(n):
                v = arr[i]
                while stack and arr[stack[-1]] <= v:
                    j = stack.pop()
                    R[j] = i
                L[i] = stack[-1] if stack else -1
                stack.append(i)
            # remaining entries keep R = n
            total = 0
            for i in range(n):
                a = i - L[i]
                b = R[i] - i
                cnt = f(m) - f(m - a) - f(m - b) + f(m - a - b)
                if cnt:
                    total += arr[i] * cnt
            return total

        return sum_of_maxes(nums, k) - sum_of_maxes([-x for x in nums], k)