class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Precompute factorials and inverse factorials for combinations
        max_n = n + 1
        fact = [1] * max_n
        inv_fact = [1] * max_n
        
        for i in range(1, max_n):
            fact[i] = fact[i-1] * i % MOD
        
        inv_fact[max_n-1] = pow(fact[max_n-1], MOD - 2, MOD)
        for i in range(max_n-2, -1, -1):
            inv_fact[i] = inv_fact[i+1] * (i+1) % MOD
        
        def comb(n, k):
            if k < 0 or k > n:
                return 0
            return fact[n] * inv_fact[k] % MOD * inv_fact[n-k] % MOD
        
        total = 0
        
        # Precompute prefix frequency maps
        # left_freq[i] will be a Counter of nums[0..i-1]
        # right_freq[i] will be a Counter of nums[i+1..n-1]
        from collections import Counter
        left_freq = [Counter() for _ in range(n+1)]
        right_freq = [Counter() for _ in range(n+1)]
        
        for i in range(n):
            if i > 0:
                left_freq[i] = left_freq[i-1].copy()
                left_freq[i][nums[i-1]] = left_freq[i-1].get(nums[i-1], 0) + 1
            if i < n:
                right_freq[i] = right_freq[i-1].copy() if i > 0 else Counter()
        
        # Build right_freq properly
        right_freq = [Counter() for _ in range(n+1)]
        for i in range(n-1, -1, -1):
            if i < n-1:
                right_freq[i] = right_freq[i+1].copy()
                right_freq[i][nums[i+1]] = right_freq[i+1].get(nums[i+1], 0) + 1
            else:
                right_freq[i] = Counter()
        
        # For each element as middle
        for i in range(n):
            mid = nums[i]
            # left part: nums[0..i-1], right part: nums[i+1..n-1]
            lf = left_freq[i]
            rf = right_freq[i]
            
            cL = lf.get(mid, 0)
            cR = rf.get(mid, 0)
            
            # We need to choose 2 from left and 2 from right
            # Let's denote:
            # a = number of mid chosen from left (0, 1, or 2)
            # b = number of mid chosen from right (0, 1, or 2)
            # such that a + b = cL + cR is not directly constrained, but we choose exactly 2 from left and 2 from right.
            # Actually, we choose 2 indices from left and 2 from right.
            # The number of mid elements in the subsequence is 2 (the middle) + (number of mid in chosen 2 from left) + (number of mid in chosen 2 from right).
            
            # We'll iterate over possible choices from left and right.
            # From left: choose a mid elements and (2-a) non-mid elements, where a in {0,1,2}
            # From right: choose b mid elements and (2-b) non-mid elements, where b in {0,1,2}
            
            # Total mid count = 2 + a + b
            # For the subsequence to have unique middle mode:
            # Case 1: 2+a+b >= 3: always valid because even if others are same, max other count is at most 2 (since only 3 other positions) and 2+a+b >= 3 > 2.
            # Case 2: 2+a+b == 2: then a+b==0, so a=0,b=0. Then the other 3 elements must be distinct.
            
            # So:
            # If a+b >= 1, then total mid count >= 3, which is always valid.
            # If a+b == 0, then we need the 3 non-mid elements to be distinct.
            
            # Count valid (a,b) pairs:
            # a can be 0,1,2; b can be 0,1,2.
            # But a <= cL, b <= cR.
            
            # For a+b >= 1:
            #   ways = sum over a in [0,1,2], b in [0,1,2] with a+b>=1, a<=cL, b<=cR of:
            #     comb(cL, a) * comb(i - cL, 2-a) * comb(cR, b) * comb(n-1-i - cR, 2-b)
            
            # For a+b == 0: (a=0, b=0)
            #   ways = comb(cL, 0)*comb(i-cL, 2) * comb(cR, 0)*comb(n-1-i-cR, 2) 
            #          but only if the 3 non-mid elements are distinct.
            #   The 3 non-mid elements: 2 from left (non-mid) and 2 from right (non-mid) -> actually 2 from left non-mid and 2 from right non-mid? No: when a=0,b=0, we choose 2 non-mid from left and 2 non-mid from right? But we only choose 2 from left and 2 from right total. So 2 non-mid from left and 2 non-mid from right? That's 4 non-mid elements? No: the subsequence has 5 elements: 2 (middle) + 2 (from left) + 2 (from right) = 6? That's wrong.
            
            # Correction: The subsequence is formed by:
            #   - The middle element at index i.
            #   - 2 elements chosen from indices < i (left part).
            #   - 2 elements chosen from indices > i (right part).
            # So total 5 elements.
            # When a=0 (no mid from left) and b=0 (no mid from right), the subsequence has:
            #   - 2 copies of mid (the middle element itself? No: the middle element is one copy. Actually, the middle element is fixed as nums[i]. Then we choose 2 from left and 2 from right. So the subsequence is: [l1, l2, mid, r1, r2].
            #   - The count of mid in the subsequence is 1 (only the middle) + a + b. But a is the number of mid chosen from left, b from right. So total mid count = 1 + a + b.
            # I made an error above: the middle element is one occurrence. Then we add a from left and b from right. So total = 1 + a + b.
            
            # Recalculate:
            # Total mid count = 1 + a + b.
            # For unique mode:
            #   If 1+a+b >= 3: always valid (since max other count is at most 2, and 3>2).
            #   If 1+a+b == 2: i.e., a+b==1. Then the other 3 elements must not include any element with count >=2. Actually, the other 3 elements: if a=1,b=0: then from left we chose 1 mid and 1 non-mid, from right 2 non-mid. The non-mid elements: 1 from left, 2 from right. For mid to be unique mode (count 2), the other elements must all have count 1. So the 3 non-mid elements must be distinct.
            #   If 1+a+b == 1: i.e., a+b==0. Then mid count is 1. The other 4 elements: for mid to be unique mode, all others must have count <1, impossible. So this case is invalid.
            
            # So valid cases:
            # Case 1: a+b >= 2 (then mid count >=3, always valid)
            # Case 2: a+b == 1 (then mid count=2, valid only if the 3 non-mid elements are distinct)
            
            # Now, for a+b==1:
            #   Subcase 2a: a=1, b=0.
            #     Choose 1 mid from left: comb(cL, 1)
            #     Choose 1 non-mid from left: comb(i - cL, 1)
            #     Choose 0 mid from right: comb(cR, 0)=1
            #     Choose 2 non-mid from right: comb(n-1-i - cR, 2)
            #     But we need the 3 non-mid elements (1 from left, 2 from right) to be distinct.
            #   Subcase 2b: a=0, b=1.
            #     Choose 0 mid from left: 1
            #     Choose 2 non-mid from left: comb(i - cL, 2)
            #     Choose 1 mid from right: comb(cR, 1)
            #     Choose 1 non-mid from right: comb(n-1-i - cR, 1)
            #     And the 3 non-mid elements (2 from left, 1 from right) must be distinct.
            
            # To handle the distinctness condition efficiently, we can:
            # For subcase 2a: 
            #   total_ways = comb(cL,1)*comb(i-cL,1)*comb(cR,0)*comb(n-1-i-cR,2)
            #   minus the ways where the 3 non-mid elements are not distinct.
            #   The non-mid elements are: one from left non-mid set, two from right non-mid set.
            #   They are not distinct if:
            #     - The left non-mid element equals one of the two right non-mid elements.
            #   We can compute:
            #     For each value v in the right non-mid set (i.e., values in rf excluding mid), let cntR_v = rf[v] (if v==mid, skip).
            #     The number of ways to choose 2 from right non-mid that include v: 
            #        = comb(cntR_v, 2) * (number of ways to choose 1 from left non-mid that is v) 
            #          + cntR_v * (number of ways to choose 1 from left non-mid that is v) * (cntR_v - 1)  [if we pick one v and one non-v]
            #     Actually, simpler: 
            #       Total ways without distinctness: T = comb(i-cL,1) * comb(n-1-i-cR,2)
            #       Invalid ways: 
            #         For each value v (v != mid) that appears in both left non-mid and right non-mid:
            #           Let L_v = count of v in left non-mid (i.e., lf[v] if v!=mid, else 0)
            #           Let R_v = count of v in right non-mid (i.e., rf[v] if v!=mid, else 0)
            #           The number of invalid selections where the left non-mid element is v and at least one of the right non-mid elements is v:
            #             = L_v * [ comb(R_v, 2) + R_v * ( (n-1-i-cR) - R_v ) ]
            #           But note: if the two right non-mid are both v, then the left non-mid is v -> all three v, not distinct.
            #           If one right non-mid is v and the other is not, and left non-mid is v -> two v's, not distinct.
            #           So invalid for a given v: L_v * [ comb(R_v,2) + R_v * ( (n-1-i-cR) - R_v ) ]
            #         However, if three v's are chosen, it's counted once. And if two v's and one other, it's also counted once for that v. But if there are two different values that cause collision? Actually, with only 3 elements, if they are not distinct, at least two are equal. And since we have only one from left and two from right, the collision must involve the left element and one of the right elements, or the two right elements being equal.
            #         Actually, the condition "not distinct" means at least two of the three are equal.
            #         We can use inclusion-exclusion, but it's simpler to iterate over all possible values that appear in the non-mid parts and subtract the bad cases.
            #
            # Given the constraints (n<=1000), we can afford to iterate over distinct values in the non-mid parts for each candidate.
            
            # Instead of complex inclusion-exclusion, we can do:
            # For subcase 2a (a=1,b=0):
            #   Let left_non_mid = all elements in left part except mid. We have counts in lf (excluding mid).
            #   Let right_non_mid = all elements in right part except mid. Counts in rf (excluding mid).
            #   We choose 1 from left_non_mid and 2 from right_non_mid.
            #   Total ways: T = (sum of counts in left_non_mid) choose 1 * (sum of counts in right_non_mid) choose 2? No, we have the counts.
            #   Actually, total ways = (i - cL) * comb(n-1-i - cR, 2)
            #   Now, subtract the cases where the chosen left element equals one of the chosen right elements.
            #   For each value v (v != mid):
            #       ways_bad_v = (lf[v]) * [ comb(rf[v], 2) + rf[v] * ( (n-1-i-cR) - rf[v] ) ]
            #   But note: if the two right elements are both v, and the left is v, then it's bad. And if one right is v and the other is w (w!=v) and left is v, then it's bad.
            #   The above formula counts exactly that.
            #   However, if three v's are chosen, it is counted once. And if two v's and one w, it is counted once for v. There is no double counting because for a given selection, if it has two v's and one w, it is only bad because of v (if we consider the left element being v). Actually, if the left element is v and one right is v, then it's bad. The other right element doesn't matter. And if the two right are v, then regardless of left, if left is v, it's bad. 
            #   Actually, the formula: for a fixed v, the bad selections are those where the left element is v and at least one right element is v.
            #   = lf[v] * [ number of ways to choose 2 from right non-mid that include at least one v ]
            #   = lf[v] * [ comb(rf[v],2) + rf[v]*( (n-1-i-cR) - rf[v] ) ]
            #   This is correct.
            #   And since the events for different v are disjoint (because if a selection has left element v and right elements including v, then v is the only value that can cause the collision for that selection? Actually, if the left element is v and the two right are v and w, then it is counted in v's bad set. It is not counted in w's bad set because the left element is not w. So no double counting.
            #
            # Similarly for subcase 2b (a=0,b=1):
            #   Total ways = comb(i-cL,2) * (n-1-i-cR)
            #   Bad ways: for each v (v!=mid):
            #       = rf[v] * [ comb(lf[v],2) + lf[v] * ( (i-cL) - lf[v] ) ]
            #
            # So algorithm for each i:
            #   cL = lf.get(mid,0), cR = rf.get(mid,0)
            #   left_non_mid_count = i - cL
            #   right_non_mid_count = n-1-i - cR
            #
            #   Case 1: a+b>=2
            #     We iterate a in [0,1,2], b in [0,1,2] with a+b>=2, a<=cL, b<=cR.
            #     For each (a,b):
            #       ways = comb(cL, a) * comb(left_non_mid_count, 2-a) * comb(cR, b) * comb(right_non_mid_count, 2-b)
            #     Sum these.
            #
            #   Case 2: a+b==1
            #     Subcase 2a: a=1, b=0
            #       if cL>=1 and left_non_mid_count>=1 and right_non_mid_count>=2:
            #         total_2a = comb(cL,1)*comb(left_non_mid_count,1)*1*comb(right_non_mid_count,2)
            #         bad_2a = 0
            #         for v in set(lf.keys()) | set(rf.keys()):
            #             if v == mid: continue
            #             lv = lf.get(v,0)
            #             rv = rf.get(v,0)
            #             if lv>0 and rv>0:
            #                 bad_2a += lv * (comb(rv,2) + rv*(right_non_mid_count - rv))
            #         valid_2a = total_2a - bad_2a
            #     Subcase 2b: a=0, b=1
            #       if left_non_mid_count>=2 and cR>=1 and right_non_mid_count>=1:
            #         total_2b = 1*comb(left_non_mid_count,2)*comb(cR,1)*comb(right_non_mid_count,1)
            #         bad_2b = 0
            #         for v in set(lf.keys()) | set(rf.keys()):
            #             if v == mid: continue
            #             lv = lf.get(v,0)
            #             rv = rf.get(v,0)
            #             if lv>0 and rv>0:
            #                 bad_2b += rv * (comb(lv,2) + lv*(left_non_mid_count - lv))
            #         valid_2b = total_2b - bad_2b
            #     Case2 = valid_2a + valid_2b
            #
            #   total += Case1 + Case2
            
            left_non_mid_count = i - cL
            right_non_mid_count = n - 1 - i - cR
            
            case1 = 0
            # a in [0,1,2], b in [0,1,2], a+b>=2
            for a in range(0, 3):
                for b in range(0, 3):
                    if a + b < 2:
                        continue
                    if a > cL or b > cR:
                        continue
                    if 2 - a < 0 or 2 - a > left_non_mid_count:
                        continue
                    if 2 - b < 0 or 2 - b > right_non_mid_count:
                        continue
                    ways = comb(cL, a) * comb(left_non_mid_count, 2 - a) % MOD
                    ways = ways * comb(cR, b) % MOD
                    ways = ways * comb(right_non_mid_count, 2 - b) % MOD
                    case1 = (case1 + ways) % MOD
            
            case2 = 0
            # Subcase 2a: a=1, b=0
            if cL >= 1 and left_non_mid_count >= 1 and right_non_mid_count >= 2:
                total_2a = comb(cL, 1) * comb(left_non_mid_count, 1) % MOD * comb(cR, 0) % MOD * comb(right_non_mid_count, 2) % MOD
                bad_2a = 0
                # Get all distinct non-mid values from left and right
                non_mid_vals = set()
                for v in lf:
                    if v != mid:
                        non_mid_vals.add(v)
                for v in rf:
                    if v != mid:
                        non_mid_vals.add(v)
                for v in non_mid_vals:
                    lv = lf.get(v, 0)
                    rv = rf.get(v, 0)
                    if lv > 0 and rv > 0:
                        # bad_2a += lv * (comb(rv,2) + rv*(right_non_mid_count - rv))
                        term = (comb(rv, 2) + rv * (right_non_mid_count - rv)) % MOD
                        bad_2a = (bad_2a + lv * term) % MOD
                valid_2a = (total_2a - bad_2a) % MOD
                case2 = (case2 + valid_2a) % MOD
            
            # Subcase 2b: a=0, b=1
            if left_non_mid_count >= 2 and cR >= 1 and right_non_mid_count >= 1:
                total_2b = comb(cL, 0) * comb(left_non_mid_count, 2) % MOD * comb(cR, 1) % MOD * comb(right_non_mid_count, 1) % MOD
                bad_2b = 0
                non_mid_vals = set()
                for v in lf:
                    if v != mid:
                        non_mid_vals.add(v)
                for v in rf:
                    if v != mid:
                        non_mid_vals.add(v)
                for v in non_mid_vals:
                    lv = lf.get(v, 0)
                    rv = rf.get(v, 0)
                    if lv > 0 and rv > 0:
                        term = (comb(lv, 2) + lv * (left_non_mid_count - lv)) % MOD
                        bad_2b = (bad_2b + rv * term) % MOD
                valid_2b = (total_2b - bad_2b) % MOD
                case2 = (case2 + valid_2b) % MOD
            
            total = (total + case1 + case2) % MOD
        
        return total