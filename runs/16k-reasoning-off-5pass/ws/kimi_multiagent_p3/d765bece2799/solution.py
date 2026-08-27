from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def count_pairs(L: int, R: int) -> int:
            # Number of (a, b) with 1 <= a <= L, 1 <= b <= R, a + b <= k + 1
            s = k + 1
            if L + R <= s:
                return L * R
            # a from 1..L, b_max = min(R, s - a), clamped at 0
            # Split: a <= s - R -> b_max = R ; s - R < a < s -> b_max = s - a ; a >= s -> 0
            total = 0
            # Region 1: a in [1, min(L, s - R)] contributes R each
            a1 = min(L, s - R)
            if a1 > 0:
                total += a1 * R
            # Region 2: a in [max(1, s - R + 1), min(L, s - 1)] contributes (s - a)
            lo = max(1, s - R + 1)
            hi = min(L, s - 1)
            if lo <= hi:
                m = hi - lo + 1
                total += m * s - (lo + hi) * m // 2
            return total

        def extremum_sum(arr: List[int], is_max: bool) -> int:
            # left[i]: distance to previous index that "blocks" attribution
            # For max: previous greater-or-equal on left, strictly greater on right
            # For min: previous less-or-equal on left, strictly less on right
            left = [0] * n
            right = [0] * n
            stack = []
            for i in range(n):
                if is_max:
                    while stack and arr[stack[-1]] < arr[i]:
                        stack.pop()
                else:
                    while stack and arr[stack[-1]] > arr[i]:
                        stack.pop()
                left[i] = i - stack[-1] if stack else i + 1
                stack.append(i)
            stack = []
            for i in range(n - 1, -1, -1):
                if is_max:
                    while stack and arr[stack[-1]] <= arr[i]:
                        stack.pop()
                else:
                    while stack and arr[stack[-1]] >= arr[i]:
                        stack.pop()
                right[i] = stack[-1] - i if stack else n - i
                stack.append(i)
            total = 0
            for i in range(n):
                total += arr[i] * count_pairs(left[i], right[i])
            return total

        return extremum_sum(nums, True) + extremum_sum(nums, False)