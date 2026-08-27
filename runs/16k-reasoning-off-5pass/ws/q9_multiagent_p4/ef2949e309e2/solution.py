from typing import List

class Solution:
    def subsequencesWithMiddleMode(self, nums: List[int]) -> int:
        MOD = 10**9 + 7
        n = len(nums)
        
        # Coordinate compression for values
        unique_nums = sorted(list(set(nums)))
        val_map = {v: i for i, v in enumerate(unique_nums)}
        m = len(unique_nums)
        
        # Prefix counts: prefix_counts[i][v] = count of value v in nums[0...i-1]
        # We only need counts for the current x_idx, but to compute "distinct pairs" 
        # efficiently for K=2, we need counts of all values.
        # Given N <= 1000, O(N^2) space for prefix counts is acceptable (1000*1000 ints).
        prefix_counts = [[0] * m for _ in range(n + 1)]
        for i in range(n):
            for j in range(m):
                prefix_counts[i+1][j] = prefix_counts[i][j]
            prefix_counts[i+1][val_map[nums[i]]] += 1
            
        def nCr(n, r):
            if r < 0 or r > n:
                return 0
            if r == 0 or r == n:
                return 1
            if r > n // 2:
                r = n - r
            
            res = 1
            for i in range(r):
                res = res * (n - i) // (i + 1)
            return res
        
        ans = 0
        
        # Iterate over each distinct number x
        for x_idx in range(m):
            x = unique_nums[x_idx]
            
            # Get indices where x appears
            indices = [i for i, val in enumerate(nums) if val == x]
            
            for i in indices:
                # i is the middle index
                cntL = prefix_counts[i][x_idx]
                cntR = prefix_counts[n][x_idx] - prefix_counts[i+1][x_idx]
                
                nonL = i - cntL
                nonR = (n - 1 - i) - cntR
                
                # Iterate over possible counts of x chosen from left (kL) and right (kR)
                # kL can be 0, 1, 2. kR can be 0, 1, 2.
                # We need kL + kR >= 1 to have at least 2 x's total (middle + 1).
                for kL in range(min(3, cntL + 1)):
                    for kR in range(min(3, cntR + 1)):
                        if kL + kR < 1:
                            continue
                        
                        K = kL + kR + 1
                        remL = 2 - kL
                        remR = 2 - kR
                        
                        if remL > nonL or remR > nonR:
                            continue
                        
                        ways_x = (nCr(cntL, kL) * nCr(cntR, kR)) % MOD
                        
                        if K >= 3:
                            # Any combination of non-x is valid because max freq of any other element is <= 2 < K
                            ways_non = (nCr(nonL, remL) * nCr(nonR, remR)) % MOD
                            term = (ways_x * ways_non) % MOD
                        else:
                            # K == 2. We need the chosen non-x elements to be pairwise distinct.
                            # This means no two chosen non-x elements have the same value.
                            term = 0
                            if remL == 1 and remR == 2:
                                # Choose 1 from left, 2 distinct from right, all distinct from each other.
                                # Let the value chosen from left be v.
                                # We need to choose 2 distinct values from right, neither equal to v.
                                # Total ways to choose 2 distinct values from right = P_total
                                # Valid ways for a specific v = P_total - (pairs in right containing v)
                                # Pairs in right containing v = count(v in right) * (nonR - count(v in right))
                                
                                # Precompute P_total for this i
                                # P_total = sum_{u != w} count(u)*count(w) / 2
                                # = ( (sum count)^2 - sum count^2 ) / 2
                                # sum count = nonR
                                sum_sq_R = 0
                                for u in range(m):
                                    c = prefix_counts[n][u] - prefix_counts[i+1][u]
                                    sum_sq_R += c * c
                                P_total = (nonR * nonR - sum_sq_R) // 2
                                
                                term_val = 0
                                for v in range(m):
                                    if v == x_idx: continue
                                    cL_v = prefix_counts[i][v]
                                    if cL_v == 0: continue
                                    cR_v = prefix_counts[n][v] - prefix_counts[i+1][v]
                                    # Pairs involving v in right: cR_v * (nonR - cR_v)
                                    invalid_pairs = cR_v * (nonR - cR_v)
                                    valid_for_v = P_total - invalid_pairs
                                    term_val = (term_val + cL_v * valid_for_v) % MOD
                                term = (ways_x * term_val) % MOD
                                
                            elif remL == 2 and remR == 1:
                                # Symmetric
                                sum_sq_L = 0
                                for u in range(m):
                                    c = prefix_counts[i][u]
                                    sum_sq_L += c * c
                                P_total = (nonL * nonL - sum_sq_L) // 2
                                
                                term_val = 0
                                for v in range(m):
                                    if v == x_idx: continue
                                    cR_v = prefix_counts[n][v] - prefix_counts[i+1][v]
                                    if cR_v == 0: continue
                                    cL_v = prefix_counts[i][v]
                                    invalid_pairs = cL_v * (nonL - cL_v)
                                    valid_for_v = P_total - invalid_pairs
                                    term_val = (term_val + cR_v * valid_for_v) % MOD
                                term = (ways_x * term_val) % MOD
                            
                            ans = (ans + term) % MOD

        return ans