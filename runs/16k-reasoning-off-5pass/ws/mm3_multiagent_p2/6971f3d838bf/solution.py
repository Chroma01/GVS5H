import math
from collections import defaultdict
from typing import List

class Solution:
    def maxSubarraySum(self, nums: List[int]) -> int:
        n = len(nums)
        if n == 0:
            return 0
        
        # Prefix sums P[0..n]
        P = [0] * (n + 1)
        for i in range(n):
            P[i+1] = P[i] + nums[i]
        
        # Suffix max subarray sum starting at i
        suf = [0] * n
        suf[n-1] = nums[n-1]
        for i in range(n-2, -1, -1):
            suf[i] = max(nums[i], nums[i] + suf[i+1])
        
        # Original max subarray sum (no operation)
        original_max = max(suf)
        
        # Precompute log table for sparse table queries
        log = [0] * (n + 1)
        for i in range(2, n+1):
            log[i] = log[i//2] + 1
        K = log[n] + 1
        
        # Sparse table for range max on suf
        st_suf = [suf[:]]
        for k in range(1, K):
            prev = st_suf[-1]
            curr_len = n - (1 << k) + 1
            if curr_len <= 0:
                break
            curr = [0] * curr_len
            for i in range(curr_len):
                curr[i] = max(prev[i], prev[i + (1 << (k-1))])
            st_suf.append(curr)
        
        def query_max_suf(L, R):
            """Return max of suf[L..R]"""
            length = R - L + 1
            k = log[length]
            return max(st_suf[k][L], st_suf[k][R - (1 << k) + 1])
        
        # Sparse table for range max on P (for max prefix sum computation)
        st_P_max = [P[:]]
        for k in range(1, K+1):
            prev = st_P_max[-1]
            curr_len = (n+1) - (1 << k) + 1
            if curr_len <= 0:
                break
            curr = [0] * curr_len
            for i in range(curr_len):
                curr[i] = max(prev[i], prev[i + (1 << (k-1))])
            st_P_max.append(curr)
        
        def query_max_P(L, R):
            """Return max of P[L..R]"""
            if L > R:
                return -10**18
            length = R - L + 1
            k = log[length]
            return max(st_P_max[k][L], st_P_max[k][R - (1 << k) + 1])
        
        # Sparse table for range min on P (for max suffix sum computation)
        st_P_min = [P[:]]
        for k in range(1, K+1):
            prev = st_P_min[-1]
            curr_len = (n+1) - (1 << k) + 1
            if curr_len <= 0:
                break
            curr = [0] * curr_len
            for i in range(curr_len):
                curr[i] = min(prev[i], prev[i + (1 << (k-1))])
            st_P_min.append(curr)
        
        def query_min_P(L, R):
            """Return min of P[L..R]"""
            if L > R:
                return 10**18
            length = R - L + 1
            k = log[length]
            return min(st_P_min[k][L], st_P_min[k][R - (1 << k) + 1])
        
        # Group positions by value
        pos_map = defaultdict(list)
        for i, v in enumerate(nums):
            pos_map[v].append(i)
        
        ans = original_max
        
        # Iterate over each distinct value x
        for x, positions in pos_map.items():
            # Build contiguous segments of non-x elements
            segments = []
            prev = 0
            for p in positions:
                if prev <= p - 1:
                    segments.append((prev, p - 1))
                prev = p + 1
            if prev <= n - 1:
                segments.append((prev, n - 1))
            
            # Skip if removing x would make the array empty
            if not segments:
                continue
            
            m = len(segments)
            sums = [0] * m
            max_subs = [0] * m
            max_prefs = [0] * m
            max_sufs = [0] * m
            
            # Precompute segment properties using range queries
            for idx, (L, R) in enumerate(segments):
                sums[idx] = P[R+1] - P[L]
                max_subs[idx] = query_max_suf(L, R)
                # Max prefix sum: max_{i in [L,R]} (P[i+1] - P[L])
                max_prefs[idx] = query_max_P(L+1, R+1) - P[L]
                # Max suffix sum: max_{i in [L,R]} (P[R+1] - P[i])
                max_sufs[idx] = P[R+1] - query_min_P(L, R)
            
            # Prefix sums of segment sums
            pref_sum = [0] * m
            for i in range(m):
                pref_sum[i] = sums[i] + (pref_sum[i-1] if i > 0 else 0)
            
            # Case 1: Best subarray lies entirely within one segment
            best = max(max_subs)
            
            # Case 2: Best subarray spans multiple segments
            if m >= 2:
                # Compute right_best[i] = max_{j > i} (pref_sum[j-1] + max_prefs[j])
                right_best = [-10**18] * (m - 1)
                cur_best = -10**18
                for j in range(m-1, 0, -1):
                    val = pref_sum[j-1] + max_prefs[j]
                    if val > cur_best:
                        cur_best = val
                    right_best[j-1] = cur_best
                
                # For each i, candidate = max_sufs[i] - pref_sum[i] + right_best[i]
                for i in range(m - 1):
                    candidate = max_sufs[i] - pref_sum[i] + right_best[i]
                    if candidate > best:
                        best = candidate
            
            if best > ans:
                ans = best
        
        return ans