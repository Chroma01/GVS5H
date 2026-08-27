class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        m = len(conflictingPairs)
        
        # Group pairs by their max value (right endpoint)
        # pairs_by_r[r] will store list of (min_val, pair_index)
        pairs_by_r = [[] for _ in range(n + 1)]
        
        for idx, (a, b) in enumerate(conflictingPairs):
            l_val = min(a, b)
            r_val = max(a, b)
            pairs_by_r[r_val].append((l_val, idx))
            
        # Precompute base_L, base_idx, fallback_L for each r from 1 to n
        # We sweep r from 1 to n, maintaining the best and second best min_val seen so far
        base_L = [0] * (n + 1)
        base_idx = [-1] * (n + 1)
        fallback_L = [0] * (n + 1)
        
        # best1: (min_val, pair_index), best2: (min_val, pair_index)
        best1 = (-1, -1)
        best2 = (-1, -1)
        
        for r in range(1, n + 1):
            # Add all pairs ending at r
            for l_val, idx in pairs_by_r[r]:
                # Update best1 and best2
                if l_val > best1[0]:
                    best2 = best1
                    best1 = (l_val, idx)
                elif l_val > best2[0]:
                    best2 = (l_val, idx)
            
            base_L[r] = best1[0] if best1[0] != -1 else 0
            base_idx[r] = best1[1]
            fallback_L[r] = best2[0] if best2[0] != -1 else 0
            
        # Calculate total_base: sum_{r=1}^{n} (r - base_L[r])
        total_base = 0
        for r in range(1, n + 1):
            total_base += (r - base_L[r])
            
        # Calculate delta for each pair removal
        # delta[i] = sum_{r where base_idx[r] == i} (base_L[r] - fallback_L[r])
        delta = [0] * m
        for r in range(1, n + 1):
            if base_idx[r] != -1:
                diff = base_L[r] - fallback_L[r]
                delta[base_idx[r]] += diff
                
        # Find maximum valid subarrays after removing exactly one pair
        max_valid = 0
        for i in range(m):
            current_valid = total_base + delta[i]
            if current_valid > max_valid:
                max_valid = current_valid
                
        return max_valid