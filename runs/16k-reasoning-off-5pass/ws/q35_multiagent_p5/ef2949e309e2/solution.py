class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Helper for combinations nCr % MOD
        def nCr_mod(n, r):
            if r < 0 or r > n:
                return 0
            if r == 0 or r == n:
                return 1
            if r > n // 2:
                r = n - r
            
            # Since n <= 1000, we can compute directly
            res = 1
            for i in range(r):
                res = res * (n - i) % MOD
                res = res * pow(i + 1, MOD - 2, MOD) % MOD
            return res

        # Precompute global frequencies to help with initial right_freq
        from collections import Counter
        global_freq = Counter(nums)
        
        # left_freq starts empty, right_freq starts as global_freq
        left_freq = Counter()
        right_freq = Counter(global_freq)
        
        ans = 0
        
        for i in range(n):
            m = nums[i]
            
            # Update frequencies: remove current element from right_freq
            # It was included in global_freq, so it's in right_freq initially.
            # But for index i, it is the middle, so it should not be in left or right.
            # So we decrement right_freq[m] here.
            right_freq[m] -= 1
            
            # Current left count and right count (number of elements)
            L = i  # number of elements to the left
            R = n - 1 - i  # number of elements to the right
            
            # Frequencies of m in left and right
            l_m = left_freq[m]
            r_m = right_freq[m]
            
            # Case 1: m appears 3 times in subsequence (pick 2 m's from L+R)
            # Subcase 1a: 2 m's from left, 2 non-m from right
            # Ways to choose 2 non-m from right: C(R - r_m, 2)
            ways_2m_left = nCr_mod(l_m, 2)
            ways_2nonm_right = nCr_mod(R - r_m, 2)
            case1a = ways_2m_left * ways_2nonm_right % MOD
            
            # Subcase 1b: 2 m's from right, 2 non-m from left
            # Ways to choose 2 non-m from left: C(L - l_m, 2)
            ways_2m_right = nCr_mod(r_m, 2)
            ways_2nonm_left = nCr_mod(L - l_m, 2)
            case1b = ways_2m_right * ways_2nonm_left % MOD
            
            # Subcase 1c: 1 m from left, 1 m from right, 1 non-m from left, 1 non-m from right
            # Ways to choose 1 non-m from left: (L - l_m)
            # Ways to choose 1 non-m from right: (R - r_m)
            case1c = l_m * r_m % MOD * (L - l_m) % MOD * (R - r_m) % MOD
            
            case1 = (case1a + case1b + case1c) % MOD
            
            # Case 2: m appears 2 times in subsequence (pick 1 m from L+R, and 2 distinct non-m)
            # Subcase 2a: 1 m from left, 2 distinct non-m from right
            # Ways to choose 2 distinct non-m from right:
            # Total pairs from right non-m: C(R - r_m, 2)
            # Minus pairs that are same value: sum_{x != m} C(right_freq[x], 2)
            # Note: sum_{x != m} C(right_freq[x], 2) = C(R, 2) - C(r_m, 2)
            # Because total pairs from right is C(R, 2), and pairs of m is C(r_m, 2).
            # So distinct non-m pairs = C(R - r_m, 2) is not directly subtractable that way.
            # Actually, the number of ways to pick 2 distinct elements from right that are not m:
            # = (Total ways to pick 2 from right) - (ways to pick 2 m's) - (ways to pick 1 m and 1 non-m? No)
            # We want 2 non-m elements that are distinct.
            # Let S be the multiset of non-m elements in right.
            # Number of pairs from S = C(|S|, 2) - sum_{x in S} C(count(x), 2)
            # |S| = R - r_m
            # sum_{x in S} C(count(x), 2) = sum_{x != m} C(right_freq[x], 2)
            # And we know: C(R, 2) = C(r_m, 2) + r_m * (R - r_m) + sum_{x != m} C(right_freq[x], 2)
            # So sum_{x != m} C(right_freq[x], 2) = C(R, 2) - C(r_m, 2) - r_m * (R - r_m)
            # Therefore, distinct non-m pairs from right = C(R - r_m, 2) - [C(R, 2) - C(r_m, 2) - r_m * (R - r_m)]
            # This is getting complicated. Let's use a simpler identity:
            # The number of ways to choose 2 distinct elements from the right part that are not m is:
            # = (Number of distinct values in right part excluding m) choose 2? No, because we can pick multiple instances.
            # Actually, it's: sum_{x < y, x,y != m} right_freq[x] * right_freq[y]
            # This equals: ( (sum_{x != m} right_freq[x])^2 - sum_{x != m} right_freq[x]^2 ) / 2
            # = ( (R - r_m)^2 - sum_{x != m} right_freq[x]^2 ) / 2
            # But we can also compute it as:
            # Total pairs from right non-m = C(R - r_m, 2)
            # Pairs with same value = sum_{x != m} C(right_freq[x], 2)
            # So distinct pairs = C(R - r_m, 2) - sum_{x != m} C(right_freq[x], 2)
            # And sum_{x != m} C(right_freq[x], 2) = (sum_{x != m} right_freq[x] * (right_freq[x] - 1)) / 2
            # = ( (sum_{x != m} right_freq[x]^2) - (sum_{x != m} right_freq[x]) ) / 2
            # = ( (sum_{x != m} right_freq[x]^2) - (R - r_m) ) / 2
            # So distinct pairs = [ (R - r_m)(R - r_m - 1) - (sum_{x != m} right_freq[x]^2) + (R - r_m) ] / 2
            # = [ (R - r_m)^2 - (sum_{x != m} right_freq[x]^2) ] / 2
            # This requires maintaining sum of squares, which is heavy.
            
            # Simpler approach for Case 2:
            # Instead of deriving a formula, note that:
            # Ways to pick 2 distinct non-m from right = 
            #   (Total ways to pick 2 from right) 
            #   - (ways to pick 2 m's) 
            #   - (ways to pick 1 m and 1 non-m) 
            #   - (ways to pick 2 non-m that are same)
            # But we want only 2 non-m that are distinct.
            # Actually, the set of all pairs from right is partitioned into:
            # 1. Two m's: C(r_m, 2)
            # 2. One m, one non-m: r_m * (R - r_m)
            # 3. Two non-m's: C(R - r_m, 2)
            # Among case 3, some are same value, some are distinct.
            # We want distinct non-m's.
            # Let D_right = number of ways to pick 2 distinct non-m from right.
            # D_right = C(R - r_m, 2) - sum_{x != m} C(right_freq[x], 2)
            # We can precompute or maintain sum_{x} C(right_freq[x], 2).
            # Let total_pairs_right = C(R, 2)
            # total_pairs_right = C(r_m, 2) + r_m*(R-r_m) + sum_{x != m} C(right_freq[x], 2) + (pairs of same non-m? No, sum_{x != m} C(right_freq[x],2) covers all same-value pairs for non-m)
            # Actually, sum_{all x} C(right_freq[x], 2) = C(r_m, 2) + sum_{x != m} C(right_freq[x], 2)
            # So sum_{x != m} C(right_freq[x], 2) = total_same_pairs_right - C(r_m, 2)
            # where total_same_pairs_right = sum_{x} C(right_freq[x], 2)
            # Then D_right = C(R - r_m, 2) - (total_same_pairs_right - C(r_m, 2))
            
            # To avoid maintaining sum of squares, we can use the following trick for Case 2:
            # For each i, we can compute the answer for Case 2 by:
            #   l_m * (ways to pick 2 distinct non-m from right) + r_m * (ways to pick 2 distinct non-m from left)
            # We can precompute for the entire array the "distinct pairs" for left and right? 
            # But left and right change.
            
            # Given N=1000, we can afford O(N) per i if the constant is small.
            # For each i, we can iterate over the right_freq to compute sum_{x != m} C(right_freq[x], 2).
            # But right_freq can have up to N entries. So O(N) per i -> O(N^2) total, which is acceptable for N=1000.
            
            # Let's implement this O(N^2) approach for Case 2.
            
            # Compute sum of C(right_freq[x], 2) for x != m
            sum_c_right = 0
            for x, cnt in right_freq.items():
                if x == m:
                    continue
                if cnt >= 2:
                    sum_c_right = (sum_c_right + cnt * (cnt - 1) // 2) % MOD  # Use integer division, then mod? But we need exact value for subtraction.
                    # Actually, we should compute modulo at the end or use large integers. Python handles large ints.
            # But sum_c_right might be large, but we only need it modulo MOD for the final answer? 
            # No, we are subtracting it from C(R - r_m, 2). We should do all arithmetic modulo MOD.
            # But C(n,2) = n*(n-1)//2. We can compute it modulo MOD.
            # And sum_c_right should be computed modulo MOD as well.
            
            # Recompute sum_c_right modulo MOD
            sum_c_right_mod = 0
            for x, cnt in right_freq.items():
                if x == m:
                    continue
                if cnt >= 2:
                    term = cnt * (cnt - 1) // 2
                    sum_c_right_mod = (sum_c_right_mod + term) % MOD
            
            ways_2distinct_nonm_right = (nCr_mod(R - r_m, 2) - sum_c_right_mod + MOD) % MOD
            case2a = l_m * ways_2distinct_nonm_right % MOD
            
            # Similarly for left
            sum_c_left_mod = 0
            for x, cnt in left_freq.items():
                if x == m:
                    continue
                if cnt >= 2:
                    term = cnt * (cnt - 1) // 2
                    sum_c_left_mod = (sum_c_left_mod + term) % MOD
            
            ways_2distinct_nonm_left = (nCr_mod(L - l_m, 2) - sum_c_left_mod + MOD) % MOD
            case2b = r_m * ways_2distinct_nonm_left % MOD
            
            case2 = (case2a + case2b) % MOD
            
            ans = (ans + case1 + case2) % MOD
            
            # Update left_freq and right_freq for next iteration
            left_freq[m] += 1
            # right_freq[m] was already decremented at the start of the loop
            
        return ans