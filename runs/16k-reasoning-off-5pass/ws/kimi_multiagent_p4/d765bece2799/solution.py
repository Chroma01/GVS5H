from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def count_pairs(L: int, R: int) -> int:
            # Number of pairs (a, b) with 1 <= a <= L, 1 <= b <= R, a + b <= k + 1
            L = min(L, k)
            R = min(R, k)
            if L <= 0 or R <= 0:
                return 0
            # For a in [1..L]: b_max = min(R, k + 1 - a)
            # k + 1 - a >= R  <=>  a <= k + 1 - R
            t = k + 1 - R  # threshold
            total = 0
            if t >= 1:
                full = min(L, t)          # a in [1..full]: term = R
                total += full * R
                start = full + 1
            else:
                start = 1
            # a in [start..L]: term = k + 1 - a (positive since a <= L <= k)
            if start <= L:
                cnt = L - start + 1
                # sum_{a=start}^{L} (k + 1 - a) = cnt*(k+1) - (start+L)*cnt//2
                total += cnt * (k + 1) - (start + L) * cnt // 2
            return total

        # ---- Minimum contributions: PSE (strict <) and NSE (<=) ----
        left_min = [0] * n   # distance to previous strictly smaller element
        right_min = [0] * n  # distance to next smaller-or-equal element
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            left_min[i] = i - stack[-1] if stack else i + 1
            stack.append(i)
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            right_min[i] = stack[-1] - i if stack else n - i
            stack.append(i)

        # ---- Maximum contributions: PGE (strict >) and NGE (>=) ----
        left_max = [0] * n   # distance to previous strictly greater element
        right_max = [0] * n  # distance to next greater-or-equal element
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            left_max[i] = i - stack[-1] if stack else i + 1
            stack.append(i)
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            right_max[i] = stack[-1] - i if stack else n - i
            stack.append(i)

        ans = 0
        for i in range(n):
            f_min = count_pairs(left_min[i], right_min[i])
            f_max = count_pairs(left_max[i], right_max[i])
            ans += nums[i] * (f_min + f_max)
        return ans