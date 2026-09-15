from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        S = k + 1  # length cap becomes: a + b <= S (since length = a + b - 1)

        def count_pairs(L: int, R: int) -> int:
            # Count (a, b) with 1 <= a <= L, 1 <= b <= R, a + b <= S.
            m = L if L < S - 1 else S - 1
            if m <= 0:
                return 0
            # For a <= S - R, the bound b <= R is binding (b can reach R).
            q = S - R
            if q > m:
                q = m
            if q < 0:
                q = 0
            res = q * R
            if q < m:
                # For a = q+1 .. m, b_max = S - a.
                lo = q + 1
                cnt = m - q
                res += cnt * S - (lo + m) * cnt // 2
            return res

        # prev_le[i] = nearest j < i with nums[j] <= nums[i]
        prev_le = [-1] * n
        stack = []
        for i in range(n):
            x = nums[i]
            while stack and nums[stack[-1]] > x:
                stack.pop()
            prev_le[i] = stack[-1] if stack else -1
            stack.append(i)

        # next_lt[i] = nearest j > i with nums[j] < nums[i]
        next_lt = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] >= x:
                stack.pop()
            next_lt[i] = stack[-1] if stack else n
            stack.append(i)

        # prev_ge[i] = nearest j < i with nums[j] >= nums[i]
        prev_ge = [-1] * n
        stack = []
        for i in range(n):
            x = nums[i]
            while stack and nums[stack[-1]] < x:
                stack.pop()
            prev_ge[i] = stack[-1] if stack else -1
            stack.append(i)

        # next_gt[i] = nearest j > i with nums[j] > nums[i]
        next_gt = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            x = nums[i]
            while stack and nums[stack[-1]] <= x:
                stack.pop()
            next_gt[i] = stack[-1] if stack else n
            stack.append(i)

        total = 0
        for i in range(n):
            x = nums[i]
            Lmin = i - prev_le[i]
            Rmin = next_lt[i] - i
            Lmax = i - prev_ge[i]
            Rmax = next_gt[i] - i
            total += x * (count_pairs(Lmin, Rmin) + count_pairs(Lmax, Rmax))
        return total