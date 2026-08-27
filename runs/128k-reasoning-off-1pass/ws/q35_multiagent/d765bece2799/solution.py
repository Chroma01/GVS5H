class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def sum_of_extremes(nums, k, is_max):
            n = len(nums)
            # prev[i] is the index of the previous element that breaks the monotonicity
            # next[i] is the index of the next element that breaks the monotonicity
            # For max: prev is previous greater, next is next greater or equal
            # For min: prev is previous smaller, next is next smaller or equal
            
            prev = [-1] * n
            next_idx = [n] * n
            
            stack = []
            if is_max:
                # Previous greater: strictly greater
                for i in range(n):
                    while stack and nums[stack[-1]] <= nums[i]:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)
                
                stack = []
                # Next greater or equal: greater or equal
                for i in range(n - 1, -1, -1):
                    while stack and nums[stack[-1]] < nums[i]:
                        stack.pop()
                    if stack:
                        next_idx[i] = stack[-1]
                    stack.append(i)
            else:
                # Previous smaller: strictly smaller
                for i in range(n):
                    while stack and nums[stack[-1]] >= nums[i]:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)
                
                stack = []
                # Next smaller or equal: smaller or equal
                for i in range(n - 1, -1, -1):
                    while stack and nums[stack[-1]] > nums[i]:
                        stack.pop()
                    if stack:
                        next_idx[i] = stack[-1]
                    stack.append(i)
            
            total = 0
            for i in range(n):
                # Distance to previous breaking element
                left_dist = i - prev[i]
                # Distance to next breaking element
                right_dist = next_idx[i] - i
                
                # We want to count pairs (l, r) such that:
                # 0 <= l <= left_dist - 1
                # 0 <= r <= right_dist - 1
                # l + r + 1 <= k  => l + r <= k - 1
                
                limit = k - 1
                a = left_dist - 1  # max l
                b = right_dist - 1 # max r
                
                # If even the smallest subarray (l=0, r=0) has length > k, skip
                if limit < 0:
                    continue
                
                # Count number of pairs (l, r) with 0 <= l <= a, 0 <= r <= b, l + r <= limit
                # This is equivalent to sum_{l=0}^{min(a, limit)} min(b, limit - l)
                
                # Determine the range of l
                l_max = min(a, limit)
                
                # For l from 0 to l_max, r can be from 0 to min(b, limit - l)
                # Split into two parts:
                # Part 1: where limit - l >= b, i.e., l <= limit - b
                # Part 2: where limit - l < b, i.e., l > limit - b
                
                # Find the split point
                split = limit - b
                
                # Part 1: l from 0 to min(l_max, split)
                # In this range, min(b, limit - l) = b
                end1 = min(l_max, split)
                if end1 >= 0:
                    count1 = (end1 + 1) * b
                else:
                    count1 = 0
                
                # Part 2: l from max(0, split + 1) to l_max
                # In this range, min(b, limit - l) = limit - l
                start2 = max(0, split + 1)
                if start2 <= l_max:
                    # Sum of (limit - l) for l from start2 to l_max
                    # = sum_{j=limit-l_max}^{limit-start2} j
                    # Let low = limit - l_max, high = limit - start2
                    low = limit - l_max
                    high = limit - start2
                    # Sum of integers from low to high
                    count2 = (high * (high + 1) // 2) - ((low - 1) * low // 2)
                else:
                    count2 = 0
                
                count = count1 + count2
                total += nums[i] * count
            
            return total
        
        return sum_of_extremes(nums, k, True) + sum_of_extremes(nums, k, False)