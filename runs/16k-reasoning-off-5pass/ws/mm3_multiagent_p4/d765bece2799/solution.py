from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Compute prev_less_strict[i] and next_less_or_equal[i] for minimum
        prev_less = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            prev_less[i] = stack[-1] if stack else -1
            stack.append(i)
        
        next_less_eq = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            next_less_eq[i] = stack[-1] if stack else n
            stack.append(i)
        
        # Compute prev_greater_strict[i] and next_greater_or_equal[i] for maximum
        prev_greater = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            prev_greater[i] = stack[-1] if stack else -1
            stack.append(i)
        
        next_greater_eq = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            next_greater_eq[i] = stack[-1] if stack else n
            stack.append(i)
        
        # Helper to compute count of subarrays of length <= k where nums[i] is the min/max
        # left = i - prev[i], right = next[i] - i
        # L = i - left + 1 (min start), R = i + right - 1 (max end)
        # s_cutoff = R - k + 1
        def get_count(i, left, right, k):
            L = i - left + 1
            R = i + right - 1
            s_cutoff = R - k + 1
            if s_cutoff < L:
                # All starts: end capped by R
                return left * right
            elif s_cutoff >= i:
                # All starts: end capped by s + k - 1
                cnt = i - L + 1
                sum_s = (L + i) * cnt // 2
                return sum_s + cnt * (k - i)
            else:
                # L <= s_cutoff < i
                # Part 1: s in [L, s_cutoff], f(s) = s + k - i
                cnt1 = s_cutoff - L + 1
                sum_s1 = (L + s_cutoff) * cnt1 // 2
                part1 = sum_s1 + cnt1 * (k - i)
                # Part 2: s in [s_cutoff+1, i], f(s) = right
                cnt2 = i - s_cutoff
                part2 = cnt2 * right
                return part1 + part2
        
        total = 0
        for i in range(n):
            left_min = i - prev_less[i]
            right_min = next_less_eq[i] - i
            count_min = get_count(i, left_min, right_min, k)
            total += nums[i] * count_min
            
            left_max = i - prev_greater[i]
            right_max = next_greater_eq[i] - i
            count_max = get_count(i, left_max, right_max, k)
            total += nums[i] * count_max
        
        return total