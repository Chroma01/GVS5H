import bisect
from typing import List

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        # Sort intervals by right endpoint, keeping original indices
        # arr[i] = [l, r, weight, original_index]
        arr = sorted(intervals, key=lambda x: x[1])
        arr = [[l, r, w, i] for i, (l, r, w) in enumerate(arr)]
        
        # Precompute lefts for binary search
        lefts = [a[0] for a in arr]
        
        # Precompute next_valid[i]: the smallest index j such that arr[j].l > arr[i].r
        next_valid = [0] * n
        for i in range(n):
            # bisect_right returns the insertion point to maintain sorted order
            # all values to the left are <= arr[i][1]
            # so the value at that index is > arr[i][1]
            next_valid[i] = bisect.bisect_right(lefts, arr[i][1])
        
        # dp2[k][i] = max weight using k intervals from arr[i:]
        # k from 0 to 4, i from 0 to n (dp2[k][n] = 0)
        dp2 = [[0] * (n + 1) for _ in range(5)]
        
        # Fill dp2 from bottom up
        for k in range(1, 5):
            for i in range(n - 1, -1, -1):
                # Option 1: skip interval i
                skip = dp2[k][i + 1]
                # Option 2: take interval i
                j = next_valid[i]
                take = arr[i][2] + dp2[k - 1][j]  # dp2[k-1][n] is 0, so safe
                dp2[k][i] = max(skip, take)
        
        # Maximum weight for up to 4 intervals
        max_weight = dp2[4][0]
        
        # Reconstruction
        res = []
        k = 4
        last_r = -1  # right endpoint of last chosen interval
        
        # We'll choose 4 intervals
        for step in range(4):
            # Find the first interval in arr that starts after last_r
            start_i = bisect.bisect_right(lefts, last_r)
            if start_i >= n:
                break
            
            # The maximum weight achievable for k intervals from start_i onward
            total_max = dp2[k][start_i]
            
            # Collect all valid candidates (intervals that start after last_r)
            # and sort them by original index to get lexicographically smallest
            candidates = []
            for i in range(start_i, n):
                # arr[i][0] is l, which is > last_r by definition of start_i
                candidates.append((arr[i][3], i))  # (original_index, position in arr)
            candidates.sort(key=lambda x: x[0])
            
            found = False
            for orig_idx, pos in candidates:
                w = arr[pos][2]
                j = next_valid[pos]
                rem = dp2[k - 1][j]  # dp2[k-1][n] is 0, so safe
                if w + rem == total_max:
                    # This interval is part of an optimal solution
                    res.append(orig_idx)
                    last_r = arr[pos][1]
                    found = True
                    break
            
            if not found:
                # Should not happen if max_weight is achievable
                break
            
            k -= 1
        
        return res