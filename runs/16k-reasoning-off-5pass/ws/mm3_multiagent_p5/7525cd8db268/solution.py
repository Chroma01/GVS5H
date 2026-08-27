from typing import List
import sys

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # For each left index, keep the two largest right endpoints of conflicting pairs.
        # top1[i] = largest right index of a conflict starting at i (or some pair where min is i)
        # top2[i] = second largest.
        # We also want to aggregate gain for each conflict (a,b) where a < b.
        
        top1 = [0] * (n + 2)
        top2 = [0] * (n + 2)
        # For each right endpoint, track which left endpoint it came from (for gain aggregation)
        # We'll use arrays to accumulate gain per conflict's right endpoint.
        # Actually, the standard approach: for each i, when we update top1 and top2,
        # we track the "left" value (max top1) and "second_left" (second max).
        # When we add a new pair, we update gain for the pair that just got demoted.
        
        # We'll store conflicts as (a, b) with a < b.
        # For each i, we need to know which conflict contributed the top1.
        # We'll maintain gain_per_pair: dict mapping pair id -> extra subarrays gained by removing it.
        
        # Approach:
        # - Build a list of conflicts per left index.
        # - When processing i from 1 to n:
        #   - We have a current "left" = max of top1[1..i-1] and "second_left" = second max.
        #   - We also have a "extra" = left - second_left (the gap, i.e., how many extra subarrays
        #     are blocked solely by the top conflict).
        #   - For each conflict (a, b) where a == i, we update top1[i], top2[i].
        #   - We add conflicts starting at i to the candidate set and find the new top1, top2.
        #   - If the new top1 is larger than current left, we shift: second_left = left, left = new_top1.
        #   - Then for this i, number of valid subarrays ending at i is i - left.
        #   - Also, for the conflict that contributed to top1[i] (the one giving the new left),
        #     if top2[i] (or previous second_left) is less than a (the left index of that conflict),
        #     then removing that conflict would add (b - a) subarrays for this i.
        #     We accumulate this gain.
        
        # Implementation details:
        # - conflicts_by_left[a] = list of (b, pair_id) where a < b.
        # - We'll process i from 1 to n.
        # - Maintain: left (int), second_left (int), left_pair_id (int, id of conflict giving left).
        # - Actually, left is just the max right endpoint, and we need the pair id of that max
        #   to know which a it belongs to. Since the max right endpoint b comes from a conflict
        #   (a, b) where a is the left index, and we process in order, the "a" of the max conflict
        #   is the left index where it was registered.
        # - When we add conflicts at position i (i.e., pairs (i, b)), we check if b > left.
        #   If so, second_left = left, left = b, and we record the new pair id.
        #   Else if b > second_left, second_left = b.
        # - For gain: for the conflict that is currently the top (left_pair_id, which corresponds to (a, b)),
        #   if second_left < a, then removing this pair would reduce the left bound from b to
        #   max(second_left, a-1)? Wait, let's think carefully.
        
        # Standard LeetCode 3480 solution:
        # - For each i, we have top1[i] and top2[i] (two largest right endpoints among conflicts
        #   with left <= i). We maintain left = max(top1[1..i]) and second_left = second max.
        # - base += i - left.
        # - For each conflict (a, b) where a < b: if top1[b] == b and top2[b] < a, then
        #   gain for this conflict += b - a.
        #   This is computed by noting that for all i >= b, if the top conflict is (a, b) and
        #   the second is less than a, then removing (a, b) allows subarrays starting at a..b-1
        #   ending at any i >= b, so we get b - a extra subarrays per such i... wait, no.
        #   Actually, the gain is: for each i where top1[i] == b and top2[i] < a, removing
        #   (a, b) increases valid subarrays ending at i by (b - a). Because currently
        #   left = b, so valid starts are 1..i-b, count = i - b. After removal, left becomes
        #   max(top2[i], a-1) = a - 1 (since top2[i] < a), so valid starts = 1..i-(a-1),
        #   count = i - a + 1. Gain = (i - a + 1) - (i - b) = b - a.
        #   So yes, for each such i, we add b - a to the gain of pair (a, b).
        #   But we need to aggregate over all i, so total gain for (a, b) is
        #   (b - a) * count_of_i_where_top1[i]==b_and_top2[i]<a.
        
        # Efficient way: when we sweep, for each i, we know left and second_left.
        # The conflict giving "left" is some (a, b) with b = left.
        # If second_left < a, then gain[left_pair_id] += b - a = left - a.
        # So we can accumulate gain online.
        
        # Let's implement this.
        
        # Step 1: Normalize pairs (a < b) and build conflicts_by_left.
        # Also, if a pair is (a, b) and a > b, swap.
        # Store pair_id for each original pair (0-indexed).
        # Build conflicts_by_left[a] = list of (b, pair_id).
        
        conflicts_by_left = [[] for _ in range(n + 2)]
        pair_id = 0
        for p in conflictingPairs:
            a, b = p[0], p[1]
            if a > b:
                a, b = b, a
            # a < b guaranteed now (since a != b per constraints)
            conflicts_by_left[a].append((b, pair_id))
            pair_id += 1
        
        m = len(conflictingPairs)
        gain = [0] * m
        
        left = 0          # current max right endpoint
        second_left = 0   # second max right endpoint
        # We need to know the "a" (left index) of the pair that gave us the current "left".
        # We'll track "left_a" = the left index of the conflict that is currently the top.
        left_a = 0
        left_pair_id = -1
        
        base = 0
        
        for i in range(1, n + 1):
            # Incorporate all conflicts starting at i.
            for b, pid in conflicts_by_left[i]:
                if b > left:
                    # New top. The old top becomes second.
                    # Gain for old top pair: if second_left (before update) < old left_a,
                    # then removing old pair gives (old left - old left_a) extra.
                    # But careful: the old left is about to become second_left.
                    # The condition is: the new second_left (which is old left) < old left_a?
                    # No. The gain is computed for the pair that is currently the top, based on
                    # the current second_left. So after we update left and second_left,
                    # we should compute gain for the new top pair using the new second_left.
                    
                    # Actually, let's think: after processing all conflicts at i, we have new
                    # left and second_left. Then for the pair that is now the top (left),
                    # if second_left < left_a (where left_a is the 'a' of that top pair),
                    # then gain[pid_of_top] += left - left_a.
                    
                    # But we need to do this for each i. So let's first update left/second_left
                    # by processing all conflicts at i, then compute gain for the new top.
                    
                    # Wait, the order matters. We should process conflicts at i, update
                    # left and second_left, then compute gain.
                    
                    # Let's do: for each conflict (b, pid) at i:
                    #   if b > left: second_left = left; left = b; left_a = i; left_pair_id = pid;
                    #   elif b > second_left: second_left = b
                    
                    # After this loop over conflicts at i, we have the correct left and
                    # second_left for position i (considering all conflicts with left <= i).
                    # Then we compute gain for the current top pair.
                    
                    second_left = left
                    left = b
                    left_a = i
                    left_pair_id = pid
                elif b > second_left:
                    second_left = b
            
            # Now, for position i, valid subarrays ending at i: starts must be > left,
            # so number of valid starts is i - left (starts from left+1 to i).
            base += i - left
            
            # Compute gain for the current top pair.
            # The top pair is (left_a, left). If second_left < left_a,
            # then removing this pair reduces the left bound to left_a - 1,
            # gaining (left - left_a) subarrays for this endpoint i.
            if second_left < left_a and left_pair_id != -1:
                gain[left_pair_id] += left - left_a
        
        # The answer is base + max gain.
        max_gain = 0
        if m > 0:
            max_gain = max(gain)
        
        return base + max_gain