from typing import List
from collections import defaultdict
import math

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Precompute max subarray sum ending at each index
        max_ending = [0] * n
        current_max = 0
        for i in range(n):
            current_max = max(nums[i], current_max + nums[i])
            max_ending[i] = current_max
            
        # Precompute max subarray sum starting at each index
        max_starting = [0] * n
        current_max = 0
        for i in range(n - 1, -1, -1):
            current_max = max(nums[i], current_max + nums[i])
            max_starting[i] = current_max
            
        # Precompute global max subarray sum for the original array
        global_max = max(max_ending)
        ans = global_max
        
        # Precompute prefix sums for O(1) range sum queries
        prefix_sum = [0] * (n + 1)
        for i in range(n):
            prefix_sum[i+1] = prefix_sum[i] + nums[i]
            
        def get_sum(l, r):
            return prefix_sum[r+1] - prefix_sum[l]
            
        # Build Sparse Table for RMQ on max_ending to find max subarray sum within a segment in O(1)
        # st[j][i] stores the max value in max_ending[i ... i + 2^j - 1]
        K = math.ceil(math.log2(n + 1)) if n > 0 else 0
        st = [[0] * n for _ in range(K)]
        
        # Initialize level 0
        for i in range(n):
            st[0][i] = max_ending[i]
            
        # Build table
        for j in range(1, K):
            length = 1 << (j - 1)
            for i in range(n - (1 << j) + 1):
                val1 = st[j-1][i]
                val2 = st[j-1][i + length]
                st[j][i] = max(val1, val2)
                
        def query_max_ending(l, r):
            if l > r:
                return -float('inf')
            j = int(math.log2(r - l + 1))
            return max(st[j][l], st[j][r - (1 << j) + 1])
            
        # Group indices by value to efficiently process removals
        indices_map = defaultdict(list)
        for i, num in enumerate(nums):
            indices_map[num].append(i)
            
        # For each unique number x, simulate its removal
        for x, indices in indices_map.items():
            blocks = []
            
            # Segment 0: from 0 to indices[0]-1
            start = 0
            end = indices[0] - 1
            if start <= end:
                seg_sum = get_sum(start, end)
                seg_max_suffix = max_ending[end]
                seg_max_prefix = max_starting[start]
                seg_max_sub = query_max_ending(start, end)
                blocks.append((seg_sum, seg_max_prefix, seg_max_suffix, seg_max_sub))
            
            # Intermediate segments
            for k in range(len(indices) - 1):
                start = indices[k] + 1
                end = indices[k+1] - 1
                if start <= end:
                    seg_sum = get_sum(start, end)
                    seg_max_suffix = max_ending[end]
                    seg_max_prefix = max_starting[start]
                    seg_max_sub = query_max_ending(start, end)
                    blocks.append((seg_sum, seg_max_prefix, seg_max_suffix, seg_max_sub))
            
            # Last segment: from indices[-1]+1 to n-1
            start = indices[-1] + 1
            end = n - 1
            if start <= end:
                seg_sum = get_sum(start, end)
                seg_max_suffix = max_ending[end]
                seg_max_prefix = max_starting[start]
                seg_max_sub = query_max_ending(start, end)
                blocks.append((seg_sum, seg_max_prefix, seg_max_suffix, seg_max_sub))
            
            # Run Kadane's algorithm on the sequence of blocks
            # Each block represents a contiguous segment of non-x elements
            # We treat each block as a "super-element" that can be merged with neighbors
            current_max = -float('inf')
            for seg_sum, seg_max_prefix, seg_max_suffix, seg_max_sub in blocks:
                if current_max == -float('inf'):
                    current_max = seg_max_sub
                else:
                    # Either start a new subarray within this block, or extend the previous one
                    current_max = max(seg_max_sub, seg_max_prefix + current_max)
                
                if current_max > ans:
                    ans = current_max
                    
        return ans