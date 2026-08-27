import heapq
from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Normalize pairs to (L, R) with L <= R
        pairs = []
        for i, (a, b) in enumerate(conflictingPairs):
            if a > b:
                a, b = b, a
            pairs.append((a, b, i))  # Store original index
        
        # Total subarrays
        total_subarrays = n * (n + 1) // 2
        
        # If no pairs, removing one is not possible? But constraints say length >= 1.
        # If only one pair, removing it leaves 0 invalid subarrays.
        if not pairs:
            return total_subarrays
            
        # Sort pairs by R
        pairs.sort(key=lambda x: x[1])
        
        # We'll use a min-heap to store (L, original_index)
        heap = []
        # Count of each L in the heap? Actually, we need to know the count of the minimum L.
        # We can use a dictionary to count frequencies of L in the heap.
        from collections import defaultdict
        count = defaultdict(int)
        
        # F[j] will store the minimum L for pairs with R <= j
        F = [0] * (n + 1)
        
        # To compute S[j] (second smallest L), we can peek at the heap.
        # But heapq doesn't support peeking the second element easily.
        # We'll use a trick: pop the min, check the next, and push back.
        # However, we need to know which pair is the min to attribute the impact.
        
        # We'll store the impact for each pair index.
        impact = [0] * len(pairs)
        
        # Pointer to pairs
        p_idx = 0
        m = len(pairs)
        
        # We also need to know the second smallest L for each j.
        # We can maintain a separate heap for the second smallest? Or just query.
        # Given n up to 1e5, doing a heap pop/peek for each j is O(n log m), which is acceptable.
        
        for j in range(1, n + 1):
            # Add all pairs with R == j
            while p_idx < m and pairs[p_idx][1] == j:
                L, R, orig_idx = pairs[p_idx]
                heapq.heappush(heap, (L, orig_idx))
                count[L] += 1
                p_idx += 1
            
            if not heap:
                F[j] = 0
                continue
                
            # Get the minimum L
            min_L, min_orig_idx = heap[0]
            F[j] = min_L
            
            # Check if the minimum is unique
            if count[min_L] == 1:
                # Find the second smallest L
                # We need to peek the next element in the heap.
                # Since heapq is a min-heap, the second smallest might not be at index 1 if there are duplicates of the min.
                # But here count[min_L] == 1, so the min is unique.
                # The next smallest is the smallest L that is > min_L.
                # We can pop the min, then the new top is the second smallest.
                heapq.heappop(heap)
                if heap:
                    second_L = heap[0][0]
                else:
                    second_L = float('inf')
                heapq.heappush(heap, (min_L, min_orig_idx))
                
                # The diff for this j is min_L - second_L
                # But if second_L is inf, diff is min_L (since new min becomes 0? No, if no other pairs, new min is inf -> 0 invalid)
                # Actually, if second_L is inf, it means no other pairs, so new F[j] = 0.
                # So diff = min_L - 0 = min_L.
                if second_L == float('inf'):
                    diff = min_L
                else:
                    diff = min_L - second_L
                
                # Add this diff to the impact of the pair that is the unique minimizer
                impact[min_orig_idx] += diff
            else:
                # Not unique, so removing one instance doesn't change the min for this j.
                pass
                
        total_invalid = sum(F[1:])
        
        min_remaining_invalid = float('inf')
        for imp in impact:
            remaining = total_invalid - imp
            if remaining < min_remaining_invalid:
                min_remaining_invalid = remaining
                
        return total_subarrays - min_remaining_invalid