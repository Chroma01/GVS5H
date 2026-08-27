from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        return self._sum_extreme(nums, k, True) + self._sum_extreme(nums, k, False)

    def _sum_extreme(self, nums: List[int], k: int, is_max: bool) -> int:
        """
        Sum over all subarrays of length <= k of the subarray's maximum
        (is_max=True) or minimum (is_max=False).

        For each index i we find its "ownership" range: the maximal range of
        subarrays for which nums[i] is THE max (resp. min), using strict
        comparison on the previous side and non-strict on the next side so
        that ties are attributed to exactly one index. Then we count, in
        O(1), how many subarrays within that range have length <= k.
        """
        n = len(nums)

        def dominates(a: int, b: int, strict: bool) -> bool:
            """True if value a 'wins over' value b (a is the extreme)."""
            if is_max:
                return a > b if strict else a >= b
            else:
                return a < b if strict else a <= b

        # left[i] = distance from i to previous element that strictly
        # dominates nums[i] (i.e. number of steps we can extend left).
        left = [0] * n
        stack: List[int] = []
        for i in range(n):
            while stack and dominates(nums[i], nums[stack[-1]], strict=False):
                stack.pop()
            left[i] = i - stack[-1] if stack else i + 1
            stack.append(i)

        # right[i] = distance from i to next element that dominates-or-ties
        # nums[i] (number of steps we can extend right).
        right = [0] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and dominates(nums[i], nums[stack[-1]], strict=True):
                stack.pop()
            right[i] = stack[-1] - i if stack else n - i
            stack.append(i)

        total = 0
        for i in range(n):
            total += nums[i] * self._count_pairs(left[i], right[i], k)
        return total

    @staticmethod
    def _count_pairs(a: int, b: int, k: int) -> int:
        """
        Number of pairs (x, y) of integers with
            0 <= x <= a - 1,  0 <= y <= b - 1,  x + y <= k - 1.
        x = left extension, y = right extension; subarray length = x + y + 1.
        Closed form via arithmetic series.
        """
        if a <= 0 or b <= 0 or k <= 0:
            return 0
        m = k - 1  # max allowed x + y
        # For x in [0, a-1]: allowed y count = min(b, m - x + 1) if m - x >= 0.
        # Split x-range at x0 = m - b + 1:
        #   x <= x0  -> count = b
        #   x >  x0  -> count = m - x + 1 (positive while x <= m)
        lo = 0
        hi = a - 1
        if hi > m:
            hi = m  # beyond this, no y available
        if hi < lo:
            return 0
        x0 = m - b + 1
        # Region 1: x in [lo, min(hi, x0)] contributes b each
        r1_end = min(hi, x0)
        total = 0
        if r1_end >= lo:
            total += (r1_end - lo + 1) * b
        # Region 2: x in [max(lo, x0 + 1), hi] contributes (m - x + 1)
        r2_start = max(lo, x0 + 1)
        if r2_start <= hi:
            cnt = hi - r2_start + 1
            first = m - r2_start + 1
            last = m - hi + 1
            total += cnt * (first + last) // 2
        return total