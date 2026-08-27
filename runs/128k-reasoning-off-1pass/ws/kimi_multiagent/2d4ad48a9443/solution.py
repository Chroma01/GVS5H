from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        ans = 0
        left = 0
        cost = 0  # min operations to make nums[left..right] non-decreasing

        # Monotonic stack of [value, count] with strictly increasing values.
        # It represents the "running maximum" structure of the current window:
        # the window is partitioned into segments; every element in segment i
        # has running maximum value[i], and segment i contains count[i] elements.
        stack = []  # list of [value, count]

        for right in range(n):
            x = nums[right]

            # --- Extend window to the right ---
            # New element x contributes 0 if x >= current max, else (max - x).
            # Merging segments with value <= x: those elements' running max
            # becomes x, reducing the cost accordingly.
            if not stack or stack[-1][0] > x:
                # x is below current running max; deficit = max - x
                cost += stack[-1][0] - x
                stack.append([x, 1])
            else:
                # x becomes the running max for itself and all later segments
                # whose previous running max was <= x.
                cnt = 1
                while stack and stack[-1][0] <= x:
                    v, c = stack.pop()
                    cost -= (x - v) * c  # their deficit shrinks by (x - v) each
                    cnt += c
                stack.append([x, cnt])

            # --- Shrink window from the left while cost > k ---
            while cost > k:
                lv, lc = stack[0]
                if lc == 1:
                    # Removing the only element of the first segment.
                    # The next segment's elements had running max lv; now their
                    # running max becomes their own segment value, so each of
                    # them gains deficit (lv - next_value).
                    stack.pop(0)
                    if stack:
                        cost += (lv - stack[0][0]) * stack[0][1]
                else:
                    # Removing one element from the first segment; the removed
                    # element itself contributed 0 (it was at its running max),
                    # so cost is unchanged.
                    stack[0][1] -= 1
                left += 1

            # All subarrays ending at `right` with left endpoint in [left..right]
            ans += right - left + 1

        return ans