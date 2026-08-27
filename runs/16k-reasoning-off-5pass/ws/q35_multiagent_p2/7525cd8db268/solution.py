class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # For each L (min(a,b)), store a min-heap of R (max(a,b))
        # But we'll use sorted lists for easier removal
        heaps_list = [[] for _ in range(n + 1)]
        for a, b in conflictingPairs:
            L, R = min(a, b), max(a, b)
            heaps_list[L].append(R)
        for L in range(1, n + 1):
            heaps_list[L].sort()
        
        # Precompute min_end[i]: the minimum R for pairs with L >= i
        min_end = [float('inf')] * (n + 2)
        # Process from right to left
        current_min = float('inf')
        for i in range(n, 0, -1):
            if heaps_list[i]:
                if heaps_list[i][0] < current_min:
                    current_min = heaps_list[i][0]
            min_end[i] = current_min
        
        # Function to compute total valid subarrays given min_end array
        def compute_valid(min_end_arr):
            total = 0
            for i in range(1, n + 1):
                me = min_end_arr[i]
                if me > n:
                    count = n - i + 1
                else:
                    count = me - i
                if count < 0:
                    count = 0
                total += count
            return total
        
        # Precompute base valid count (with all pairs)
        base_valid = compute_valid(min_end)
        best = base_valid
        
        # For each conflicting pair, remove it and compute the new valid count
        # We need to know which R to remove for each pair. Since there can be duplicates, we remove one occurrence.
        # We'll iterate over conflictingPairs and for each, remove one R from heaps_list[L] and update min_end for affected indices.
        
        # To avoid O(n) per removal for the entire min_end array, we can update only the affected part.
        # But for simplicity and given constraints, we'll recompute min_end for each removal in O(n).
        
        # Save original heaps_list for restoration
        original_heaps = [list(h) for h in heaps_list]
        
        for a, b in conflictingPairs:
            L, R = min(a, b), max(a, b)
            # Remove R from heaps_list[L]
            # Find the index of R in heaps_list[L] (remove first occurrence)
            idx = heaps_list[L].index(R)
            heaps_list[L].pop(idx)
            
            # Recompute min_end from L down to 1 (since min_end[i] for i > L is unchanged)
            # But actually, min_end[i] for i <= L might change because the min for L changed.
            # We need to recompute min_end from n down to 1? Actually, only min_end[i] for i <= L can change.
            # But min_end[i] = min(min_end[i+1], min_R_for_L_i)
            # So we can recompute from L down to 1.
            
            # Create a copy of min_end to update
            new_min_end = list(min_end)
            current_min = float('inf')
            # Recompute from n down to L
            # But min_end[i] for i > L is unchanged, so we start from L
            # Actually, min_end[L] = min(heaps_list[L][0] if exists else inf, min_end[L+1])
            # Then min_end[L-1] = min(heaps_list[L-1][0] if exists else inf, min_end[L]), etc.
            # So we recompute from L down to 1.
            
            # Start from L and go down to 1
            # But note: min_end[L] depends on min_end[L+1] which is unchanged.
            # So:
            current_min = min_end[L + 1]  # min_end[L+1] is unchanged
            for i in range(L, 0, -1):
                if heaps_list[i]:
                    if heaps_list[i][0] < current_min:
                        current_min = heaps_list[i][0]
                new_min_end[i] = current_min
            
            # Compute valid count for this removal
            current_valid = compute_valid(new_min_end)
            if current_valid > best:
                best = current_valid
                
            # Restore heaps_list[L]
            heaps_list[L].insert(idx, R)
            # Restore min_end to original (we can just use the original min_end for next iteration, but we need to restore heaps_list which we did)
            # Actually, we don't need to restore min_end because we created a new array for each removal.
            # But we did modify heaps_list, so we restored it.
            
        return best