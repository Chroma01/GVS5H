import bisect
from typing import List

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Attach original indices and sort by right endpoint
        sorted_intervals = sorted(
            (l, r, w, idx) for idx, (l, r, w) in enumerate(intervals),
            key=lambda x: x[1]
        )
        # Extract right endpoints for binary search
        rights = [r for (_, r, _, _) in sorted_intervals]
        # Precompute predecessor indices p[i] = largest j < i with r_j < l_i
        p = [0] * n
        for i in range(n):
            l_i = sorted_intervals[i][0]
            # Use bisect_left to find first position with r >= l_i, then -1
            j = bisect.bisect_left(rights, l_i, hi=i) - 1
            p[i] = j
        
        # dp[i][k] = best (weight, tuple(indices)) using intervals up to i and exactly k intervals
        # Initialize with invalid: weight = -1
        dp = [[(-1, ()) for _ in range(5)] for _ in range(n)]
        for i in range(n):
            l_i, r_i, w_i, idx_i = sorted_intervals[i]
            # Base case: picking 0 intervals always valid
            dp[i][0] = (0, ())
            # Option 1: skip current interval
            if i > 0:
                for k in range(5):
                    dp[i][k] = dp[i-1][k]  # start with skipping
            else:
                # i == 0, only k=0 is valid so far
                for k in range(1, 5):
                    dp[i][k] = (-1, ())
            
            # Option 2: take current interval (if it leads to a better state)
            for k in range(1, 5):
                # We need the best state from p[i] with k-1 intervals
                if k == 1:
                    # Starting fresh, no previous intervals
                    candidate = (w_i, (idx_i,))
                else:
                    prev_i = p[i]
                    if prev_i == -1:
                        continue  # cannot pick k intervals if no valid predecessor
                    # Get best state with k-1 intervals up to prev_i
                    if prev_i > 0:
                        prev_state = dp[prev_i][k-1]
                    else:
                        # prev_i == 0, use dp[0][k-1] (which may be invalid)
                        prev_state = dp[0][k-1]
                    if prev_state[0] == -1:
                        continue  # invalid previous state
                    # Combine: add current interval weight and merge indices (keep sorted)
                    # prev_state[1] is already sorted
                    new_indices = prev_state[1] + (idx_i,)
                    # Since we iterate i in increasing order of r and idx_i may not be in order,
                    # but the list is built by adding indices of intervals with increasing r.
                    # The original idx is not guaranteed to be sorted, so we must sort.
                    new_indices = tuple(sorted(new_indices))
                    candidate = (prev_state[0] + w_i, new_indices)
                
                # Compare with current dp[i][k] (which is currently either invalid or from skipping)
                current = dp[i][k]
                if current[0] < candidate[0]:
                    dp[i][k] = candidate
                elif current[0] == candidate[0]:
                    if candidate[1] < current[1]:  # lexicographic comparison
                        dp[i][k] = candidate
        
        # Find the best across k=0..4
        best_weight = -1
        best_indices = ()
        for k in range(5):
            w, idxs = dp[n-1][k]
            if w > best_weight:
                best_weight = w
                best_indices = idxs
            elif w == best_weight:
                if idxs < best_indices:
                    best_indices = idxs
        
        return list(best_indices)