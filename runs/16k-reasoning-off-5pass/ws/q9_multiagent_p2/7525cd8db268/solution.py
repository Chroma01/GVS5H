from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Normalize pairs: ensure a < b
        pairs = []
        for a, b in conflictingPairs:
            if a > b:
                a, b = b, a
            pairs.append((a, b))
        
        # Group pairs by 'a'
        pairs_by_a = [[] for _ in range(n + 1)]
        for a, b in pairs:
            pairs_by_a[a].append(b)
            
        INF = n + 1
        min_b = [INF] * (n + 2)
        count_min = [0] * (n + 2)
        second_min = [INF] * (n + 2)
        total_pairs = [0] * (n + 2)
        
        current_min = INF
        current_count = 0
        current_second = INF
        current_total = 0
        
        # Fill suffix arrays from n down to 1
        for L in range(n, 0, -1):
            for b in pairs_by_a[L]:
                current_total += 1
                if b < current_min:
                    current_second = current_min
                    current_min = b
                    current_count = 1
                elif b == current_min:
                    current_count += 1
                elif b < current_second:
                    current_second = b
            
            min_b[L] = current_min
            count_min[L] = current_count
            second_min[L] = current_second
            total_pairs[L] = current_total
            
        # Calculate base valid subarrays count
        base_count = 0
        for L in range(1, n + 1):
            limit = min_b[L]
            if limit > L:
                base_count += (limit - L)
                
        # Precompute prefix sums of second_min
        P2 = [0] * (n + 1)
        current_sum = 0
        for i in range(1, n + 1):
            current_sum += second_min[i]
            P2[i] = current_sum
            
        # Identify ranges [L_start, L_end] where min_b[L] == v and count_min[L] == 1
        ranges_map = {}
        i = 1
        while i <= n:
            j = i
            while j <= n and min_b[j] == min_b[i]:
                j += 1
            # Range [i, j-1] has min_b = v
            v = min_b[i]
            # Find the first index in [i, j-1] where count_min == 1
            start_valid = -1
            for k in range(i, j):
                if count_min[k] == 1:
                    start_valid = k
                    break
            if start_valid != -1:
                ranges_map[v] = (start_valid, j - 1)
            i = j
            
        max_gain = 0
        for a, b in pairs:
            if b in ranges_map:
                L_start, L_end = ranges_map[b]
                # We need sum_{L=L_start}^{min(L_end, a)} (second_min[L] - b)
                limit = min(L_end, a)
                if limit >= L_start:
                    term = (P2[limit] - P2[L_start-1]) - b * (limit - L_start + 1)
                    if term > max_gain:
                        max_gain = term
        
        return base_count + max_gain