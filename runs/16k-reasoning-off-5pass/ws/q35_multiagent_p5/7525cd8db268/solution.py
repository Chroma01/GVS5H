class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Normalize pairs: a < b
        pairs = []
        for x, y in conflictingPairs:
            if x > y:
                x, y = y, x
            pairs.append((x, y))
        
        # Group pairs by their left endpoint a
        pairs_at_a = [[] for _ in range(n + 1)]
        for a, b in pairs:
            pairs_at_a[a].append(b)
            
        # Precompute best_b, second_best_b, and count_best for each l
        # best_b[l] = min b among all pairs with a' <= l
        # second_best_b[l] = second min b among all pairs with a' <= l
        # count_best[l] = count of pairs with a' <= l that have b == best_b[l]
        
        best_b = [float('inf')] * (n + 2)
        second_best_b = [float('inf')] * (n + 2)
        count_best = [0] * (n + 2)
        
        # Current state as we sweep l from 1 to n
        cur_best = float('inf')
        cur_second = float('inf')
        cur_count = 0
        
        for l in range(1, n + 1):
            # Update current best/second with pairs starting at l
            for b in pairs_at_a[l]:
                if b < cur_best:
                    cur_second = cur_best
                    cur_best = b
                    cur_count = 1
                elif b == cur_best:
                    cur_count += 1
                elif b < cur_second:
                    cur_second = b
            
            best_b[l] = cur_best
            second_best_b[l] = cur_second
            count_best[l] = cur_count
            
        # Helper to compute valid subarrays starting at l given a bottleneck R
        def valid_subarrays(l, R):
            if R > n:
                return n - l + 1
            else:
                return max(0, R - l)
        
        # Compute total good subarrays for the original set
        total_good_global = 0
        for l in range(1, n + 1):
            total_good_global += valid_subarrays(l, best_b[l])
            
        # For each pair, compute the gain if we remove it
        # Gain for pair [a,b] = sum_{l=1}^{a} [best_b[l]==b and count_best[l]==1] * (valid(l, second_best_b[l]) - valid(l, best_b[l]))
        
        # Aggregate gains by b value
        # For each b, store list of (l, gain) where gain = valid(l, second_best_b[l]) - valid(l, best_b[l])
        # and best_b[l] == b and count_best[l] == 1
        from collections import defaultdict
        gains_by_b = defaultdict(list)
        
        for l in range(1, n + 1):
            if count_best[l] == 1:
                b_val = best_b[l]
                if b_val <= n:  # Only consider if there is a bottleneck
                    gain = valid_subarrays(l, second_best_b[l]) - valid_subarrays(l, b_val)
                    if gain > 0:
                        gains_by_b[b_val].append((l, gain))
        
        # For each b, sort by l and compute prefix sums
        for b_val in gains_by_b:
            gains_by_b[b_val].sort(key=lambda x: x[0])
            prefix_sum = [0] * (len(gains_by_b[b_val]) + 1)
            for i, (l, gain) in enumerate(gains_by_b[b_val]):
                prefix_sum[i+1] = prefix_sum[i] + gain
            gains_by_b[b_val] = (prefix_sum, gains_by_b[b_val])
            
        # For each pair, query the gain
        import bisect
        
        max_good = 0
        for a, b in pairs:
            # Get prefix sum array for b
            if b in gains_by_b:
                prefix_sum, _ = gains_by_b[b]
                # Find all l <= a
                # The list is sorted by l, so we can use bisect_right
                # We want sum of gains for l <= a
                # Find the rightmost index where l <= a
                indices = [x[0] for x in gains_by_b[b][1]]
                idx = bisect.bisect_right(indices, a)
                reduction = prefix_sum[idx]
            else:
                reduction = 0
                
            current_good = total_good_global + reduction
            if current_good > max_good:
                max_good = current_good
                
        return max_good