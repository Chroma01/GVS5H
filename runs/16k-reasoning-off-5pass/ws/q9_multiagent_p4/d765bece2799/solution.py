from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def calculate_sum(arr: List[int], k: int, is_min: bool) -> int:
            n = len(arr)
            # Determine boundaries for each element where it is the min/max
            # For min: prev is strictly smaller, next is smaller or equal
            # For max: prev is strictly larger, next is larger or equal
            # This ensures each subarray's min/max is counted exactly once.
            
            if is_min:
                # Find previous strictly smaller
                prev = [-1] * n
                stack = []
                for i in range(n):
                    while stack and arr[stack[-1]] >= arr[i]:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)
                
                # Find next smaller or equal
                next_idx = [n] * n
                stack = []
                for i in range(n-1, -1, -1):
                    while stack and arr[stack[-1]] > arr[i]:
                        stack.pop()
                    if stack:
                        next_idx[i] = stack[-1]
                    stack.append(i)
            else:
                # Find previous strictly larger
                prev = [-1] * n
                stack = []
                for i in range(n):
                    while stack and arr[stack[-1]] <= arr[i]:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)
                
                # Find next larger or equal
                next_idx = [n] * n
                stack = []
                for i in range(n-1, -1, -1):
                    while stack and arr[stack[-1]] < arr[i]:
                        stack.pop()
                    if stack:
                        next_idx[i] = stack[-1]
                    stack.append(i)
            
            total = 0
            for i in range(n):
                l = prev[i] + 1
                r = next_idx[i] - 1
                
                # Valid start indices: [l, i] -> length from left: a = i - start
                # Valid end indices: [i, r] -> length from right: b = end - i
                # Constraint: (end - start + 1) <= k  =>  a + b <= k - 1
                # a ranges from 0 to max_a = i - l
                # b ranges from 0 to max_b = r - i
                
                max_a = i - l
                max_b = r - i
                
                # We need to count pairs (a, b) such that:
                # 0 <= a <= max_a
                # 0 <= b <= max_b
                # a + b <= k - 1
                
                limit_sum = k - 1
                count = 0
                
                # If the total possible range (max_a + max_b) is less than limit_sum,
                # then all pairs are valid.
                if max_a + max_b < limit_sum:
                    count = (max_a + 1) * (max_b + 1)
                else:
                    # We need to subtract pairs where a + b > limit_sum
                    # Or calculate directly: sum over valid a of valid b count.
                    # For a fixed a, b can be from 0 to min(max_b, limit_sum - a).
                    # If limit_sum - a < 0, then no b is valid.
                    
                    # a must be <= limit_sum (otherwise limit_sum - a < 0)
                    # So a ranges from 0 to min(max_a, limit_sum)
                    
                    upper_a = min(max_a, limit_sum)
                    
                    # Split point where limit_sum - a >= max_b
                    # => a <= limit_sum - max_b
                    split_a = limit_sum - max_b
                    
                    # Range 1: 0 <= a <= min(upper_a, split_a)
                    # Here, limit_sum - a >= max_b, so b can go up to max_b.
                    # Count for each a is (max_b + 1).
                    r1_end = min(upper_a, split_a)
                    if r1_end >= 0:
                        count += (r1_end + 1) * (max_b + 1)
                    
                    # Range 2: max(0, split_a + 1) <= a <= upper_a
                    # Here, limit_sum - a < max_b, so b can go up to limit_sum - a.
                    # Count for each a is (limit_sum - a + 1).
                    start_a = max(0, split_a + 1)
                    if start_a <= upper_a:
                        # Sum of (limit_sum - a + 1) for a from start_a to upper_a
                        # Let term = limit_sum + 1 - a
                        # Sum = (limit_sum + 1 - start_a) + ... + (limit_sum + 1 - upper_a)
                        # This is an arithmetic progression.
                        num_terms = upper_a - start_a + 1
                        first_term = limit_sum + 1 - start_a
                        last_term = limit_sum + 1 - upper_a
                        count += num_terms * (first_term + last_term) // 2
                
                total += count * arr[i]
            
            return total

        return calculate_sum(nums, k, is_min=True) + calculate_sum(nums, k, is_min=False)