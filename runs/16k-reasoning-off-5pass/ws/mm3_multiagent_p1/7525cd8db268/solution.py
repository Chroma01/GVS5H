from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Build adjacency: for each endpoint b (the larger index), store the smaller index a
        # We will store pairs as (a, b) with a < b
        pairs_by_end = [[] for _ in range(n + 1)]
        for a, b in conflictingPairs:
            if a > b:
                a, b = b, a
            pairs_by_end[b].append(a)
        
        # Sweep from 1 to n
        # max1: largest a seen so far
        # max2: second largest a seen so far
        # cnt_max1: how many times max1 appears as the dominant constraint (for tie-breaking)
        max1 = 0
        max2 = 0
        cnt_max1 = 0
        
        base = 0  # total valid subarrays without removing any pair
        gain = [0] * (n + 1)  # gain[a] accumulates (max1 - max2) for positions where max1 == a
        
        for i in range(1, n + 1):
            # Update max1, max2 with all pairs ending at i
            for a in pairs_by_end[i]:
                if a > max1:
                    max2 = max1
                    max1 = a
                    cnt_max1 = 1
                elif a == max1:
                    cnt_max1 += 1
                elif a > max2:
                    max2 = a
            
            # Number of valid subarrays ending at i
            base += i - max1
            
            # Gain if we remove the pair that currently gives max1
            # If there are multiple pairs with the same max1, removing one of them
            # still leaves another with the same max1, so gain is 0.
            if cnt_max1 == 1:
                gain[max1] += max1 - max2
        
        # Compute prefix sums of gain to get total gain for removing a pair with a = max1
        # The gain for removing a pair (a, b) where a is the dominant constraint for a range
        # is the sum of gain[a] over that range.
        max_gain = 0
        current = 0
        for a in range(1, n + 1):
            current += gain[a]
            if current > max_gain:
                max_gain = current
        
        return base + max_gain