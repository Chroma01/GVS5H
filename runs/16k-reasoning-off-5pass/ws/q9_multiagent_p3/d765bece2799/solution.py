from collections import deque
from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        total_sum = 0
        
        # Deque for maximums: stores indices, values are decreasing
        max_dq = deque()
        # Deque for minimums: stores indices, values are increasing
        min_dq = deque()
        
        for i in range(n):
            # Update max_dq: maintain decreasing order
            while max_dq and nums[max_dq[-1]] <= nums[i]:
                max_dq.pop()
            max_dq.append(i)
            
            # Update min_dq: maintain increasing order
            while min_dq and nums[min_dq[-1]] >= nums[i]:
                min_dq.pop()
            min_dq.append(i)
            
            # Remove indices that are out of the window [i-k+1, i]
            # The window of valid start indices is [i-k+1, i]
            # So any index < i-k+1 is invalid
            remove_idx = i - k + 1
            
            # For max_dq
            if max_dq[0] < remove_idx:
                max_dq.popleft()
            
            # For min_dq
            if min_dq[0] < remove_idx:
                min_dq.popleft()
            
            # Calculate contribution of current max
            # The max element is at max_dq[0]
            # It is the maximum for all subarrays ending at i that start at index j
            # where max_dq[0] <= j <= i.
            # Also, the subarray length constraint is j >= i - k + 1.
            # So valid j range is [max(max_dq[0], i - k + 1), i]
            # Count of such subarrays = i - max(max_dq[0], i - k + 1) + 1
            # Note: Since we already popped indices < i-k+1 from the front, max_dq[0] is guaranteed >= i-k+1.
            # So the lower bound is simply max_dq[0].
            # So count = i - max_dq[0] + 1.
            
            count_max = i - max_dq[0] + 1
            total_sum += count_max * nums[max_dq[0]]
            
            # Calculate contribution of current min
            count_min = i - min_dq[0] + 1
            total_sum += count_min * nums[min_dq[0]]
            
        return total_sum