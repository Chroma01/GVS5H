from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Monotonic stack: each entry is (max_val, count, orig_sum)
        # For the current window [left, right], the total deficit is:
        # sum_{i in window} (max_sofar - nums[i]) = sum(stack[j].max_val * stack[j].count) - sum(stack[j].orig_sum)
        stack = []  # list of [max_val, count, orig_sum]
        total_deficit = 0
        left = 0
        ans = 0
        
        for right in range(n):
            x = nums[right]
            cnt = 1
            orig = x
            # Merge with smaller or equal max values
            while stack and stack[-1][0] <= x:
                mv, cc, os = stack.pop()
                total_deficit -= mv * cc - os  # remove their contribution
                cnt += cc
                orig += os
            # Now push the new merged entry with max_val = x
            stack.append([x, cnt, orig])
            total_deficit += x * cnt - orig  # add contribution of new entry
            
            # Shrink window if deficit exceeds k
            while total_deficit > k:
                # Remove nums[left] from window
                # The leftmost element belongs to the first stack entry
                mv, cc, os = stack[0]
                # Reduce count and orig_sum by nums[left]
                stack[0][1] -= 1
                stack[0][2] -= nums[left]
                total_deficit -= mv - nums[left]  # deficit reduction for this element
                left += 1
                if stack[0][1] == 0:
                    stack.pop(0)
            
            # All subarrays ending at 'right' with start in [left, right] are valid
            ans += right - left + 1
        
        return ans