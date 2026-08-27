from typing import List

class Solution:
    def minMaxSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        total_sum = 0
        
        # --- Precompute indices for Max ---
        # prev_greater[i]: index of first element to left >= nums[i]
        prev_greater = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] < nums[i]:
                stack.pop()
            if stack:
                prev_greater[i] = stack[-1]
            stack.append(i)
            
        # next_greater[i]: index of first element to right > nums[i]
        next_greater = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and nums[stack[-1]] <= nums[i]:
                stack.pop()
            if stack:
                next_greater[i] = stack[-1]
            stack.append(i)
            
        # --- Precompute indices for Min ---
        # prev_smaller[i]: index of first element to left <= nums[i]
        prev_smaller = [-1] * n
        stack = []
        for i in range(n):
            while stack and nums[stack[-1]] > nums[i]:
                stack.pop()
            if stack:
                prev_smaller[i] = stack[-1]
            stack.append(i)
            
        # next_smaller[i]: index of first element to right < nums[i]
        next_smaller = [n] * n
        stack = []
        for i in range(n-1, -1, -1):
            while stack and nums[stack[-1]] >= nums[i]:
                stack.pop()
            if stack:
                next_smaller[i] = stack[-1]
            stack.append(i)
            
        # --- Helper to add contribution ---
        def add_contribution(val, L_s, R_s, L_e, R_e, k):
            nonlocal total_sum
            # We need to count pairs (s, e) such that:
            # L_s <= s <= R_s
            # L_e <= e <= R_e
            # e - s + 1 <= k  =>  s >= e - k + 1
            
            # Effective s range lower bound considering e >= L_e
            s_eff_start = max(L_s, L_e - k + 1)
            
            if s_eff_start > R_s:
                return
            
            # The term min(R_e, s + k - 1) switches when s + k - 1 = R_e
            switch_s = R_e - k + 1
            
            # Range A: s in [s_eff_start, min(R_s, switch_s)]
            # Here min(R_e, s + k - 1) = s + k - 1
            range_a_start = s_eff_start
            range_a_end = min(R_s, switch_s)
            
            if range_a_start <= range_a_end:
                count_a = range_a_end - range_a_start + 1
                # Sum of s for s in [range_a_start, range_a_end]
                sum_s_a = (range_a_start + range_a_end) * count_a // 2
                # Contribution: sum (s + k - 1 - L_e + 1) = sum (s + k - L_e)
                term_a = sum_s_a + count_a * (k - L_e)
                total_sum += term_a
            
            # Range B: s in [max(s_eff_start, switch_s + 1), R_s]
            # Here min(R_e, s + k - 1) = R_e
            range_b_start = max(s_eff_start, switch_s + 1)
            range_b_end = R_s
            
            if range_b_start <= range_b_end:
                count_b = range_b_end - range_b_start + 1
                # Contribution: sum (R_e - L_e + 1)
                term_b = count_b * (R_e - L_e + 1)
                total_sum += term_b

        # --- Calculate contribution for Max ---
        for i in range(n):
            L_s = prev_greater[i] + 1
            R_s = i
            L_e = i
            R_e = next_greater[i] - 1
            add_contribution(nums[i], L_s, R_s, L_e, R_e, k)
            
        # --- Calculate contribution for Min ---
        for i in range(n):
            L_s = prev_smaller[i] + 1
            R_s = i
            L_e = i
            R_e = next_smaller[i] - 1
            add_contribution(nums[i], L_s, R_s, L_e, R_e, k)
            
        return total_sum