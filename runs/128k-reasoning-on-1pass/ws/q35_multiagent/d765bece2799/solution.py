from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        
        def count_pairs(l, r, T):
            # Count pairs (x, y) such that 1 <= x <= l, 1 <= y <= r, x + y <= T
            if T <= 1: 
                return 0
            x0 = T - r
            end1 = min(l, x0)
            if end1 < 1: 
                end1 = 0
            sum1 = end1 * r
            
            start2 = max(1, x0 + 1)
            end2 = min(l, T - 1)
            if start2 > end2:
                sum2 = 0
            else:
                num_terms = end2 - start2 + 1
                first = T - start2
                last = T - end2
                sum2 = num_terms * (first + last) // 2
            return sum1 + sum2

        # For maximums: strictly greater on left, greater or equal on right
        prev_greater = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            if stack:
                prev_greater[i] = stack[-1]
            stack.append(i)
            
        next_ge = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            if stack:
                next_ge[i] = stack[-1]
            stack.append(i)
            
        s_max = 0
        for i in range(n):
            l = i - prev_greater[i]
            r = next_ge[i] - i
            s_max += nums[i] * count_pairs(l, r, k + 1)
            
        # For minimums: strictly smaller on left, smaller or equal on right
        prev_smaller = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            if stack:
                prev_smaller[i] = stack[-1]
            stack.append(i)
            
        next_se = [n] * n
        stack = []
        for i in range(n - 1, -1, -1):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            if stack:
                next_se[i] = stack[-1]
            stack.append(i)
            
        s_min = 0
        for i in range(n):
            l = i - prev_smaller[i]
            r = next_se[i] - i
            s_min += nums[i] * count_pairs(l, r, k + 1)
            
        return s_max + s_min