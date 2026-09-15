from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        limit = k + 1

        def count_pairs(left: int, right: int) -> int:
            # Count positive x <= left and y <= right with x + y <= limit.
            if limit >= left + right:
                return left * right

            max_x = left if left < limit else limit - 1
            if max_x <= 0:
                return 0

            full = limit - right
            if full < 0:
                full = 0
            elif full > max_x:
                full = max_x

            ans = full * right
            if max_x > full:
                cnt = max_x - full
                ans += cnt * limit - (full + 1 + max_x) * cnt // 2
            return ans

        def sum_min(arr: List[int]) -> int:
            n = len(arr)
            left = [0] * n
            stack = []

            # left[i] = number of possible starts for which arr[i] can be
            # the rightmost minimum, ignoring the length cap.
            for i, x in enumerate(arr):
                while stack and arr[stack[-1]] >= x:
                    stack.pop()
                left[i] = (i - stack[-1]) if stack else (i + 1)
                stack.append(i)

            total = 0
            stack = []

            # Scan right-to-left to find the next smaller-or-equal element.
            for i in range(n - 1, -1, -1):
                x = arr[i]
                while stack and arr[stack[-1]] > x:
                    stack.pop()

                nxt = stack[-1] if stack else n
                right = nxt - i
                total += x * count_pairs(left[i], right)
                stack.append(i)

            return total

        # Sum of minima plus sum of maxima.
        # Maxima of nums are minima of -nums.
        return sum_min(nums) - sum_min([-x for x in nums])