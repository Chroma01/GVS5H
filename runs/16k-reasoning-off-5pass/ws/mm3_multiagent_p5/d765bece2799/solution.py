from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        prev_smaller = [0] * n
        prev_larger = [0] * n
        
        # Monotonic increasing stack for previous strictly smaller element
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            prev_smaller[i] = stack[-1] if stack else -1
            stack.append(i)
        
        # Monotonic decreasing stack for previous strictly larger element
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            prev_larger[i] = stack[-1] if stack else -1
            stack.append(i)
        
        total = 0
        for i in range(n):
            count_min = min(i - prev_smaller[i], k)
            count_max = min(i - prev_larger[i], k)
            total += nums[i] * (count_min + count_max)
        
        return total