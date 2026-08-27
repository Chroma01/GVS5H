from typing import List
from collections import Counter

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        if n < 5:
            return 0
        
        # Precompute total frequencies to initialize right_counts
        total_counts = Counter(nums)
        
        left_counts = Counter()
        right_counts = Counter(nums)
        
        total_ans = 0
        
        # Helper for combinations C(n, k)
        def nCk(n, k):
            if k < 0 or k > n:
                return 0
            if k == 0 or k == n:
                return 1
            if k == 1:
                return n
            if k == 2:
                return n * (n - 1) // 2
            return 0
        
        # Helper to calculate sum of C(count, 2) for all values in a counter
        def get_pairs_sum(counter):
            pairs = 0
            for count in counter.values():
                if count >= 2:
                    pairs += count * (count - 1) // 2
            return pairs
        
        # Iterate through each element considering it as the middle element (index 2 of subsequence)
        # We need at least 2 elements to the left and 2 to the right.
        # So i ranges from 2 to n-3 inclusive.
        for i in range(2, n - 2):
            val = nums[i]
            
            # Update counts: move current element from right to left
            right_counts[val] -= 1
            if right_counts[val] == 0:
                del right_counts[val]
            left_counts[val] += 1
            
            L_count = left_counts[val]
            R_count = right_counts[val]
            
            L_total = i
            R_total = n - 1 - i
            
            L_non_v = L_total - L_count
            R_non_v = R_total - R_count
            
            ans_i = 0
            
            # Case 1: Total count of val is 3 (1 from pivot + 2 from others)
            # Subcase 1a: 2 from Left (both val), 0 from Right (both non-val)
            term1a = nCk(L_count, 2) * nCk(R_non_v, 2)
            
            # Subcase 1b: 1 from Left (1 val, 1 non-val), 1 from Right (1 val, 1 non-val)
            term1b = nCk(L_count, 1) * nCk(L_non_v, 1) * nCk(R_count, 1) * nCk(R_non_v, 1)
            
            # Subcase 1c: 0 from Left (2 non-val), 2 from Right (both val)
            term1c = nCk(L_non_v, 2) * nCk(R_count, 2)
            
            ans_i = (ans_i + term1a + term1b + term1c) % MOD
            
            # Case 2: Total count of val is 4 (1 from pivot + 3 from others)
            # Subcase 2a: 2 from Left (both val), 1 from Right (1 val, 1 non-val)
            term2a = nCk(L_count, 2) * nCk(R_count, 1) * nCk(R_non_v, 1)
            
            # Subcase 2b: 1 from Left (1 val, 1 non-val), 2 from Right (both val)
            term2b = nCk(L_count, 1) * nCk(L_non_v, 1) * nCk(R_count, 2)
            
            ans_i = (ans_i + term2a + term2b) % MOD
            
            # Case 3: Total count of val is 5 (1 from pivot + 4 from others)
            # Subcase 3a: 2 from Left (both val), 2 from Right (both val)
            term3a = nCk(L_count, 2) * nCk(R_count, 2)
            
            ans_i = (ans_i + term3a) % MOD
            
            total_ans = (total_ans + ans_i) % MOD
            
        return total_ans