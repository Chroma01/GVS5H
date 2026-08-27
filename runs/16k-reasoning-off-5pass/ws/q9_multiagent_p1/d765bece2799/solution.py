from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        total_sum = 0
        
        # Helper to compute boundaries using monotonic stack
        # strict_left: if True, find nearest element to left that is STRICTLY greater (for max) or STRICTLY smaller (for min)
        # strict_right: if True, find nearest element to right that is STRICTLY greater (for max) or STRICTLY smaller (for min)
        # We use strict on one side and non-strict on the other to handle duplicates correctly.
        # For Max: left is strict (>), right is non-strict (>=).
        # For Min: left is strict (<), right is non-strict (<=).
        def get_boundaries(arr, n, strict_left, strict_right):
            left = [-1] * n
            stack = []
            if strict_left:
                # Find nearest element to left that is > arr[i]
                for i in range(n):
                    while stack and arr[stack[-1]] <= arr[i]:
                        stack.pop()
                    if stack:
                        left[i] = stack[-1]
                    stack.append(i)
            else:
                # Find nearest element to left that is < arr[i]
                for i in range(n):
                    while stack and arr[stack[-1]] >= arr[i]:
                        stack.pop()
                    if stack:
                        left[i] = stack[-1]
                    stack.append(i)
            
            right = [n] * n
            stack = []
            if strict_right:
                # Find nearest element to right that is >= arr[i] (for max)
                # Logic: pop while stack top is < current
                for i in range(n - 1, -1, -1):
                    while stack and arr[stack[-1]] < arr[i]:
                        stack.pop()
                    if stack:
                        right[i] = stack[-1]
                    stack.append(i)
            else:
                # Find nearest element to right that is <= arr[i] (for min)
                # Logic: pop while stack top is > current
                for i in range(n - 1, -1, -1):
                    while stack and arr[stack[-1]] > arr[i]:
                        stack.pop()
                    if stack:
                        right[i] = stack[-1]
                    stack.append(i)
            
            return left, right

        # Compute boundaries for Max
        # left_max: nearest index to left with value > nums[i]
        # right_max: nearest index to right with value >= nums[i]
        left_max, right_max = get_boundaries(nums, n, strict_left=True, strict_right=False)
        
        # Compute boundaries for Min
        # left_min: nearest index to left with value < nums[i]
        # right_min: nearest index to right with value <= nums[i]
        left_min, right_min = get_boundaries(nums, n, strict_left=False, strict_right=False)
        
        for i in range(n):
            # Contribution as Max
            # Valid start s must be in (left_max[i], i]
            # Valid end e must be in [i, right_max[i])
            # Constraint: e - s + 1 <= k  =>  s >= e - k + 1
            
            L_max = left_max[i] + 1
            R_max = right_max[i] - 1
            
            # The end point e can range from i to min(R_max, i + k - 1)
            # Because if e > i + k - 1, the length e - i + 1 > k, which is invalid even if s=i.
            end_e_max = min(R_max, i + k - 1)
            
            if end_e_max >= i:
                # We need to sum over e in [i, end_e_max]: count(s) * nums[i]
                # count(s) = i - max(L_max, e - k + 1) + 1
                
                # Split the range of e into two parts based on which term in max() is larger.
                # Part 1: e - k + 1 <= L_max  =>  e <= L_max + k - 1
                # In this part, max(L_max, e - k + 1) = L_max
                # count = i - L_max + 1 (constant)
                
                limit1 = min(end_e_max, L_max + k - 1)
                count1 = limit1 - i + 1
                if count1 > 0:
                    term = i + 1 - L_max
                    total_sum += nums[i] * count1 * term
                
                # Part 2: e > L_max + k - 1  =>  e >= L_max + k
                # In this part, max(L_max, e - k + 1) = e - k + 1
                # count = i - (e - k + 1) + 1 = i + k - e
                
                start2 = max(i, L_max + k)
                if start2 <= end_e_max:
                    count2 = end_e_max - start2 + 1
                    # Sum of e from start2 to end_e_max
                    sum_e = (start2 + end_e_max) * count2 // 2
                    # Sum of count = sum(i + k - e) = count2 * (i + k) - sum_e
                    term2 = (i + k) * count2 - sum_e
                    total_sum += nums[i] * term2
            
            # Contribution as Min
            L_min = left_min[i] + 1
            R_min = right_min[i] - 1
            
            end_e_min = min(R_min, i + k - 1)
            
            if end_e_min >= i:
                limit1 = min(end_e_min, L_min + k - 1)
                count1 = limit1 - i + 1
                if count1 > 0:
                    term = i + 1 - L_min
                    total_sum += nums[i] * count1 * term
                
                start2 = max(i, L_min + k)
                if start2 <= end_e_min:
                    count2 = end_e_min - start2 + 1
                    sum_e = (start2 + end_e_min) * count2 // 2
                    term2 = (i + k) * count2 - sum_e
                    total_sum += nums[i] * term2
                    
        return total_sum

if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    nums1 = [1, 2, 3]
    k1 = 2
    result1 = sol.minMaxSubarraySum(nums1, k1)
    print(f"Example 1: Input: nums = {nums1}, k = {k1}")
    print(f"Output: {result1}, Expected: 20")
    
    # Example 2
    nums2 = [1, -3, 1]
    k2 = 2
    result2 = sol.minMaxSubarraySum(nums2, k2)
    print(f"Example 2: Input: nums = {nums2}, k = {k2}")
    print(f"Output: {result2}, Expected: -6")
    
    # Additional Test: Single element
    nums3 = [5]
    k3 = 1
    result3 = sol.minMaxSubarraySum(nums3, k3)
    print(f"Example 3: Input: nums = {nums3}, k = {k3}")
    print(f"Output: {result3}, Expected: 10")
    
    # Additional Test: k = n
    nums4 = [1, 2, 3]
    k4 = 3
    result4 = sol.minMaxSubarraySum(nums4, k4)
    print(f"Example 4: Input: nums = {nums4}, k = {k4}")
    print(f"Output: {result4}, Expected: 24")