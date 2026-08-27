import math
from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        INF = float('inf')
        
        # Step 1: Precompute min1[i] and min2[i] for i from n down to 1.
        # min1[i] = smallest b among pairs (a, b) with a >= i and a < b
        # min2[i] = second smallest b among pairs (a, b) with a >= i and a < b
        
        min1 = [INF] * (n + 2)
        min2 = [INF] * (n + 2)
        
        # For each position i, we'll store the pairs that start at i
        # Then we sweep from n down to 1, merging the current pair's b values with the accumulated min1/min2 from i+1
        
        # First, collect pairs by their left endpoint
        pairs_by_left = [[] for _ in range(n + 1)]
        for a, b in conflictingPairs:
            if a > b:
                a, b = b, a
            # Only consider pairs with a < b
            if a < b:
                pairs_by_left[a].append(b)
        
        # Initialize min1[n] and min2[n] from pairs starting at n
        # But note: a pair starting at n would have b > n, which is impossible, so skip.
        # Actually, a < b and b <= n, so a can be at most n-1.
        
        # We'll compute min1 and min2 from n down to 1
        # Start from n: no pairs start at n (since a < b <= n implies a <= n-1)
        # So min1[n] = INF, min2[n] = INF
        
        # We'll use a running min1 and min2 from the right
        cur_min1 = INF
        cur_min2 = INF
        
        for i in range(n, 0, -1):
            # Update cur_min1 and cur_min2 with pairs starting at i
            for b in pairs_by_left[i]:
                # Insert b into the current min1, min2
                if b < cur_min1:
                    cur_min2 = cur_min1
                    cur_min1 = b
                elif b < cur_min2:
                    cur_min2 = b
            
            min1[i] = cur_min1
            min2[i] = cur_min2
        
        # Step 2: Compute base_total_bad
        total_subarrays = n * (n + 1) // 2
        base_total_bad = 0
        for i in range(1, n + 1):
            if min1[i] != INF:
                # Number of bad subarrays starting at i
                bad_count = n - min1[i] + 1
                if bad_count > 0:
                    base_total_bad += bad_count
        
        # Step 3: Group indices i by min1[i]
        # For each value v, store a list of (i, reduction_value) where reduction_value = max(0, min2[i] - v)
        from collections import defaultdict
        groups = defaultdict(list)
        
        for i in range(1, n + 1):
            v = min1[i]
            if v != INF:
                reduction = max(0, min2[i] - v)
                groups[v].append((i, reduction))
        
        # Step 4: For each group, sort by i and build prefix sum of reduction values
        group_prefix = {}
        for v, lst in groups.items():
            # lst is list of (i, reduction)
            lst.sort(key=lambda x: x[0])
            indices = [x[0] for x in lst]
            reductions = [x[1] for x in lst]
            prefix = [0] * (len(reductions) + 1)
            for idx in range(len(reductions)):
                prefix[idx + 1] = prefix[idx] + reductions[idx]
            group_prefix[v] = (indices, prefix)
        
        # Step 5: For each conflicting pair to remove, compute the reduction
        max_valid = 0
        
        # We need to consider each unique pair in conflictingPairs? 
        # But note: there might be duplicate pairs? The problem doesn't say they are unique.
        # We should iterate over each pair in conflictingPairs as given.
        
        for a0, b0 in conflictingPairs:
            if a0 > b0:
                a0, b0 = b0, a0
            # Only consider if a0 < b0, otherwise the pair doesn't form a valid conflict interval
            if a0 >= b0:
                # This pair doesn't create any bad subarray, so removing it doesn't change anything
                # But we still need to compute valid subarrays
                new_bad = base_total_bad
                valid = total_subarrays - new_bad
                if valid > max_valid:
                    max_valid = valid
                continue
            
            # Get the reduction for removing (a0, b0)
            reduction = 0
            if b0 in group_prefix:
                indices, prefix = group_prefix[b0]
                # Find all indices i in indices such that i <= a0
                # Use bisect_right to find the count of indices <= a0
                import bisect
                pos = bisect.bisect_right(indices, a0)
                reduction = prefix[pos]
            
            new_bad = base_total_bad - reduction
            valid = total_subarrays - new_bad
            if valid > max_valid:
                max_valid = valid
        
        return max_valid