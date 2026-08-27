from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Organize intervals by their start position
        # An interval is [min(a,b), max(a,b)]
        starts = [[] for _ in range(n + 2)]
        for a, b in conflictingPairs:
            l, r = min(a, b), max(a, b)
            starts[l].append(r)
        
        # min1[x] stores the minimum r among all intervals starting >= x
        # min2[x] stores the second minimum r among all intervals starting >= x
        # count_min[x] stores how many intervals achieve the minimum r
        # We use n + 1 as infinity since valid subarrays can extend up to n
        min1 = [n + 1] * (n + 2)
        min2 = [n + 1] * (n + 2)
        count_min = [0] * (n + 2)
        
        # Map each value v to the range [L, R] where min1[x] == v
        val_ranges = {}
        
        current_min1 = n + 1
        current_min2 = n + 1
        current_count = 0
        
        # Iterate backwards from n to 1 to accumulate intervals
        # As x decreases, the set of intervals starting >= x grows
        for x in range(n, 0, -1):
            # Update min1, min2, count_min with intervals starting at x
            for r in starts[x]:
                if r < current_min1:
                    current_min2 = current_min1
                    current_min1 = r
                    current_count = 1
                elif r == current_min1:
                    current_count += 1
                elif r < current_min2:
                    current_min2 = r
            
            min1[x] = current_min1
            min2[x] = current_min2
            count_min[x] = current_count
            
            # Record the range for the current minimum value
            # Since min1 is non-decreasing as x increases, the range for a specific value is contiguous
            if current_min1 != n + 1:
                if current_min1 not in val_ranges:
                    val_ranges[current_min1] = [x, x]
                else:
                    val_ranges[current_min1][1] = x
        
        # Precompute prefix sums of the potential gain (diff)
        # diff[x] is the increase in valid subarrays count at x if the unique minimum interval is removed
        # Gain at x is (new_min - old_min) = (min2[x] - min1[x]) if count_min[x] == 1
        prefix_diff = [0] * (n + 2)
        for x in range(1, n + 1):
            # Only if there is a unique minimum interval that is not "infinity" (no intervals)
            if count_min[x] == 1 and min1[x] != n + 1:
                prefix_diff[x] = prefix_diff[x-1] + (min2[x] - min1[x])
            else:
                prefix_diff[x] = prefix_diff[x-1]
        
        # Calculate the total valid subarrays with all pairs present
        # A subarray starting at x is valid if it ends at y < min1[x]
        # Number of such y is max(0, min1[x] - x). Since min1[x] >= x always (or n+1), it's min1[x] - x.
        base_total = 0
        for x in range(1, n + 1):
            base_total += (min1[x] - x)
        
        max_ans = base_total
        
        # Try removing each pair and update the maximum
        for a, b in conflictingPairs:
            l, r = min(a, b), max(a, b)
            
            # We only care if this pair was the unique minimum for some x <= l
            # Check if r is a value that appears as min1 in some range
            if r not in val_ranges:
                continue
            
            L_range, R_range = val_ranges[r]
            
            # The affected x are in the intersection of [1, l] and [L_range, R_range]
            # Because removing a pair [l, r] only affects x where l >= x (i.e., x <= l)
            start = max(1, L_range)
            end = min(l, R_range)
            
            if start <= end:
                # The gain is the sum of diffs in this range
                delta = prefix_diff[end] - prefix_diff[start - 1]
                max_ans = max(max_ans, base_total + delta)
        
        return max_ans