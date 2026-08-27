from typing import List
from collections import defaultdict

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # 1. Precompute max_ending_here and max_starting_here
        # max_ending[i]: max subarray sum ending at index i
        # max_starting[i]: max subarray sum starting at index i
        max_ending = [0] * n
        max_starting = [0] * n
        
        # Forward pass for max_ending
        current_max = nums[0]
        max_ending[0] = nums[0]
        for i in range(1, n):
            current_max = max(nums[i], current_max + nums[i])
            max_ending[i] = current_max
            
        # Backward pass for max_starting
        current_max = nums[n-1]
        max_starting[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            current_max = max(nums[i], current_max + nums[i])
            max_starting[i] = current_max
            
        # 2. Precompute global_max_prefix and global_max_suffix
        # global_max_prefix[i]: max subarray sum in nums[0...i]
        # global_max_suffix[i]: max subarray sum in nums[i...n-1]
        global_max_prefix = [0] * n
        global_max_suffix = [0] * n
        
        # Forward pass for global_max_prefix
        current_max = nums[0]
        global_max_prefix[0] = nums[0]
        for i in range(1, n):
            current_max = max(current_max + nums[i], nums[i])
            global_max_prefix[i] = max(global_max_prefix[i-1], current_max)
            
        # Backward pass for global_max_suffix
        current_max = nums[n-1]
        global_max_suffix[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            current_max = max(current_max + nums[i], nums[i])
            global_max_suffix[i] = max(global_max_suffix[i+1], current_max)
            
        # 3. Store positions of each number
        positions = defaultdict(list)
        for i, x in enumerate(nums):
            positions[x].append(i)
            
        # 4. Calculate original max subarray sum (case: no operation)
        original_max = global_max_prefix[n-1]
        ans = original_max
        
        # 5. Iterate over unique numbers to try removing them
        for x, indices in positions.items():
            first = indices[0]
            last = indices[-1]
            
            # Check if removing x leaves the array empty
            # This happens if the array consists only of x
            if first == 0 and last == n - 1:
                continue
            
            # Candidates for new max subarray sum
            candidates = []
            
            # Candidate 1: Max subarray in the left part (0 to first-1)
            if first > 0:
                candidates.append(global_max_prefix[first-1])
            
            # Candidate 2: Max subarray in the right part (last+1 to n-1)
            if last < n - 1:
                candidates.append(global_max_suffix[last+1])
            
            # Candidate 3: Combination of suffix of left part and prefix of right part
            # Suffix of left part ending at first-1: max_ending[first-1]
            # Prefix of right part starting at last+1: max_starting[last+1]
            if first > 0 and last < n - 1:
                candidates.append(max_ending[first-1] + max_starting[last+1])
            
            if candidates:
                ans = max(ans, max(candidates))
                
        return ans