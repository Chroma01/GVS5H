from typing import List
from collections import deque

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        
        # Helper to compute previous smaller element index
        def get_prev_smaller(arr):
            n = len(arr)
            prev = [-1] * n
            stack = []  # stores indices
            for i in range(n):
                while stack and arr[stack[-1]] > arr[i]:
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)
            return prev
        
        # Helper to compute next smaller or equal element index
        def get_next_smaller_equal(arr):
            n = len(arr)
            next_sm = [n] * n
            stack = []  # stores indices
            for i in range(n-1, -1, -1):
                while stack and arr[stack[-1]] >= arr[i]:
                    stack.pop()
                if stack:
                    next_sm[i] = stack[-1]
                stack.append(i)
            return next_sm
        
        # Helper to compute previous greater element index
        def get_prev_greater(arr):
            n = len(arr)
            prev = [-1] * n
            stack = []
            for i in range(n):
                while stack and arr[stack[-1]] < arr[i]:
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)
            return prev
        
        # Helper to compute next greater or equal element index
        def get_next_greater_equal(arr):
            n = len(arr)
            next_gre = [n] * n
            stack = []
            for i in range(n-1, -1, -1):
                while stack and arr[stack[-1]] <= arr[i]:
                    stack.pop()
                if stack:
                    next_gre[i] = stack[-1]
                stack.append(i)
            return next_gre
        
        # Compute arrays for min contribution
        prev_sm = get_prev_smaller(nums)
        next_sm_eq = get_next_smaller_equal(nums)
        
        # Compute arrays for max contribution
        prev_gr = get_prev_greater(nums)
        next_gr_eq = get_next_greater_equal(nums)
        
        def compute_count(a, b, k):
            """
            Compute the number of subarrays where the element is the min/max
            and the length is <= k.
            a = number of elements to the left (exclusive) that are >= current (for min) or <= current (for max)
            b = number of elements to the right (exclusive) that are > current (for min) or < current (for max)
            
            For min: prev_smaller gives strict smaller, so a = i - prev_sm[i] - 1
                     next_smaller_equal gives smaller or equal, so b = next_sm_eq[i] - i - 1
            For max: prev_greater gives strict greater, so a = i - prev_gr[i] - 1
                     next_greater_equal gives greater or equal, so b = next_gr_eq[i] - i - 1
            
            The count is: sum_{t=-a}^{0} (min(b, t+k-1) + 1)
            Let u = t + k - 1, then u from -a+k-1 to k-1
            f(u) = min(b, u) + 1
            """
            L = -a + k - 1
            R = k - 1
            
            if L > R:
                return 0
            
            if R <= b:
                # sum_{u=L}^{R} (u + 1)
                # = (L+1 + R+1) * (R - L + 1) // 2
                return (L + 1 + R + 1) * (R - L + 1) // 2
            elif L > b:
                # sum_{u=L}^{R} (b + 1)
                return (b + 1) * (R - L + 1)
            else:
                # sum_{u=L}^{b} (u+1) + sum_{u=b+1}^{R} (b+1)
                part1 = (L + 1 + b + 1) * (b - L + 1) // 2
                part2 = (b + 1) * (R - b)
                return part1 + part2
        
        total = 0
        for i in range(n):
            # For min
            a_min = i - prev_sm[i] - 1
            b_min = next_sm_eq[i] - i - 1
            count_min = compute_count(a_min, b_min, k)
            total += nums[i] * count_min
            
            # For max
            a_max = i - prev_gr[i] - 1
            b_max = next_gr_eq[i] - i - 1
            count_max = compute_count(a_max, b_max, k)
            total += nums[i] * count_max
            
        return total