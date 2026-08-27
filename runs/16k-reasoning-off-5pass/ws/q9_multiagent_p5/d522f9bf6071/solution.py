from typing import List
import bisect

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []
        
        # Store original index with interval data
        # Format: (l, r, weight, original_index)
        indexed_intervals = []
        for i in range(n):
            l, r, w = intervals[i]
            indexed_intervals.append((l, r, w, i))
        
        # Sort by start time, then by end time, then by weight, then by original index
        indexed_intervals.sort(key=lambda x: (x[0], x[1], x[2], x[3]))
        
        # Extract sorted arrays for easier access
        sorted_l = [x[0] for x in indexed_intervals]
        sorted_r = [x[1] for x in indexed_intervals]
        sorted_w = [x[2] for x in indexed_intervals]
        sorted_idx = [x[3] for x in indexed_intervals]
        
        # Precompute suffix max DP
        # dp[k][i] = maximum weight achievable by selecting exactly k non-overlapping intervals
        # from the suffix starting at index i in the sorted list.
        NEG_INF = -1
        
        dp = [[NEG_INF] * n for _ in range(5)]
        
        # Base case: k=1
        current_max = NEG_INF
        for i in range(n - 1, -1, -1):
            current_max = max(current_max, sorted_w[i])
            dp[1][i] = current_max
            
        # Fill for k=2 to 4
        for k in range(2, 5):
            # Precompute next_idx for each i
            next_idx = [0] * n
            for i in range(n):
                idx = bisect.bisect_right(sorted_l, sorted_r[i], lo=i+1)
                next_idx[i] = idx if idx < n else n
            
            # Compute dp[k]
            current_dp = [NEG_INF] * (n + 1)
            current_dp[n] = NEG_INF
            
            for i in range(n - 1, -1, -1):
                skip_val = current_dp[i+1]
                take_val = NEG_INF
                if next_idx[i] < n:
                    prev_max = dp[k-1][next_idx[i]]
                    if prev_max != NEG_INF:
                        take_val = sorted_w[i] + prev_max
                
                current_dp[i] = max(skip_val, take_val)
            
            dp[k] = current_dp[:n]
            
        # Helper to build SegTree
        def build_seg_tree(arr):
            size = 1
            while size <= len(arr):
                size *= 2
            tree = [NEG_INF] * (2 * size)
            for i in range(len(arr)):
                tree[size + i] = arr[i]
            for i in range(size - 1, 0, -1):
                tree[i] = max(tree[2*i], tree[2*i+1])
            return tree, size
        
        def update_seg_tree(tree, size, idx, val):
            idx += size
            tree[idx] = val
            while idx > 1:
                idx //= 2
                tree[idx] = max(tree[2*idx], tree[2*idx+1])
        
        def query_seg_tree(tree, size, l, r):
            if l > r:
                return NEG_INF
            l += size
            r += size
            res = NEG_INF
            while l <= r:
                if l % 2 == 1:
                    res = max(res, tree[l])
                    l += 1
                if r % 2 == 0:
                    res = max(res, tree[r])
                    r -= 1
                l //= 2
                r //= 2
            return res
        
        # Build SegTrees for k=1..4
        seg_trees = []
        sizes = []
        for k in range(1, 5):
            arr = dp[k][:]
            tree, size = build_seg_tree(arr)
            seg_trees.append(tree)
            sizes.append(size)
            
        # Find GlobalMax
        global_max = NEG_INF
        for k in range(1, 5):
            if dp[k][0] > global_max:
                global_max = dp[k][0]
        
        if global_max == NEG_INF:
            return []
            
        candidates = []
        
        # Compute pos_in_sorted
        pos_in_sorted = [0] * n
        for idx, (l, r, w, orig) in enumerate(indexed_intervals):
            pos_in_sorted[orig] = idx
        
        # Try each k
        for k in range(1, 5):
            if dp[k][0] != global_max:
                continue
            
            # Reset SegTree for this k
            arr = dp[k][:]
            tree, size = build_seg_tree(arr)
            
            current_set = []
            last_end = -1
            last_orig = -1
            k_curr = k
            needed = global_max
            picked_count = 0
            
            # Iterate I from 0 to n-1 (original indices)
            for I in range(n):
                # Remove I from SegTree
                u = pos_in_sorted[I]
                update_seg_tree(tree, size, u, NEG_INF)
                
                if picked_count == k:
                    break
                
                if k_curr == 0:
                    break
                
                # Check if I can be the next interval
                if sorted_l[u] > last_end:
                    l_query = bisect.bisect_right(sorted_l, sorted_r[u])
                    if l_query < n:
                        q = query_seg_tree(tree, size, l_query, n-1)
                        if q != NEG_INF and sorted_w[u] + q == needed:
                            current_set.append(I)
                            picked_count += 1
                            last_end = sorted_r[u]
                            last_orig = I
                            k_curr -= 1
                            needed -= sorted_w[u]
            
            if picked_count == k:
                candidates.append(current_set)
        
        if not candidates:
            return []
        
        candidates.sort()
        return candidates[0]