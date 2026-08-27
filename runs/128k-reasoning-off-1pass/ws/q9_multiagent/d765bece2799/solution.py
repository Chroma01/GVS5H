from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def get_boundaries(arr: List[int], n: int, is_min: bool) -> tuple[List[int], List[int]]:
            # Find previous boundary and next boundary for each element
            # To ensure unique counting of subarrays:
            # For Max: prev is nearest index with value >= current, next is nearest index with value > current
            # For Min: prev is nearest index with value <= current, next is nearest index with value < current
            
            prev = [-1] * n
            next = [n] * n
            
            stack = []
            
            # Previous boundary
            for i in range(n):
                val = arr[i]
                # We want to keep elements that are >= (for Max) or <= (for Min) in the stack.
                # So we pop elements that are strictly smaller (for Max) or strictly larger (for Min).
                # Condition to pop: (is_min and arr[top] > val) or (not is_min and arr[top] < val)
                while stack and ((is_min and arr[stack[-1]] > val) or (not is_min and arr[stack[-1]] < val)):
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)
            
            stack = []
            # Next boundary
            for i in range(n - 1, -1, -1):
                val = arr[i]
                # We want to keep elements that are > (for Max) or < (for Min) in the stack.
                # So we pop elements that are <= (for Max) or >= (for Min).
                # Condition to pop: (is_min and arr[top] >= val) or (not is_min and arr[top] <= val)
                while stack and ((is_min and arr[stack[-1]] >= val) or (not is_min and arr[stack[-1]] <= val)):
                    stack.pop()
                if stack:
                    next[i] = stack[-1]
                stack.append(i)
            
            return prev, next

        def count_pairs(L: int, R: int, limit: int) -> int:
            # Count pairs (x, y) such that 0 <= x < L, 0 <= y < R, and x + y <= limit
            # This is equivalent to summing min(R, limit - x + 1) for x in 0..L-1
            # Optimized to O(1) using arithmetic series.
            
            if L == 0 or R == 0:
                return 0
            
            # x ranges from 0 to L-1. Also x <= limit.
            max_x = min(L - 1, limit)
            if max_x < 0:
                return 0
            
            # We sum (min(R, limit - x + 1)) for x in 0..max_x
            # Let term(x) = min(R, limit - x + 1)
            # The term is R when limit - x + 1 >= R  =>  x <= limit - R + 1
            # The term is limit - x + 1 when x > limit - R + 1
            
            threshold = limit - R + 1
            
            # Part 1: x from 0 to min(max_x, threshold)
            # In this range, term(x) = R
            part1_end = min(max_x, threshold)
            count1 = part1_end + 1
            sum1 = count1 * R
            
            # Part 2: x from part1_end + 1 to max_x
            # In this range, term(x) = limit - x + 1
            # This is an arithmetic progression.
            # First term (at x = part1_end + 1): limit - (part1_end + 1) + 1 = limit - part1_end
            # Last term (at x = max_x): limit - max_x + 1
            # Number of terms: max_x - (part1_end + 1) + 1 = max_x - part1_end
            
            if max_x > part1_end:
                first_term = limit - part1_end
                last_term = limit - max_x + 1
                count2 = max_x - part1_end
                sum2 = (first_term + last_term) * count2 // 2
            else:
                sum2 = 0
                
            return sum1 + sum2

        n = len(nums)
        total_sum = 0
        
        # Calculate contribution for Maximums
        # For Max: prev is nearest >=, next is nearest >
        prev_max, next_max = get_boundaries(nums, n, is_min=False)
        for i in range(n):
            lenL = i - prev_max[i]
            lenR = next_max[i] - i
            
            # We need x + y + 1 <= k => x + y <= k - 1
            limit = k - 1
            count = count_pairs(lenL, lenR, limit)
            total_sum += count * nums[i]
            
        # Calculate contribution for Minimums
        # For Min: prev is nearest <=, next is nearest <
        prev_min, next_min = get_boundaries(nums, n, is_min=True)
        for i in range(n):
            lenL = i - prev_min[i]
            lenR = next_min[i] - i
            
            limit = k - 1
            count = count_pairs(lenL, lenR, limit)
            total_sum += count * nums[i]
            
        return total_sum