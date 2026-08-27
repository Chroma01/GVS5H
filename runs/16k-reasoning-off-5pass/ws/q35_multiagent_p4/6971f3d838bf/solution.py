class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Global max subarray sum using Kadane's
        max_so_far = nums[0]
        current_max = nums[0]
        for i in range(1, n):
            current_max = max(nums[i], current_max + nums[i])
            max_so_far = max(max_so_far, current_max)
        
        # If only one element, return it
        if n == 1:
            return max_so_far
        
        # Build Sparse Table for Range Max Subarray Sum
        # Each node stores: (total_sum, max_prefix, max_suffix, max_sub)
        # LOG_N = ceil(log2(n)) + 1
        import math
        LOG_N = n.bit_length()
        
        # st[k][i] represents the node for range starting at i with length 2^k
        st = [[None] * n for _ in range(LOG_N)]
        
        # Initialize level 0 (length 1)
        for i in range(n):
            val = nums[i]
            st[0][i] = (val, val, val, val)
        
        # Build the sparse table
        for k in range(1, LOG_N):
            length = 1 << k
            half = 1 << (k - 1)
            for i in range(n - length + 1):
                left = st[k-1][i]
                right = st[k-1][i + half]
                
                # Merge logic
                total_sum = left[0] + right[0]
                max_prefix = max(left[1], left[0] + right[1])
                max_suffix = max(right[2], right[0] + left[2])
                max_sub = max(left[3], right[3], left[2] + right[1])
                
                st[k][i] = (total_sum, max_prefix, max_suffix, max_sub)
        
        def query(l, r):
            """Returns (total_sum, max_prefix, max_suffix, max_sub) for range [l, r]"""
            if l > r:
                return None
            
            length = r - l + 1
            k = length.bit_length() - 1
            
            left_node = st[k][l]
            right_node = st[k][r - (1 << k) + 1]
            
            total_sum = left_node[0] + right_node[0]
            max_prefix = max(left_node[1], left_node[0] + right_node[1])
            max_suffix = max(right_node[2], right_node[0] + left_node[2])
            max_sub = max(left_node[3], right_node[3], left_node[2] + right_node[1])
            
            return (total_sum, max_prefix, max_suffix, max_sub)
        
        # Group indices by value
        from collections import defaultdict
        positions = defaultdict(list)
        for i, num in enumerate(nums):
            positions[num].append(i)
        
        ans = max_so_far
        
        # For each unique element, consider removing it
        for x, pos_list in positions.items():
            # The segments are defined by the positions of x
            # Segments: [0, pos_list[0]-1], [pos_list[0]+1, pos_list[1]-1], ..., [pos_list[-1]+1, n-1]
            prev = -1
            for p in pos_list:
                # Segment from prev+1 to p-1
                l, r = prev + 1, p - 1
                if l <= r:
                    res = query(l, r)
                    if res:
                        ans = max(ans, res[3])
                prev = p
            
            # Last segment after the last occurrence
            l, r = prev + 1, n - 1
            if l <= r:
                res = query(l, r)
                if res:
                    ans = max(ans, res[3])
        
        return ans