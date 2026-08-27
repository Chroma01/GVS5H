from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Precompute prefix max subarray sums
        # pre_max[i] = max subarray sum in nums[0...i]
        pre_max = [0] * n
        current_max = nums[0]
        pre_max[0] = nums[0]
        for i in range(1, n):
            current_max = max(nums[i], current_max + nums[i])
            pre_max[i] = max(pre_max[i-1], current_max)
            
        # Precompute suffix max subarray sums
        # suf_max[i] = max subarray sum in nums[i...n-1]
        suf_max = [0] * n
        current_max = nums[n-1]
        suf_max[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            current_max = max(nums[i], current_max + nums[i])
            suf_max[i] = max(suf_max[i+1], current_max)
            
        # Precompute prefix sums and suffix sums to handle the case where we might want to
        # consider the sum of the entire left part or entire right part if they are all positive?
        # Actually, the logic is simpler:
        # If we remove x, the array splits into nums[0...first-1] and nums[last+1...n-1].
        # The max subarray is max(max_subarray(left), max_subarray(right)).
        # However, we must ensure the subarray is non-empty.
        # If left part exists, its max subarray is pre_max[first-1].
        # If right part exists, its max subarray is suf_max[last+1].
        # We take the max of these two if both exist, or just the one that exists.
        # But wait, is it possible that the "max subarray" of the left part is negative?
        # Yes, if all numbers in left part are negative. But the problem says "non-empty".
        # So if left part is not empty, we MUST pick at least one element from it.
        # The standard Kadane's algorithm (as implemented above) returns the max subarray sum
        # which could be negative if all numbers are negative. This is correct for "non-empty".
        
        # We need to know the first and last occurrence of each number.
        first_occ = {}
        last_occ = {}
        for i, x in enumerate(nums):
            if x not in first_occ:
                first_occ[x] = i
            last_occ[x] = i
            
        # Calculate the original max subarray sum (case where we do nothing)
        original_max = pre_max[n-1]
        
        ans = original_max
        
        # Iterate over all unique numbers
        unique_nums = set(nums)
        
        for x in unique_nums:
            first = first_occ[x]
            last = last_occ[x]
            
            # Check if removing x leaves the array non-empty
            # The array becomes empty only if n == 1 (since we remove the only element)
            if n == 1:
                continue
                
            # Identify the left part: nums[0...first-1]
            # Identify the right part: nums[last+1...n-1]
            
            left_max = -float('inf')
            right_max = -float('inf')
            left_exists = False
            right_exists = False
            
            if first > 0:
                left_exists = True
                left_max = pre_max[first-1]
            
            if last < n - 1:
                right_exists = True
                right_max = suf_max[last+1]
            
            if left_exists and right_exists:
                current_max = max(left_max, right_max)
            elif left_exists:
                current_max = left_max
            elif right_exists:
                current_max = right_max
            else:
                # This case should be covered by n==1 check, but for safety:
                continue
                
            ans = max(ans, current_max)
            
        return ans