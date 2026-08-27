import bisect
from typing import List

class Solution:
    def maximumWeight(self, intervals: List[List[int]]) -> List[int]:
        n = len(intervals)
        if n == 0:
            return []
        
        # Store (l, r, weight, original_index)
        # We keep the original index to handle lexicographical order correctly
        sorted_intervals = sorted(intervals, key=lambda x: (x[1], x[0]))
        
        # Coordinate compression for start times
        start_times = sorted(set(x[0] for x in sorted_intervals))
        start_map = {val: i for i, val in enumerate(start_times)}
        m = len(start_times)
        
        # Segment Tree for range max query
        class SegmentTree:
            def __init__(self, size):
                self.n = 1
                while self.n < size:
                    self.n *= 2
                self.tree = [-1] * (2 * self.n)
            
            def update(self, i, val):
                i += self.n
                self.tree[i] = max(self.tree[i], val)
                while i > 1:
                    self.tree[i >> 1] = max(self.tree[i >> 1], self.tree[i])
                    i >>= 1
            
            def query(self, l, r):
                if l > r:
                    return -1
                l += self.n
                r += self.n
                res = -1
                while l <= r:
                    if l % 2 == 1:
                        res = max(res, self.tree[l])
                        l += 1
                    if r % 2 == 0:
                        res = max(res, self.tree[r])
                        r -= 1
                    l >>= 1
                    r >>= 1
                return res

        # dp[k][i] = max weight using exactly k intervals ending with sorted_intervals[i]
        dp = [[-1] * n for _ in range(5)]
        
        # Base case: k=1
        for i in range(n):
            dp[1][i] = sorted_intervals[i][2]
        
        # Precompute end times for binary search
        end_times = [x[1] for x in sorted_intervals]
        
        # Fill DP for k=2 to 4
        for k in range(2, 5):
            # Precompute prefix max for dp[k-1]
            prefix_max = [-1] * n
            current_max = -1
            for idx in range(n):
                current_max = max(current_max, dp[k-1][idx])
                prefix_max[idx] = current_max
            
            for i in range(n):
                l, r, w = sorted_intervals[i]
                # Find largest index 'ptr' such that sorted_intervals[ptr].end < l
                # bisect_left gives the first index where end_times[idx] >= l
                idx = bisect.bisect_left(end_times, l)
                if idx > 0:
                    best_prev = prefix_max[idx-1]
                    if best_prev != -1:
                        dp[k][i] = best_prev + w
        
        # Find global max weight
        max_w = 0
        for k in range(1, 5):
            for i in range(n):
                if dp[k][i] > max_w:
                    max_w = dp[k][i]
        
        if max_w == 0:
            return []
        
        # suffix_dp[k][i] = max weight using exactly k intervals starting with sorted_intervals[i]
        suffix_dp = [[-1] * n for _ in range(5)]
        
        # Initialize for k=1
        for i in range(n):
            suffix_dp[1][i] = sorted_intervals[i][2]
        
        # Build Segment Tree with k=1 values
        st = SegmentTree(m)
        for i in range(n):
            rank = start_map[sorted_intervals[i][0]]
            st.update(rank, suffix_dp[1][i])
        
        # Compute suffix_dp for k=2 to 4
        for k in range(2, 5):
            for i in range(n):
                l, r, w = sorted_intervals[i]
                # We need max(suffix_dp[k-1][j]) for all j such that start_j > r
                # Find smallest rank such that start_times[rank] > r
                idx = bisect.bisect_right(start_times, r)
                if idx < m:
                    best = st.query(idx, m-1)
                    if best != -1:
                        suffix_dp[k][i] = w + best
            
            # Update ST with suffix_dp[k] values
            for i in range(n):
                rank = start_map[sorted_intervals[i][0]]
                st.update(rank, suffix_dp[k][i])
        
        best_seq = None
        
        # Reconstruct lexicographically smallest sequence
        # Check lengths 1 to 4
        for L in range(1, 5):
            current_weight = max_w
            current_end = -1
            seq = []
            possible = True
            
            for step in range(1, L + 1):
                found = False
                # Iterate original indices to find the lexicographically smallest valid next interval
                for v in range(n):
                    # Check start constraint (non-overlapping)
                    if step > 1:
                        if intervals[v][0] <= current_end:
                            continue
                    
                    rem_weight = current_weight - intervals[v][2]
                    
                    # Check if we can complete the sequence
                    if step == L:
                        # Last interval, remaining weight must be 0
                        if rem_weight != 0:
                            continue
                    else:
                        # Need to check if there exists a sequence of length L-step starting after v
                        # with weight rem_weight.
                        # This is equivalent to: max_{j: start_j > intervals[v].end} suffix_dp[L-step][j] == rem_weight
                        end_v = intervals[v][1]
                        max_rem = -1
                        
                        # Optimization: We can iterate all j. Since N=50000 and L is small, this is acceptable.
                        # O(N) per step, total O(N*L^2) ~ 50000 * 16 = 800,000 operations.
                        for j in range(n):
                            if intervals[j][0] > end_v:
                                if suffix_dp[L-step][j] > max_rem:
                                    max_rem = suffix_dp[L-step][j]
                        
                        if max_rem != rem_weight:
                            continue
                    
                    # If we are here, v is a valid candidate.
                    seq.append(v)
                    current_end = intervals[v][1]
                    current_weight = rem_weight
                    found = True
                    break
                
                if not found:
                    possible = False
                    break
            
            if possible:
                if best_seq is None or seq < best_seq:
                    best_seq = seq
        
        return best_seq