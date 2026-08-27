from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def capped_count(A: int, B: int) -> int:
            # Count pairs (x, y) with 0 <= x <= A-1, 0 <= y <= B-1, x + y + 1 <= k
            # = sum_{x=0}^{A-1} clamp(k - x, 0, B)
            if A <= 0 or B <= 0 or k <= 0:
                return 0
            # x range where k - x >= B  => x <= k - B
            full_end = min(A - 1, k - B)          # inclusive
            total = 0
            x = 0
            if full_end >= 0:
                total += (full_end + 1) * B
                x = full_end + 1
            # x range where 0 < k - x < B => k - B < x < k
            lo = x
            hi = min(A - 1, k - 1)                # inclusive
            if lo <= hi:
                m = hi - lo + 1
                # sum_{x=lo}^{hi} (k - x) = m*k - (lo+hi)*m//2
                total += m * k - (lo + hi) * m // 2
            return total

        # ---- Maximum contributions ----
        # prev index with value >= nums[i]; next index with value > nums[i]
        # (equal values attributed to the rightmost occurrence)
        prev_ge = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            prev_ge[i] = stack[-1] if stack else -1
            stack.append(i)

        next_gt = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            next_gt[i] = stack[-1] if stack else n
            stack.append(i)

        # ---- Minimum contributions ----
        # prev index with value <= nums[i]; next index with value < nums[i]
        prev_le = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            prev_le[i] = stack[-1] if stack else -1
            stack.append(i)

        next_lt = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            next_lt[i] = stack[-1] if stack else n
            stack.append(i)

        ans = 0
        for i in range(n):
            a_max = i - prev_ge[i]
            b_max = next_gt[i] - i
            a_min = i - prev_le[i]
            b_min = next_lt[i] - i
            ans += nums[i] * (capped_count(a_max, b_max) + capped_count(a_min, b_min))
        return ans