from collections import Counter
from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n < 5:
            return 0
        
        # Initialize left_freq as empty, right_freq as frequency of nums[2:]
        left_freq = Counter()
        right_freq = Counter(nums[2:])
        
        ans = 0
        
        # Iterate i from 1 to n-2 (0-indexed)
        for i in range(1, n - 1):
            m = nums[i]
            
            l_m = left_freq.get(m, 0)
            r_m = right_freq.get(m, 0)
            
            left_total = i  # number of elements in nums[0:i]
            right_total = n - 1 - i  # number of elements in nums[i+1:n]
            
            left_non_m_total = left_total - l_m
            right_non_m_total = right_total - r_m
            
            # For k=3: m appears 3 times in subsequence
            # Case 1: 2 m's from left, 0 from right
            # Choose 2 m's from left: C(l_m, 2)
            # Choose 2 non-m from right: C(right_non_m_total, 2)
            if l_m >= 2 and right_non_m_total >= 2:
                case1 = (l_m * (l_m - 1) // 2) * (right_non_m_total * (right_non_m_total - 1) // 2)
                ans = (ans + case1) % MOD
            
            # Case 2: 1 m from left, 1 m from right
            # Choose 1 m from left: l_m
            # Choose 1 non-m from left: left_non_m_total
            # Choose 1 m from right: r_m
            # Choose 1 non-m from right: right_non_m_total
            if l_m >= 1 and r_m >= 1 and left_non_m_total >= 1 and right_non_m_total >= 1:
                case2 = l_m * left_non_m_total * r_m * right_non_m_total
                ans = (ans + case2) % MOD
            
            # Case 3: 0 m's from left, 2 from right
            # Choose 2 m's from right: C(r_m, 2)
            # Choose 2 non-m from left: C(left_non_m_total, 2)
            if r_m >= 2 and left_non_m_total >= 2:
                case3 = (r_m * (r_m - 1) // 2) * (left_non_m_total * (left_non_m_total - 1) // 2)
                ans = (ans + case3) % MOD
            
            # For k=2: m appears 2 times in subsequence
            # Case 1: 1 m from left, 0 from right
            # Choose 1 m from left: l_m
            # Choose 1 non-m from left: left_non_m_total
            # Choose 2 non-m from right such that they are distinct from each other and from the left non-m
            # ways1 = sum_{v in left non-m} freq_L[v] * C(right_non_m_total - freq_R.get(v,0), 2)
            ways1 = 0
            for v, count in left_freq.items():
                if v == m:
                    continue
                r_v = right_freq.get(v, 0)
                rem = right_non_m_total - r_v
                if rem >= 2:
                    ways1 += count * (rem * (rem - 1) // 2)
            
            # Case 2: 0 m's from left, 1 from right
            # ways2 = sum_{v in right non-m} freq_R[v] * C(left_non_m_total - freq_L.get(v,0), 2)
            ways2 = 0
            for v, count in right_freq.items():
                if v == m:
                    continue
                l_v = left_freq.get(v, 0)
                rem = left_non_m_total - l_v
                if rem >= 2:
                    ways2 += count * (rem * (rem - 1) // 2)
            
            ans = (ans + ways1 + ways2) % MOD
            
            # Update left_freq and right_freq for next iteration
            # Add nums[i] to left_freq
            left_freq[m] = left_freq.get(m, 0) + 1
            # Remove nums[i+1] from right_freq
            if i + 1 < n:
                next_val = nums[i + 1]
                right_freq[next_val] -= 1
                if right_freq[next_val] == 0:
                    del right_freq[next_val]
        
        return ans % MOD