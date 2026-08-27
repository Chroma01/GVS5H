from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Total number of subarrays is n * (n + 1) / 2
        total_subarrays = n * (n + 1) // 2
        
        # If there's only one pair, removing it leaves 0 conflicting pairs.
        # All subarrays are valid.
        if len(conflictingPairs) == 1:
            return total_subarrays
        
        # Group pairs by their first element 'a' to easily find the best candidate.
        # We want to remove a pair [a, b] such that:
        # 1. b is minimized (smallest b).
        # 2. If ties in b, a is maximized (largest a).
        # We can store for each 'a', the minimum 'b' found so far.
        # Then iterate to find the global minimum 'b' and corresponding max 'a'.
        
        # Map: a -> min_b
        min_b_map = {}
        for a, b in conflictingPairs:
            if a not in min_b_map or b < min_b_map[a]:
                min_b_map[a] = b
        
        # Find the candidate pair to remove
        best_b = float('inf')
        best_a = -1
        
        for a, b in min_b_map.items():
            if b < best_b or (b == best_b and a > best_a):
                best_b = b
                best_a = a
        
        # Remove the candidate pair [best_a, best_b]
        # We need to calculate the number of invalid subarrays for the remaining pairs.
        # A subarray [i, j] (1-based indices) is invalid if there exists a remaining pair [a, b]
        # such that i <= a and j >= b.
        # This is equivalent to: j >= min{ b | exists [a, b] in remaining, a >= i }.
        # Let suffix_min[i] = min{ b | exists [a, b] in remaining, a >= i }.
        # If no such pair exists for a given i, suffix_min[i] = infinity.
        # The number of invalid subarrays starting at i is max(0, n - suffix_min[i] + 1).
        
        # We can compute suffix_min efficiently by iterating backwards from n to 1.
        # Initialize suffix_min with infinity.
        # We need a way to quickly query the min b for pairs with a >= i.
        # Since we iterate i from n down to 1, we can maintain the current minimum b.
        # When moving from i+1 to i, we include all pairs where a == i.
        
        # Prepare a list of b's for each a
        pairs_by_a = [[] for _ in range(n + 2)]  # 1 to n
        for a, b in conflictingPairs:
            if a == best_a and b == best_b:
                continue  # Skip the removed pair
            pairs_by_a[a].append(b)
        
        # Compute suffix minimums
        # current_min_b tracks min(b) for all pairs with a >= i
        current_min_b = float('inf')
        invalid_count = 0
        
        # Iterate i from n down to 1
        for i in range(n, 0, -1):
            # Update current_min_b with pairs starting at i
            if i <= n:
                for b in pairs_by_a[i]:
                    if b < current_min_b:
                        current_min_b = b
            
            # If current_min_b is still infinity, no constraint starts at or after i
            if current_min_b == float('inf'):
                # No invalid subarrays start at i
                continue
            
            # All subarrays starting at i and ending at j >= current_min_b are invalid.
            # Valid j range: [current_min_b, n]
            # Count = n - current_min_b + 1
            count = n - current_min_b + 1
            if count > 0:
                invalid_count += count
        
        return total_subarrays - invalid_count