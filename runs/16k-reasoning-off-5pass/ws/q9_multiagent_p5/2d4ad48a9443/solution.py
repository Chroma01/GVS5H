from typing import List

class Solution:
    def countNonDecreasingSubarrays(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Stack stores tuples: (value, count, start_index)
        # value: the adjusted value of the segment (all elements in this segment are raised to this value)
        # count: number of elements in the segment
        # start_index: the original index of the first element in this segment
        stack = []
        total_cost = 0
        left = 0
        valid_count = 0
        
        for right in range(n):
            current_val = nums[right]
            
            # Expansion: Maintain non-decreasing property in the stack
            # If the current element is smaller than the top of the stack,
            # it must be incremented to match the top's value.
            # We merge the current element into the top segment.
            if stack and stack[-1][0] > current_val:
                val, cnt, start = stack[-1]
                total_cost += cnt * (val - current_val)
                stack[-1] = (val, cnt + 1, start)
            else:
                stack.append((current_val, 1, right))
            
            # Shrink window from the left if cost exceeds k
            while total_cost > k:
                val, cnt, start = stack[0]
                # Subtract the cost contribution of the element being removed (nums[left])
                # The element nums[left] was adjusted to 'val'.
                # The cost incurred for this specific element is (val - original_value).
                total_cost -= (val - nums[start])
                
                if cnt == 1:
                    stack.pop(0)
                else:
                    # If the segment has more than 1 element, just decrement the count
                    # and update the start index. The value remains 'val' because
                    # the remaining elements in this segment were also adjusted to 'val'.
                    stack[0] = (val, cnt - 1, start + 1)
                
                left += 1
            
            # All subarrays ending at 'right' and starting from 'left' to 'right' are valid
            valid_count += (right - left + 1)
            
        return valid_count