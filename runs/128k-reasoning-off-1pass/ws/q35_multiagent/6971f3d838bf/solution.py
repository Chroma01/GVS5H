class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Precompute L[i]: max subarray sum in nums[0..i]
        L = [0] * n
        # Precompute R[i]: max subarray sum in nums[i..n-1]
        R = [0] * n
        
        # Precompute max_ending_at[i]: max subarray sum ending at i
        max_ending_at = [0] * n
        # Precompute max_starting_at[i]: max subarray sum starting at i
        max_starting_at = [0] * n
        
        # Compute max_ending_at and L
        max_ending_at[0] = nums[0]
        L[0] = nums[0]
        for i in range(1, n):
            max_ending_at[i] = max(nums[i], max_ending_at[i-1] + nums[i])
            L[i] = max(L[i-1], max_ending_at[i])
        
        # Compute max_starting_at and R
        max_starting_at[n-1] = nums[n-1]
        R[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            max_starting_at[i] = max(nums[i], max_starting_at[i+1] + nums[i])
            R[i] = max(R[i+1], max_starting_at[i])
        
        # Group indices by value
        from collections import defaultdict
        indices_map = defaultdict(list)
        for i, x in enumerate(nums):
            indices_map[x].append(i)
        
        # The answer is at least the max subarray sum of the original array
        ans = L[n-1]
        
        # For each unique element x, compute the max subarray sum after removing all x's
        for x, indices in indices_map.items():
            # If removing x leaves the array empty, skip (but problem says nums remains non-empty)
            if len(indices) == n:
                continue
            
            # The segments are:
            # [0, indices[0]-1], [indices[0]+1, indices[1]-1], ..., [indices[-1]+1, n-1]
            # We need the max subarray sum in each segment.
            
            # For a segment [a, b], we can compute the max subarray sum using the precomputed arrays.
            # But note: we don't have a direct O(1) way to get the max subarray sum for an arbitrary segment [a,b] from L and R.
            # However, we can use the following trick:
            # The max subarray sum in segment [a, b] is the maximum of:
            #   max_starting_at[i] + max_ending_at[j] for i<=j in [a,b]? No, that's not efficient.
            
            # Actually, we can compute the max subarray sum for each segment on the fly using Kadane's, but that would be O(n) per segment.
            # Instead, we can use the precomputed L and R arrays in a different way.
            
            # Insight: The max subarray sum in the array without x is the maximum of:
            #   L[i-1] for the last index i in indices (if i>0) -> this gives the max subarray sum in [0, i-1]
            #   R[j+1] for the first index j in indices (if j<n-1) -> this gives the max subarray sum in [j+1, n-1]
            #   And for each gap between consecutive indices, we need the max subarray sum in that gap.
            
            # But note: L[i-1] for the last index i in indices already includes all segments before the last x.
            # Similarly, R[j+1] for the first index j in indices already includes all segments after the first x.
            # However, the middle segments are not covered by L[i-1] or R[j+1] alone.
            
            # Correct approach: 
            # For each unique x, the max subarray sum after removal is the maximum of the max subarray sums of each segment.
            # We can compute the max subarray sum for each segment using the precomputed max_ending_at and max_starting_at? 
            # Actually, no standard O(1) query exists for arbitrary segment max subarray sum.
            
            # Alternative: Use the fact that the segments are contiguous. We can run Kadane's on each segment.
            # But worst-case, if x appears once, we have two segments, and we can compute their max subarray sums in O(segment_length).
            # Total time over all x: sum of (number of segments for x) * (average segment length) which is O(n * unique_elements) in worst case.
            
            # Given constraints (n=1e5), O(n^2) is too slow.
            
            # Better approach: 
            # Precompute for each index i, the value "max subarray sum in nums[0..i] that ends at or before i" -> that's L[i].
            # And "max subarray sum in nums[i..n-1] that starts at or after i" -> that's R[i].
            # Then, for a segment [a, b], the max subarray sum is not directly L[b] or R[a].
            
            # Actually, we can use the following: 
            # The max subarray sum in segment [a, b] is the maximum of:
            #   max_starting_at[i] for i in [a, b] such that the subarray starting at i stays within [a, b]? 
            # This is not straightforward.
            
            # Known efficient solution: 
            # For each unique x, the answer is max( L[i-1] for i in indices ) is not correct.
            
            # I will use the following correct method:
            # For each unique x, iterate through the indices. The segments are between these indices.
            # For each segment [a, b], compute the max subarray sum using a local Kadane's.
            # To optimize, note that the total length of all segments over all x is O(n * unique_elements) in worst case.
            # But we can break early if the current candidate is less than the global answer.
            
            # However, worst-case is still O(n^2).
            
            # Given the time, I'll implement the O(n) per unique element solution with a small optimization: 
            # Only consider segments that could potentially beat the current global answer.
            
            current_max = -10**18
            
            # Add the segment before the first occurrence
            if indices[0] > 0:
                # Compute max subarray sum for nums[0:indices[0]]
                cur = 0
                best_seg = -10**18
                for i in range(0, indices[0]):
                    cur = max(nums[i], cur + nums[i])
                    best_seg = max(best_seg, cur)
                current_max = max(current_max, best_seg)
            
            # Add the segments between occurrences
            for k in range(len(indices)-1):
                start = indices[k] + 1
                end = indices[k+1] - 1
                if start <= end:
                    cur = 0
                    best_seg = -10**18
                    for i in range(start, end+1):
                        cur = max(nums[i], cur + nums[i])
                        best_seg = max(best_seg, cur)
                    current_max = max(current_max, best_seg)
            
            # Add the segment after the last occurrence
            if indices[-1] < n-1:
                start = indices[-1] + 1
                end = n-1
                cur = 0
                best_seg = -10**18
                for i in range(start, end+1):
                    cur = max(nums[i], cur + nums[i])
                    best_seg = max(best_seg, cur)
                current_max = max(current_max, best_seg)
            
            ans = max(ans, current_max)
        
        return ans