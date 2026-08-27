from typing import List
import bisect

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Pair each interval with its original index
        indexed = [(l, r, w, idx) for idx, (l, r, w) in enumerate(intervals)]
        # Sort by end ascending, then start ascending
        indexed.sort(key=lambda x: (x[1], x[0]))
        
        # Extract sorted arrays for binary search
        ends = [item[1] for item in indexed]
        starts = [item[0] for item in indexed]
        weights = [item[2] for item in indexed]
        orig_indices = [item[3] for item in indexed]
        
        # dp[k][i] = (max_weight, best_indices_tuple) using at most k intervals among first i intervals (0..i-1)
        dp = [[(0, ())] * (n + 1) for _ in range(5)]
        
        # Helper to compare two candidates: returns True if a is better than b
        def is_better(a_weight, a_indices, b_weight, b_indices):
            if a_weight != b_weight:
                return a_weight > b_weight
            return a_indices < b_indices  # Python tuple lexicographic comparison
        
        # Process each interval in sorted order
        for i in range(n):
            l_i = starts[i]
            w_i = weights[i]
            orig_i = orig_indices[i]
            
            # Find the largest index p < i such that ends[p] < l_i
            p = bisect.bisect_left(ends, l_i, 0, i) - 1
            
            # Update dp for k=1..4
            for k in range(1, 5):
                # Option 1: skip interval i (inherit from dp[k][i])
                best_weight, best_indices = dp[k][i]
                
                # Option 2: take interval i
                if p >= 0:
                    prev_weight, prev_indices = dp[k-1][p+1]
                else:
                    prev_weight, prev_indices = 0, ()
                
                cand_weight = prev_weight + w_i
                cand_indices = prev_indices + (orig_i,)
                
                # Compare and keep the better one
                if is_better(cand_weight, cand_indices, best_weight, best_indices):
                    best_weight, best_indices = cand_weight, cand_indices
                
                dp[k][i+1] = (best_weight, best_indices)
        
        # The answer is dp[4][n] (up to 4 intervals among all n)
        result = dp[4][n][1]
        return list(result)