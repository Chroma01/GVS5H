from typing import List
from collections import defaultdict

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Normalize pairs to (a, b) with a < b, and deduplicate
        unique_pairs = set()
        for p in conflictingPairs:
            a, b = p[0], p[1]
            if a > b:
                a, b = b, a
            unique_pairs.add((a, b))
        
        # For each right endpoint b, collect left endpoints a
        by_b = [[] for _ in range(n + 2)]
        for a, b in unique_pairs:
            by_b[b].append(a)
        
        total = 0
        # State: M1 (max a), count_M1, owner_b (b of the unique M1 pair), M2 (second largest a)
        M1 = 0
        count_M1 = 0
        owner_b = 0  # only valid when count_M1 == 1
        M2 = 0
        
        # Track gain per pair
        pair_gain = defaultdict(int)
        max_gain = 0
        
        for r in range(1, n + 1):
            # Add new pairs with right endpoint = r
            for a in by_b[r]:
                if a == M1:
                    count_M1 += 1
                    # Owner is lost (count >= 2)
                elif a > M1:
                    # New maximum. The old M1 (if any) becomes M2.
                    # The old owner's gain accumulation ends at r-1.
                    M2 = M1  # old M1 is now second largest
                    M1 = a
                    count_M1 = 1
                    owner_b = r
                else:
                    # a < M1
                    if a > M2:
                        M2 = a
            
            # Base contribution
            total += r - M1
            
            # Gain from removing the unique owner pair
            if count_M1 == 1:
                gain_r = M1 - M2
                pair = (M1, owner_b)
                pair_gain[pair] += gain_r
                if pair_gain[pair] > max_gain:
                    max_gain = pair_gain[pair]
        
        return total + max_gain