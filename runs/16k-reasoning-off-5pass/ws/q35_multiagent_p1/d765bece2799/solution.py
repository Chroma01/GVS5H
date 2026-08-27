class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        
        # Helper to find previous less element index
        def get_prev_less(arr):
            n_arr = len(arr)
            prev = [-1] * n_arr
            stack = []  # stores indices
            for i in range(n_arr):
                while stack and arr[stack[-1]] > arr[i]:
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)
            return prev
        
        # Helper to find next less element index
        def get_next_less(arr):
            n_arr = len(arr)
            next_ = [n_arr] * n_arr
            stack = []  # stores indices
            for i in range(n_arr - 1, -1, -1):
                while stack and arr[stack[-1]] >= arr[i]:
                    stack.pop()
                if stack:
                    next_[i] = stack[-1]
                stack.append(i)
            return next_
        
        # Helper to find previous greater element index
        def get_prev_greater(arr):
            n_arr = len(arr)
            prev = [-1] * n_arr
            stack = []  # stores indices
            for i in range(n_arr):
                while stack and arr[stack[-1]] < arr[i]:
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)
            return prev
        
        # Helper to find next greater element index
        def get_next_greater(arr):
            n_arr = len(arr)
            next_ = [n_arr] * n_arr
            stack = []  # stores indices
            for i in range(n_arr - 1, -1, -1):
                while stack and arr[stack[-1]] <= arr[i]:
                    stack.pop()
                if stack:
                    next_[i] = stack[-1]
                stack.append(i)
            return next_
        
        # Function to calculate sum of mins/maxs for subarrays of length <= k
        def calculate_sum(arr, prev_boundary, next_boundary):
            total = 0
            for i in range(n):
                val = arr[i]
                # L is the number of choices for left endpoint: from prev_boundary[i]+1 to i
                L = i - prev_boundary[i]
                # R is the number of choices for right endpoint: from i to next_boundary[i]-1
                R = next_boundary[i] - i
                
                # We need to count pairs (a, b) such that:
                # 0 <= a < L, 0 <= b < R, and a + b + 1 <= k
                # i.e., a + b <= k - 1
                # a ranges from 0 to min(L-1, k-1)
                max_a = min(L - 1, k - 1)
                
                # For each a, b can range from 0 to min(R-1, k - 1 - a)
                # So count for a given a is min(R, k - a)
                # But if k - a <= 0, then count is 0.
                
                # We split the range of a into two parts:
                # Let threshold = k - R. 
                # If a <= threshold, then k - a >= R, so min(R, k-a) = R
                # If a > threshold, then k - a < R, so min(R, k-a) = k - a
                
                # But we also have the constraint that a <= max_a and a >= 0.
                
                threshold = k - R
                
                # Part 1: a from 0 to min(max_a, threshold)
                end1 = min(max_a, threshold)
                if end1 >= 0:
                    count1 = end1 + 1
                    total += val * count1 * R
                
                # Part 2: a from max(0, threshold + 1) to max_a
                start2 = max(0, threshold + 1)
                if start2 <= max_a:
                    # Sum of (k - a) for a from start2 to max_a
                    # This is an arithmetic series
                    # Number of terms = max_a - start2 + 1
                    num_terms = max_a - start2 + 1
                    first_term = k - start2
                    last_term = k - max_a
                    sum_series = num_terms * (first_term + last_term) // 2
                    total += val * sum_series
                    
            return total
        
        # Calculate sum of minimums
        prev_less = get_prev_less(nums)
        next_less = get_next_less(nums)
        sum_min = calculate_sum(nums, prev_less, next_less)
        
        # Calculate sum of maximums
        prev_greater = get_prev_greater(nums)
        next_greater = get_next_greater(nums)
        sum_max = calculate_sum(nums, prev_greater, next_greater)
        
        return sum_min + sum_max