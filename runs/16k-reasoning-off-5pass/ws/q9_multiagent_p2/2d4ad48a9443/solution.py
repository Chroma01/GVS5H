from typing import List
from collections import deque

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Stack stores tuples: (height, count, sum_original, left_index)
        # height: the value that all elements in the segment are raised to
        # count: number of elements in the segment
        # sum_original: sum of original nums values in this segment
        # left_index: the starting index of this segment in nums
        stack = deque()
        current_cost = 0
        left = 0
        result = 0
        
        for right in range(n):
            val = nums[right]
            
            # Add nums[right] to the stack (right end)
            # We maintain the stack such that heights are non-decreasing from left to right.
            # If the current value is less than the top height, we merge into the top segment.
            # If it's greater or equal, we push a new segment.
            if stack and stack[-1][0] > val:
                # Merge with the top (rightmost) segment
                h, count, s, L = stack.pop()
                # The cost to raise 'count' elements from their original sum 's' to 'h' is:
                # cost = count * h - s.
                # When we add a new element 'val' to this segment (raising it to 'h'),
                # the new cost contribution becomes (count + 1) * h - (s + val).
                # The change in cost is: ((count + 1) * h - (s + val)) - (count * h - s) = h - val.
                current_cost += (h - val)
                stack.append((h, count + 1, s + val, L))
            else:
                # Push new segment
                stack.append((val, 1, val, right))
            
            # Shrink from the left until cost <= k
            while current_cost > k:
                # The leftmost segment is at stack[0]
                h, count, s, L = stack[0]
                
                # We are removing nums[L]
                # The cost contribution of this element in the current configuration is (h - nums[L])
                cost_removed = h - nums[L]
                current_cost -= cost_removed
                count -= 1
                
                if count == 0:
                    # Segment is completely removed
                    stack.popleft()
                else:
                    # Segment still has elements, update its properties
                    # The sum of original values decreases by nums[L]
                    # The left index increases by 1
                    # The height remains h
                    stack[0] = (h, count, s - nums[L], L + 1)
                
                left += 1
            
            # All subarrays ending at 'right' and starting from 'left' to 'right' are valid
            result += (right - left + 1)
            
        return result

# Verification against examples
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    nums1 = [6, 3, 1, 2, 4, 4]
    k1 = 7
    res1 = sol.countNonDecreasingSubarrays(nums1, k1)
    print(f"Example 1: Input: nums = {nums1}, k = {k1}")
    print(f"Output: {res1}, Expected: 17")
    
    # Example 2
    nums2 = [6, 3, 1, 3, 6]
    k2 = 4
    res2 = sol.countNonDecreasingSubarrays(nums2, k2)
    print(f"Example 2: Input: nums = {nums2}, k = {k2}")
    print(f"Output: {res2}, Expected: 12")