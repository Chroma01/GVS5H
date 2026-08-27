class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Preprocess pairs: store as (min_val, max_val)
        pairs = []
        for a, b in conflictingPairs:
            if a > b:
                a, b = b, a
            pairs.append((a, b))
        
        # Group pairs by their min value (left endpoint)
        # pairs_by_l[l] will contain list of max values for pairs with min = l
        pairs_by_l = [[] for _ in range(n + 1)]
        for l, r in pairs:
            pairs_by_l[l].append(r)
        
        # We'll sweep l from n down to 1
        # Maintain a min-heap of active max values (from pairs with min >= l)
        import heapq
        heap = []  # min-heap of max values
        min1 = [0] * (n + 1)  # min1[l] = smallest max value in heap at step l
        min2 = [0] * (n + 1)  # min2[l] = second smallest max value in heap at step l
        
        # We'll also store the actual heap state? No, we just need min1 and min2.
        # But to get min2, we might need to peek at the heap.
        # Actually, we can maintain the heap and also a separate structure for min2?
        # Standard technique: use a heap, and when popping, if the top is the same as min1, 
        # then the next top is min2. But we need to keep the heap intact for the next step.
        # Instead, we can just use two heaps? Or we can do:
        # At each step, after adding new pairs, we get min1 = heap[0].
        # To get min2, we can pop min1, get new top, then push min1 back.
        # But that's O(log m) per step, which is acceptable.
        
        # Initialize min1 and min2 with infinity (represented by n+1 or a large number)
        INF = n + 1
        min1 = [INF] * (n + 1)
        min2 = [INF] * (n + 1)
        
        for l in range(n, 0, -1):
            # Add all pairs that start at l
            for r in pairs_by_l[l]:
                heapq.heappush(heap, r)
            
            # Get min1
            if heap:
                min1[l] = heap[0]
                # Get min2: pop min1, get new top, push min1 back
                val1 = heapq.heappop(heap)
                if heap:
                    min2[l] = heap[0]
                else:
                    min2[l] = INF
                heapq.heappush(heap, val1)
            else:
                min1[l] = INF
                min2[l] = INF
        
        # Precompute invalid counts for min1 and min2
        # invalid1[l] = max(0, n - min1[l] + 1) if min1[l] <= n else 0
        # invalid2[l] = max(0, n - min2[l] + 1) if min2[l] <= n else 0
        invalid1 = [0] * (n + 1)
        invalid2 = [0] * (n + 1)
        for l in range(1, n + 1):
            if min1[l] <= n:
                invalid1[l] = n - min1[l] + 1
            if min2[l] <= n:
                invalid2[l] = n - min2[l] + 1
        
        # Precompute prefix sums for invalid1 and invalid2
        # prefix_invalid1[i] = sum(invalid1[1..i])
        prefix_invalid1 = [0] * (n + 1)
        prefix_invalid2 = [0] * (n + 1)
        for i in range(1, n + 1):
            prefix_invalid1[i] = prefix_invalid1[i-1] + invalid1[i]
            prefix_invalid2[i] = prefix_invalid2[i-1] + invalid2[i]
        
        # Base invalid count (with all pairs)
        base_invalid = prefix_invalid1[n]
        
        # For each pair removal, compute new invalid count
        # For a pair (L, R), the new invalid count is:
        #   base_invalid - sum_{l=1}^{L} [if min1[l] == R then invalid1[l] else 0] 
        #                 + sum_{l=1}^{L} [if min1[l] == R then invalid2[l] else 0]
        # = base_invalid + sum_{l=1}^{L} [if min1[l] == R then (invalid2[l] - invalid1[l]) else 0]
        
        # Precompute for each R value, the sum of (invalid2[l] - invalid1[l]) for l where min1[l] == R
        # Use a dictionary: diff_sum[R] = sum of (invalid2[l] - invalid1[l]) for l with min1[l] == R
        diff_sum = {}
        for l in range(1, n + 1):
            r_val = min1[l]
            if r_val <= n:  # only if min1[l] is valid
                diff = invalid2[l] - invalid1[l]
                if r_val not in diff_sum:
                    diff_sum[r_val] = 0
                diff_sum[r_val] += diff
        
        # Also, we need to consider only l <= L for each pair. 
        # But the above diff_sum is for all l. We need to restrict to l <= L.
        # So we need to store, for each R, a list of (l, diff) and then use prefix sums per R? 
        # That might be too heavy.
        #
        # Alternative: Instead of precomputing diff_sum globally, we can iterate over pairs and for each pair, 
        # we need sum_{l=1}^{L} [min1[l] == R] * (invalid2[l] - invalid1[l]).
        # We can precompute for each R, a prefix sum array? But R can be up to n, and there are n possible R's.
        # We can create an array for each R? That would be O(n^2) space.
        #
        # Better: We can store for each R, a list of l's where min1[l] == R, and then for each pair, 
        # we need the sum of diffs for l in that list that are <= L.
        # We can precompute for each R, a sorted list of (l, diff) and then use binary search or prefix sums.
        #
        # Let's do:
        #   r_to_l_diffs = defaultdict(list)  # r -> list of (l, diff)
        # Then for each R, we can create a prefix sum array for the diffs, indexed by the order in the list.
        # But then for a given L, we need to sum diffs for l <= L. We can use bisect to find the index.
        
        from collections import defaultdict
        import bisect
        
        r_to_l_diffs = defaultdict(list)
        for l in range(1, n + 1):
            r_val = min1[l]
            if r_val <= n:
                diff = invalid2[l] - invalid1[l]
                r_to_l_diffs[r_val].append((l, diff))
        
        # For each R, sort by l (already sorted if we iterate l from 1 to n, but let's sort to be safe)
        # Actually, we iterated l from 1 to n, so the lists are sorted by l.
        # Precompute prefix sums for each R
        r_to_prefix_diff = {}
        for r_val, l_diffs in r_to_l_diffs.items():
            # l_diffs is list of (l, diff), sorted by l
            prefix = [0] * (len(l_diffs) + 1)
            for i, (l, diff) in enumerate(l_diffs):
                prefix[i+1] = prefix[i] + diff
            r_to_prefix_diff[r_val] = (l_diffs, prefix)
        
        # Now, for each pair (L, R), compute the adjustment
        # adjustment = sum of diffs for l <= L with min1[l] == R
        # We can use bisect_right to find the index in l_diffs for l <= L
        
        best_new_invalid = float('inf')
        
        for L, R in pairs:
            # Get the list and prefix for this R
            if R in r_to_prefix_diff:
                l_diffs, prefix = r_to_prefix_diff[R]
                # Find the largest index such that l_diffs[i][0] <= L
                # bisect_right on the l values
                l_values = [x[0] for x in l_diffs]
                idx = bisect.bisect_right(l_values, L)
                adjustment = prefix[idx]
            else:
                adjustment = 0
            
            new_invalid = base_invalid + adjustment
            if new_invalid < best_new_invalid:
                best_new_invalid = new_invalid
        
        total_subarrays = n * (n + 1) // 2
        return total_subarrays - best_new_invalid