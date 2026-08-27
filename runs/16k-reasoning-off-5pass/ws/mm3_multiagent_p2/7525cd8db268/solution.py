from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Normalize pairs so that a < b (left endpoint is the smaller index)
        # Group pairs by their right endpoint b
        pairs_by_right = [[] for _ in range(n + 1)]  # 1-indexed
        for idx, (x, y) in enumerate(conflictingPairs):
            a, b = x, y
            if a > b:
                a, b = b, a
            pairs_by_right[b].append((a, idx))
        
        # Sweep from 1 to n
        # Maintain top two maximum 'a' values among pairs with right endpoint <= i
        # L1: largest a, L2: second largest a
        # idx_L1: pair index contributing L1, idx_L2: pair index contributing L2
        L1 = 0
        L2 = 0
        idx_L1 = -1
        idx_L2 = -1
        
        baseline = 0
        # gain[idx] = total gain if we remove pair idx
        gain = [0] * len(conflictingPairs)
        
        for i in range(1, n + 1):
            # Update top two with all pairs ending at i
            for a, idx in pairs_by_right[i]:
                if a > L1:
                    # New maximum: old L1 becomes L2
                    L2 = L1
                    idx_L2 = idx_L1
                    L1 = a
                    idx_L1 = idx
                elif a > L2:
                    L2 = a
                    idx_L2 = idx
                # If a == L2 or a == L1, we keep the existing attribution.
                # The first pair encountered with a given value keeps the slot.
                # However, we must ensure that if a == L1, we don't accidentally
                # overwrite idx_L1. The strict '>' handles this correctly.
            
            # Add contribution of subarrays ending at i
            baseline += i - L1
            
            # If L1 > L2, removing the pair contributing L2 gives gain (L1 - L2) at this i
            if L1 > L2:
                gain[idx_L2] += L1 - L2
        
        max_gain = max(gain) if gain else 0
        return baseline + max_gain