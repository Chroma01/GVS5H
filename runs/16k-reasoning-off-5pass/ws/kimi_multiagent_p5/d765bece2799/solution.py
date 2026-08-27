from typing import List


class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)

        def count_pairs(a: int, b: int) -> int:
            # Number of (l, r) with l in [i-a+1, i], r in [i, i+b-1],
            # and r - l + 1 <= k.  Here a, b >= 1.
            if a + b - 1 <= k:
                return a * b
            if a > b:
                a, b = b, a
            # now a <= b and a + b - 1 > k
            if k < a:
                # only lengths 1..k matter; each length len has exactly
                # len placements (since len <= k < a <= b)
                return k * (k + 1) // 2
            if k < b:
                # a <= k < b: for l = i - j (j = 0..a-1), valid r count
                # is k - j (no b-plateau since k < b)
                return a * k - a * (a - 1) // 2
            # a <= b <= k < a + b - 1
            # j in [0, k-b] give b choices each; j in [k-b+1, a-1] give k-j
            return ((k - b + 1) * b
                    + b * (b - 1) // 2
                    - (k - a) * (k - a + 1) // 2)

        def contribution(is_min: bool) -> int:
            # left[i]: number of choices for l ending at i, bounded by the
            # nearest index to the left that strictly "wins"
            # (> nums[i] for min, < nums[i] for max)
            left = [0] * n
            stack = []
            for i in range(n):
                if is_min:
                    while stack and nums[stack[-1]] > nums[i]:
                        stack.pop()
                else:
                    while stack and nums[stack[-1]] < nums[i]:
                        stack.pop()
                left[i] = i - stack[-1] if stack else i + 1
                stack.append(i)

            # right[i]: number of choices for r starting at i, bounded by the
            # nearest index to the right that ties-or-wins
            # (>= for min, <= for max) -- consistent tie-breaking
            right = [0] * n
            stack = []
            for i in range(n - 1, -1, -1):
                if is_min:
                    while stack and nums[stack[-1]] >= nums[i]:
                        stack.pop()
                else:
                    while stack and nums[stack[-1]] <= nums[i]:
                        stack.pop()
                right[i] = stack[-1] - i if stack else n - i
                stack.append(i)

            total = 0
            for i in range(n):
                total += nums[i] * count_pairs(left[i], right[i])
            return total

        return contribution(True) + contribution(False)