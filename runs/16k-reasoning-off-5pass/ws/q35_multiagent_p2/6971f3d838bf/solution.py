class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        
        # Helper function to compute max subarray sum, max prefix sum, max suffix sum for a list
        def get_segment_info(arr):
            if not arr:
                return (float('-inf'), float('-inf'), float('-inf'))
            
            # Kadane's for max subarray sum
            max_so_far = arr[0]
            current_max = arr[0]
            
            # Max prefix sum
            max_pre = arr[0]
            current_pre = arr[0]
            
            # Max suffix sum
            max_suf = arr[0]
            current_suf = arr[0]
            
            for i in range(1, len(arr)):
                # Kadane's
                current_max = max(arr[i], current_max + arr[i])
                max_so_far = max(max_so_far, current_max)
                
                # Prefix
                current_pre = max(arr[i], current_pre + arr[i])
                max_pre = max(max_pre, current_pre)
                
                # Suffix: we can compute by reversing or doing a second pass, 
                # but here we do a single pass for suffix by tracking from right? 
                # Actually, for simplicity and since segments might be small on average, 
                # we can just compute suffix in a separate pass or use a different method.
                # Let's compute suffix properly:
                # We'll do a second pass for suffix to be safe and clear.
                pass
            
            # Recompute suffix properly
            max_suf = arr[-1]
            current_suf = arr[-1]
            for i in range(len(arr)-2, -1, -1):
                current_suf = max(arr[i], current_suf + arr[i])
                max_suf = max(max_suf, current_suf)
                
            return (max_so_far, max_pre, max_suf)
        
        # 1. Original max subarray sum
        orig_max, _, _ = get_segment_info(nums)
        ans = orig_max
        
        # 2. Group indices by value
        from collections import defaultdict
        indices_map = defaultdict(list)
        for i, num in enumerate(nums):
            indices_map[num].append(i)
        
        # 3. For each unique negative number, compute max subarray sum after removal
        # Only negative numbers can potentially increase the max subarray sum when removed.
        # (Removing a positive number can only decrease or keep the same the max subarray sum)
        for x, idxs in indices_map.items():
            if x >= 0:
                continue
            
            # The array is split into segments by the occurrences of x
            # Segments are between consecutive indices of x
            # Add boundaries: -1 and n
            all_indices = [-1] + idxs + [n]
            
            # We'll collect segment info: (max_sub, max_pre, max_suf) for each segment
            segments_info = []
            
            for k in range(len(all_indices) - 1):
                start = all_indices[k] + 1
                end = all_indices[k+1]  # exclusive
                if start < end:
                    seg = nums[start:end]
                    segments_info.append(get_segment_info(seg))
                else:
                    # Empty segment, skip
                    segments_info.append(None)
            
            # Now, the max subarray sum for this removal is the max of:
            # a) max_sub of any single segment
            # b) max_suf of segment i + max_pre of segment i+1 for adjacent non-empty segments
            
            current_max = float('-inf')
            
            # Check single segments
            for info in segments_info:
                if info is not None:
                    current_max = max(current_max, info[0])
            
            # Check combinations of adjacent segments
            for k in range(len(segments_info) - 1):
                if segments_info[k] is not None and segments_info[k+1] is not None:
                    combined = segments_info[k][2] + segments_info[k+1][1]
                    current_max = max(current_max, combined)
            
            ans = max(ans, current_max)
            
        return ans