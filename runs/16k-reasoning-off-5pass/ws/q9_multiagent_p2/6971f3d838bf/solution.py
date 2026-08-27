from typing import List
from collections import defaultdict

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # 1. Calculate the maximum subarray sum of the original array (case: no operation)
        # Using Kadane's algorithm
        max_so_far = nums[0]
        current_max = nums[0]
        for i in range(1, n):
            current_max = max(nums[i], current_max + nums[i])
            max_so_far = max(max_so_far, current_max)
        
        # 2. Precompute prefix sums P[i] = sum(nums[0...i-1])
        P = [0] * (n + 1)
        for i in range(n):
            P[i+1] = P[i] + nums[i]
            
        # 3. Precompute prefix max subarray sums (L_best[i])
        # L_best[i] = max subarray sum in nums[0...i]
        L_best = [0] * n
        current_max = nums[0]
        L_best[0] = nums[0]
        for i in range(1, n):
            current_max = max(nums[i], current_max + nums[i])
            L_best[i] = max(L_best[i-1], current_max)
            
        # 4. Precompute suffix max subarray sums (R_best[i])
        # R_best[i] = max subarray sum in nums[i...n-1]
        R_best = [0] * n
        current_max = nums[n-1]
        R_best[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            current_max = max(nums[i], nums[i] + current_max)
            R_best[i] = max(R_best[i+1], current_max)
            
        # 5. Iterate over each unique number x to simulate its removal
        # We group indices by value to efficiently process segments
        indices_map = defaultdict(list)
        for i, x in enumerate(nums):
            indices_map[x].append(i)
            
        # We also need to track the global maximum found so far
        global_max = max_so_far
        
        # To optimize, we can iterate through the array once and maintain the best
        # subarray sum for each x encountered so far in the current segment.
        # However, a simpler O(N) approach for the "remove x" logic:
        # For a specific x, the array is split into segments by occurrences of x.
        # The max subarray sum after removing x is the max of:
        #   a) Max subarray sum entirely within one segment.
        #   b) Max subarray sum formed by concatenating a suffix of segment j and prefix of segment j+1.
        #
        # We can precompute:
        #   - prefix_max_ending[i]: max subarray sum ending at i (standard Kadane ending at i)
        #   - suffix_max_starting[i]: max subarray sum starting at i (standard Kadane starting at i)
        #
        # Then for each x, we iterate through its occurrences.
        # Let occurrences be idx_1, idx_2, ..., idx_k.
        # Segments are: [0, idx_1-1], [idx_1+1, idx_2-1], ..., [idx_k+1, n-1].
        #
        # For each segment [s, e], the max subarray sum is max(L_best[e], R_best[s])? 
        # No, L_best[e] is max in [0, e], which might include x.
        # We need max subarray sum strictly within [s, e].
        # We can precompute segment_max[s][e] but that's O(N^2).
        #
        # Alternative efficient approach:
        # For each x, we want max_{L, R} (Sum(L, R) - count(x, L, R) * x).
        # This is equivalent to max_{L, R} ( (P[R+1] - P[L]) - x * (C[R+1] - C[L]) )
        # = max_{L, R} ( (P[R+1] - x*C[R+1]) - (P[L] - x*C[L]) )
        # Let val(i, x) = P[i] - x * C_x[i]. We want max_{j} val(j, x) - min_{i <= j} val(i, x).
        #
        # We can compute this for all x simultaneously in one pass.
        # Maintain min_val[x] = min(val(i, x)) for all i seen so far.
        # At each step i (from 0 to n), for each x, val(i, x) = P[i] - x * count[x].
        # But we can't iterate all x at each step.
        #
        # Instead, we iterate through the array and update the state for the current element's value.
        # But we need to query the max difference for ALL x.
        #
        # Let's go back to the segment logic but optimize the segment max calculation.
        # We can precompute "max subarray sum in range [i, j]"? No.
        #
        # Let's use the property that between two occurrences of x, the term x*C is constant.
        # So in a segment between idx_j and idx_{j+1}, val(k, x) = P[k] - j*x.
        # The max difference in this segment is (max(P[k]) - min(P[k])) for k in range.
        #
        # We can precompute prefix max and min of P?
        # Let pre_max[i] = max(P[0]...P[i]) and pre_min[i] = min(P[0]...P[i]).
        # Then for a segment (idx_j, idx_{j+1}), the max difference is pre_max[idx_{j+1}] - pre_min[idx_j]?
        # No, we need the max and min within the specific range (idx_j, idx_{j+1}).
        # This requires Range Max/Min Query (RMQ). We can use a Segment Tree or Sparse Table.
        # Given N=10^5, Sparse Table is O(N log N) build and O(1) query.
        #
        # Steps:
        # 1. Build Sparse Table for P to answer RMQ in O(1).
        # 2. For each unique x, iterate its occurrences.
        #    - Define segments.
        #    - For each segment, query RMQ on P to get max_P and min_P.
        #    - Calculate potential max subarray sum = (max_P - min_P) - (count * x).
        #    - Also consider subarrays entirely before the first occurrence or after the last.
        #
        # This is O(N log N) or O(N) with linear RMQ (if we process offline or use specific structure).
        # Given constraints, O(N log N) is acceptable.
        
        # Build Sparse Table for Range Max/Min on P
        # P has size n+1.
        import math
        
        m = n + 1
        K = m.bit_length()
        
        # st_max[k][i] stores max of P[i...i+2^k-1]
        st_max = [[0] * m for _ in range(K)]
        st_min = [[0] * m for _ in range(K)]
        
        for i in range(m):
            st_max[0][i] = P[i]
            st_min[0][i] = P[i]
            
        for k in range(1, K):
            length = 1 << (k-1)
            for i in range(m - (1 << k) + 1):
                st_max[k][i] = max(st_max[k-1][i], st_max[k-1][i + length])
                st_min[k][i] = min(st_min[k-1][i], st_min[k-1][i + length])
                
        def query_max(L, R):
            if L > R: return -float('inf')
            k = (R - L + 1).bit_length() - 1
            return max(st_max[k][L], st_max[k][R - (1 << k) + 1])
            
        def query_min(L, R):
            if L > R: return float('inf')
            k = (R - L + 1).bit_length() - 1
            return min(st_min[k][L], st_min[k][R - (1 << k) + 1])
            
        # Process each unique x
        for x, occs in indices_map.items():
            # occs contains indices where nums[i] == x, sorted
            # Add boundaries 0 and n to handle segments easily
            # Segments are defined by ranges [occ[j]+1, occ[j+1]-1]
            # We also need to consider the prefix before the first occurrence and suffix after the last.
            
            # Case 1: Subarray entirely before the first occurrence of x
            # Range [0, occs[0]-1]
            if occs[0] > 0:
                # Max subarray sum in [0, occs[0]-1]
                # This is max_{L, R in [0, occs[0]-1]} (P[R+1] - P[L])
                # = max(P[1...occs[0]]) - min(P[0...occs[0]])
                # Note: P indices involved are 0 to occs[0]
                # Range for P indices: L in [0, occs[0]], R+1 in [1, occs[0]] => R in [0, occs[0]-1]
                # Actually, we need max(P[R+1] - P[L]) for 0 <= L <= R < occs[0].
                # This is max(P[1...occs[0]]) - min(P[0...occs[0]])
                max_p = query_max(1, occs[0])
                min_p = query_min(0, occs[0])
                global_max = max(global_max, max_p - min_p)
                
            # Case 2: Subarray entirely after the last occurrence of x
            # Range [occs[-1]+1, n-1]
            if occs[-1] < n - 1:
                # Range for P indices: L in [occs[-1]+1, n], R+1 in [occs[-1]+2, n]
                # Wait, indices in array are occs[-1]+1 to n-1.
                # P indices involved: L from occs[-1]+1 to n, R+1 from occs[-1]+2 to n.
                # Actually, simpler: max subarray in [s, e] is max(P[s...e+1]) - min(P[s...e+1])?
                # No. Max subarray in [s, e] is max_{L, R in [s, e]} (P[R+1] - P[L]).
                # L ranges from s to e, R+1 ranges from s+1 to e+1.
                # So we need max(P[s+1...e+1]) - min(P[s...e+1]).
                s = occs[-1] + 1
                e = n - 1
                if s <= e:
                    max_p = query_max(s+1, e+1)
                    min_p = query_min(s, e+1)
                    global_max = max(global_max, max_p - min_p)
                    
            # Case 3: Subarray spanning across occurrences
            # We iterate through adjacent occurrences idx_j, idx_{j+1}
            # The segment between them is [idx_j+1, idx_{j+1}-1].
            # The subarray can start in [0, idx_j] and end in [idx_{j+1}, n-1]
            # But it must skip all x's.
            # Actually, the formula val(R+1) - val(L) handles this automatically if we consider
            # the entire range [0, n] and subtract the cost of x's.
            # However, we must ensure the subarray is non-empty in the resulting array.
            # The formula max_{j} val(j, x) - min_{i <= j} val(i, x) gives the max sum of non-x elements.
            # We need to ensure that the range [i, j-1] (in terms of P indices) contains at least one non-x element.
            # If the range [i, j-1] consists only of x's, then the sum is 0 (since we subtract x*x_count).
            # But we need a non-empty subarray of non-x elements.
            # If the max sum is 0, we need to check if there's any non-x element.
            # If all non-x elements are negative, the max sum will be the max single element (negative).
            # The formula val(j) - val(i) works even if the sum is negative.
            # The only issue is if the optimal range [i, j-1] contains ONLY x's.
            # In that case, the sum of non-x elements is 0. But we need a non-empty subarray of non-x elements.
            # If the only non-x elements are negative, the max sum is negative.
            # If we pick a range with only x's, the sum is 0. This is invalid if we must pick non-x.
            # So we need to ensure the range [i, j-1] has at least one non-x.
            # This is equivalent to saying the range [i, j-1] is not a subset of the occurrences of x.
            # Since we are iterating through the array, we can just compute the global max difference
            # and then verify if the resulting subarray is valid.
            # Or, simpler: The max subarray sum of non-x elements is exactly what we want.
            # If the max sum is 0, it means either all non-x are negative (and we picked the least negative)
            # OR we picked a range with only x's (sum 0).
            # If we picked a range with only x's, that's invalid.
            # But if all non-x are negative, the max sum will be negative (from the formula).
            # Wait, if all non-x are negative, say [-5, -3], and x=0 (not present).
            # P = [0, -5, -8]. val(i, 0) = P[i].
            # max diff = -5 - 0 = -5. Correct.
            # If x is present, say [0, 0, -5, -3]. x=0.
            # P = [0, 0, 0, -5, -8].
            # val(i, 0) = P[i] - 0*count.
            # i=0: 0. i=1: 0. i=2: 0. i=3: -5. i=4: -8.
            # max diff = 0 - 0 = 0.
            # But valid subarrays are [-5] (-5) and [-3] (-3). Max is -3.
            # The formula gives 0 because it picks range [0, 1] (indices 0 to 0 in P, i.e., empty in array? No).
            # P indices: L=0, R+1=1 => range [0, 0] in array. nums[0]=0 (x). Sum non-x = 0.
            # This is invalid.
            # So we need to ensure the range [L, R] contains at least one non-x.
            # This means we cannot pick a range that is entirely within the occurrences of x.
            # We can handle this by initializing the answer for x to -infinity and updating only if valid.
            # But checking validity for every pair is hard.
            #
            # Alternative: The max subarray sum of non-x elements is simply the max subarray sum of the array
            # where x is replaced by 0, EXCLUDING the case where the subarray consists entirely of 0s.
            # If the max subarray sum of (nums with x->0) is > 0, it's valid.
            # If it is 0, we need to check if there's any non-x element. If yes, max is 0 (if all non-x <= 0).
            # If no non-x element, then we can't form a subarray (but problem says nums remains non-empty).
            # If nums remains non-empty, there is at least one non-x element.
            # So if max sum is 0, and there is at least one non-x element, the answer is 0?
            # No, if all non-x are negative, the max sum is negative.
            # The formula val(j) - val(i) will give 0 if we pick a range of only x's.
            # We need to force the range to include at least one non-x.
            # This is equivalent to: max_{L, R} (Sum(L, R) - count(x, L, R)*x) such that count(non-x, L, R) >= 1.
            #
            # Let's refine the logic:
            # We can compute the max subarray sum of non-x elements by running Kadane's on the modified array.
            # But we can't run Kadane's for each x.
            #
            # Let's go back to the segment idea.
            # The max subarray sum is the max of:
            # 1. Max subarray sum within a single segment (no x's).
            # 2. Max subarray sum formed by concatenating suffix of segment j and prefix of segment j+1.
            #
            # We can precompute:
            #   - prefix_max_ending[i]: max subarray sum ending at i (standard Kadane)
            #   - suffix_max_starting[i]: max subarray sum starting at i
            #
            # Then for each x, iterate occurrences idx_j, idx_{j+1}.
            # Segment j is [idx_j+1, idx_{j+1}-1].
            # Max subarray within segment j:
            #   We can query this using precomputed RMQ on prefix_max_ending?
            #   No, prefix_max_ending[i] is max ending at i. We need max in range [s, e].
            #   This is max_{k in [s, e]} (prefix_max_ending[k]).
            #   We can build a Sparse Table on prefix_max_ending array.
            #   Similarly for suffix_max_starting.
            #
            # Then for each x:
            #   - For each segment [s, e], query max(prefix_max_ending) in [s, e].
            #   - For each adjacent pair of segments (separated by x at idx), 
            #     combine suffix of segment j and prefix of segment j+1.
            #     Suffix of segment j: max_{k in [s_j, e_j]} (suffix_max_starting[k]).
            #     Prefix of segment j+1: max_{k in [s_{j+1}, e_{j+1}]} (prefix_max_ending[k]).
            #     Sum = suffix_val + prefix_val.
            #
            # This covers all cases.
            # Also need to consider the case where the subarray is entirely before the first x or after the last x.
            # These are covered by the first and last segments.
            
            # Implementation details:
            # 1. Compute prefix_max_ending and suffix_max_starting.
            # 2. Build Sparse Tables for RMQ on these two arrays.
            # 3. For each x, iterate segments and query.
            
            # Let's implement this.
            
            # Precompute prefix_max_ending and suffix_max_starting
            # prefix_max_ending[i] = max subarray sum ending at i
            # suffix_max_starting[i] = max subarray sum starting at i
            
            # We already have L_best and R_best, but we need the specific ending/starting values.
            # Let's recompute them.
            
            pass # Will be done below
            
        # Re-implementing the full logic with Sparse Tables for RMQ
        
        # 1. Prefix sums P
        # 2. prefix_max_ending[i]
        # 3. suffix_max_starting[i]
        # 4. Sparse Tables for RMQ on prefix_max_ending and suffix_max_starting
        
        # Recompute prefix_max_ending
        pre_end = [0] * n
        curr = nums[0]
        pre_end[0] = nums[0]
        for i in range(1, n):
            curr = max(nums[i], curr + nums[i])
            pre_end[i] = curr
            
        # Recompute suffix_max_starting
        suf_start = [0] * n
        curr = nums[n-1]
        suf_start[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            curr = max(nums[i], nums[i] + curr)
            suf_start[i] = curr
            
        # Build Sparse Tables for RMQ on pre_end and suf_start
        # st_pre[k][i] = max(pre_end[i ... i+2^k-1])
        # st_suf[k][i] = max(suf_start[i ... i+2^k-1])
        
        K = n.bit_length()
        st_pre = [[0] * n for _ in range(K)]
        st_suf = [[0] * n for _ in range(K)]
        
        for i in range(n):
            st_pre[0][i] = pre_end[i]
            st_suf[0][i] = suf_start[i]
            
        for k in range(1, K):
            length = 1 << (k-1)
            for i in range(n - (1 << k) + 1):
                st_pre[k][i] = max(st_pre[k-1][i], st_pre[k-1][i + length])
                st_suf[k][i] = max(st_suf[k-1][i], st_suf[k-1][i + length])
                
        def query_max(arr_st, L, R):
            if L > R: return -float('inf')
            k = (R - L + 1).bit_length() - 1
            return max(arr_st[k][L], arr_st[k][R - (1 << k) + 1])
            
        # Process each x
        for x, occs in indices_map.items():
            # Case 1: Entirely before first occurrence
            if occs[0] > 0:
                # Max subarray in [0, occs[0]-1]
                # This is max_{k in [0, occs[0]-1]} pre_end[k]
                val = query_max(st_pre, 0, occs[0]-1)
                global_max = max(global_max, val)
                
            # Case 2: Entirely after last occurrence
            if occs[-1] < n - 1:
                # Max subarray in [occs[-1]+1, n-1]
                # This is max_{k in [occs[-1]+1, n-1]} suf_start[k]
                val = query_max(st_suf, occs[-1]+1, n-1)
                global_max = max(global_max, val)
                
            # Case 3: Spanning across occurrences
            # Iterate through adjacent occurrences
            for j in range(len(occs) - 1):
                idx1 = occs[j]
                idx2 = occs[j+1]
                
                # Segment 1: [idx1+1, idx2-1]
                # Segment 2: [idx1+1, idx2-1] (same segment between them)
                # We want to combine suffix of segment 1 and prefix of segment 2?
                # No, the segments are:
                # ... [idx1-1] (end of prev), [idx1] (x), [idx1+1...idx2-1] (segment), [idx2] (x), ...
                # We want to combine suffix of the segment ending at idx1-1? No.
                # We want to combine suffix of the segment BEFORE idx1 and prefix of the segment AFTER idx1?
                # No, we want to combine suffix of the segment ending at idx1-1 and prefix of the segment starting at idx1+1?
                # Wait, the segments are separated by x.
                # Let's denote segments as S_0, S_1, ..., S_m.
                # S_0 = [0, idx1-1]
                # S_1 = [idx1+1, idx2-1]
                # ...
                # We want to combine suffix of S_j and prefix of S_{j+1}.
                # Suffix of S_j: max_{k in S_j} suf_start[k]
                # Prefix of S_{j+1}: max_{k in S_{j+1}} pre_end[k]
                # Sum = suffix_val + prefix_val.
                
                # We need to iterate through all adjacent segments.
                # The segments are defined by the gaps between occurrences.
                # Gap 0: [0, idx1-1]
                # Gap 1: [idx1+1, idx2-1]
                # ...
                # Gap m: [idx_last+1, n-1]
                
                # We can compute suffix_max for each gap and prefix_max for each gap.
                # But we need to do this efficiently.
                # We can precompute prefix_max_gap and suffix_max_gap for each x?
                # No, we can just iterate through the gaps.
                
                # Let's collect all gaps for x.
                gaps = []
                curr_start = 0
                for idx in occs:
                    if curr_start < idx:
                        gaps.append((curr_start, idx-1))
                    curr_start = idx + 1
                if curr_start < n:
                    gaps.append((curr_start, n-1))
                    
                # Now iterate through gaps
                # For each gap, compute max suffix (from right) and max prefix (from left)
                # But we need to combine gap j and gap j+1.
                # We can precompute for each gap:
                #   max_suffix[gap_idx] = max_{k in gap} suf_start[k]
                #   max_prefix[gap_idx] = max_{k in gap} pre_end[k]
                
                # Then for each j, candidate = max_suffix[j] + max_prefix[j+1]
                
                # To do this efficiently:
                # Compute max_suffix for all gaps.
                # Compute max_prefix for all gaps.
                # Then sum adjacent.
                
                # We can do this in one pass over gaps.
                
                # But we need to handle the case where a gap is empty (idx1+1 > idx2-1).
                # If a gap is empty, max_suffix = -inf, max_prefix = -inf.
                
                # Let's implement this.
                
                gap_max_suf = []
                gap_max_pre = []
                
                for s, e in gaps:
                    if s > e:
                        gap_max_suf.append(-float('inf'))
                        gap_max_pre.append(-float('inf'))
                    else:
                        # Max suffix in [s, e]
                        val_suf = query_max(st_suf, s, e)
                        # Max prefix in [s, e]
                        val_pre = query_max(st_pre, s, e)
                        gap_max_suf.append(val_suf)
                        gap_max_pre.append(val_pre)
                        
                # Now combine adjacent gaps
                for j in range(len(gaps) - 1):
                    if gap_max_suf[j] != -float('inf') and gap_max_pre[j+1] != -float('inf'):
                        global_max = max(global_max, gap_max_suf[j] + gap_max_pre[j+1])
                        
        return global_max