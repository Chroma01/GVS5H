from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        return self._sumExtremum(nums, k, True) + self._sumExtremum(nums, k, False)

    def _sumExtremum(self, nums: List[int], k: int, isMin: bool) -> int:
        n = len(nums)
        left = [0] * n   # nearest index to the left that "wins" (blocks i)
        right = [0] * n  # nearest index to the right that "wins" (blocks i)
        stack = []

        # Previous blocking element: strict for min (>), strict for max (<)
        for i in range(n):
            while stack and (nums[stack[-1]] > nums[i] if isMin else nums[stack[-1]] < nums[i]):
                stack.pop()
            left[i] = stack[-1] if stack else -1
            stack.append(i)

        stack.clear()
        # Next blocking element: non-strict (>= / <=) so ties are counted once
        for i in range(n - 1, -1, -1):
            while stack and (nums[stack[-1]] >= nums[i] if isMin else nums[stack[-1]] <= nums[i]):
                stack.pop()
            right[i] = stack[-1] if stack else n
            stack.append(i)

        total = 0
        for i in range(n):
            L = left[i] + 1          # smallest allowed start
            R = right[i] - 1         # largest allowed end
            s_lo = max(L, i - k + 1) # starts must keep length <= k
            if s_lo > i:
                continue
            # split starts: for s <= s_split, cap k binds (end = s+k-1);
            # for s > s_split, right boundary binds (end = R)
            s_split = min(i, R - k + 1)
            cnt = 0
            if s_lo <= s_split:
                m = s_split - s_lo + 1
                # sum_{s=s_lo}^{s_split} (s + k - i)
                cnt += m * (s_lo + s_split) // 2 + m * (k - i)
            if s_split < i:
                m = i - max(s_lo, s_split + 1) + 1
                if m > 0:
                    cnt += m * (R - i + 1)
            total += nums[i] * cnt
        return total