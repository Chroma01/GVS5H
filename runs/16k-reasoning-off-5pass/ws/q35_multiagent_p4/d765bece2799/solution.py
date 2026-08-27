class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        def get_contribution(nums, k, mode):
            n = len(nums)
            # prev[i] will store the index of the previous element that breaks the monotonicity
            # next[i] will store the index of the next element that breaks the monotonicity
            prev = [-1] * n
            next_idx = [n] * n
            
            stack = []
            
            if mode == 'max':
                # For max: find previous greater (strict) and next greater or equal
                # Stack stores indices, nums[stack[-1]] is decreasing
                for i in range(n):
                    while stack and nums[stack[-1]] <= nums[i]:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)
                
                stack = []
                for i in range(n - 1, -1, -1):
                    while stack and nums[stack[-1]] < nums[i]:
                        stack.pop()
                    if stack:
                        next_idx[i] = stack[-1]
                    stack.append(i)
            else:
                # For min: find previous smaller (strict) and next smaller or equal
                # Stack stores indices, nums[stack[-1]] is increasing
                for i in range(n):
                    while stack and nums[stack[-1]] >= nums[i]:
                        stack.pop()
                    if stack:
                        prev[i] = stack[-1]
                    stack.append(i)
                
                stack = []
                for i in range(n - 1, -1, -1):
                    while stack and nums[stack[-1]] > nums[i]:
                        stack.pop()
                    if stack:
                        next_idx[i] = stack[-1]
                    stack.append(i)
            
            total = 0
            for i in range(n):
                # Range where nums[i] is the max/min is (prev[i], next_idx[i])
                # Left boundary: l = prev[i] + 1
                # Right boundary: r = next_idx[i] - 1
                l = prev[i] + 1
                r = next_idx[i] - 1
                
                # Subarray start s in [l, i]
                # Subarray end e in [i, r]
                # Constraint: e - s + 1 <= k  =>  e <= s + k - 1
                
                # We need to count pairs (s, e) such that:
                # l <= s <= i
                # i <= e <= r
                # e <= s + k - 1
                
                # For a fixed s, e can range from i to min(r, s + k - 1)
                # Let max_e(s) = min(r, s + k - 1)
                # The number of valid e's for a given s is max(0, max_e(s) - i + 1)
                
                # We split the range of s into two parts:
                # 1. Where s + k - 1 >= r, i.e., s >= r - k + 1. In this case, max_e(s) = r.
                # 2. Where s + k - 1 < r, i.e., s < r - k + 1. In this case, max_e(s) = s + k - 1.
                
                # Let s1 = max(l, r - k + 1)
                # Let s2 = min(i, r - k)  [the largest s such that s < r - k + 1]
                
                # Part 1: s in [s1, i] (if s1 <= i)
                # Count = sum_{s=s1}^{i} (r - i + 1)
                #        = (i - s1 + 1) * (r - i + 1)
                
                # Part 2: s in [l, s2] (if l <= s2)
                # Count = sum_{s=l}^{s2} (s + k - 1 - i + 1)
                #        = sum_{s=l}^{s2} (s + k - i)
                # Let term = s + k - i
                # This is an arithmetic series.
                # First term (s=l): l + k - i
                # Last term (s=s2): s2 + k - i
                # Number of terms: s2 - l + 1
                # Sum = (first + last) * num_terms // 2
                
                count = 0
                
                s1 = max(l, r - k + 1)
                s2 = min(i, r - k)
                
                # Part 1
                if s1 <= i:
                    num_terms = i - s1 + 1
                    count += num_terms * (r - i + 1)
                
                # Part 2
                if l <= s2:
                    num_terms = s2 - l + 1
                    first_term = l + k - i
                    last_term = s2 + k - i
                    count += (first_term + last_term) * num_terms // 2
                
                total += nums[i] * count
                
            return total

        return get_contribution(nums, k, 'max') + get_contribution(nums, k, 'min')