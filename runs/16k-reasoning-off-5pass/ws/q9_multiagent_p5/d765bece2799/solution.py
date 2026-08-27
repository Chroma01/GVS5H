from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        
        def get_contribution(arr: List[int]) -> int:
            # Calculate sum of max/min for all subarrays with length <= k
            # We use a monotonic stack to find the range where each element is the max/min
            
            # prev[i]: index of the first element to the left strictly greater than arr[i]
            # next[i]: index of the first element to the right greater or equal to arr[i]
            prev = [-1] * n
            next = [n] * n
            
            stack = []
            for i in range(n):
                while stack and arr[stack[-1]] <= arr[i]:
                    stack.pop()
                if stack:
                    prev[i] = stack[-1]
                stack.append(i)
            
            stack = []
            for i in range(n - 1, -1, -1):
                while stack and arr[stack[-1]] < arr[i]:
                    stack.pop()
                if stack:
                    next[i] = stack[-1]
                stack.append(i)
            
            total = 0
            for i in range(n):
                left_bound = prev[i] + 1
                right_bound = next[i] - 1
                
                A = i - left_bound
                B = right_bound - i
                
                K_val = k - 1
                count_le_K = 0
                
                # We need to count pairs (x, y) such that 0 <= x <= A, 0 <= y <= B, and x + y <= K_val
                # x represents distance from start to i (i - L)
                # y represents distance from i to end (R - i)
                
                # Split the range of x into two parts based on the constraint x + y <= K_val
                
                # Part 1: x such that x + B <= K_val  =>  x <= K_val - B
                # In this region, for any x, y can range from 0 to B (since x + y <= x + B <= K_val)
                limit_x = K_val - B
                
                r1_end = min(A, limit_x)
                if r1_end >= 0:
                    # Number of x values is (r1_end - 0 + 1)
                    # For each such x, there are (B + 1) valid y values
                    count_le_K += (r1_end + 1) * (B + 1)
                
                # Part 2: x such that x > K_val - B AND x <= K_val (since y >= 0 implies x <= K_val)
                # Also x <= A
                r2_start = max(0, limit_x + 1)
                r2_end = min(A, K_val)
                
                if r2_start <= r2_end:
                    num_terms = r2_end - r2_start + 1
                    # For these x, y can range from 0 to K_val - x
                    # Sum of (K_val - x + 1) for x in [r2_start, r2_end]
                    # = num_terms * (K_val + 1) - Sum(x)
                    sum_x = (r2_start + r2_end) * num_terms // 2
                    count_le_K += num_terms * (K_val + 1) - sum_x
                
                valid_pairs = count_le_K
                total += valid_pairs * arr[i]
                
            return total

        sum_max = get_contribution(nums)
        sum_min = get_contribution([-x for x in nums])
        
        return sum_max + sum_min