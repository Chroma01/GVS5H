from typing import List

class Solution:
    def maxSubarrays(self, n: int, conflictingPairs: List[List[int]]) -> int:
        # Group pairs by their starting element u (where u = min(a, b))
        # pairs_by_u[u] will store a list of v's such that (u, v) is a conflicting pair
        pairs_by_u = [[] for _ in range(n + 1)]
        
        for a, b in conflictingPairs:
            u, v = (a, b) if a < b else (b, a)
            pairs_by_u[u].append(v)
        
        # Sort each list to easily get min and second min
        for i in range(n + 1):
            pairs_by_u[i].sort()
        
        # m1[L] = min v among all pairs with u >= L
        # m2[L] = second min v among all pairs with u >= L
        # We use n + 1 to represent "no constraint" (infinity)
        INF = n + 1
        m1 = [INF] * (n + 2)
        m2 = [INF] * (n + 2)
        
        # Compute m1 and m2 from n down to 1
        for L in range(n, 0, -1):
            vals = pairs_by_u[L]
            if vals:
                v1 = vals[0]
                v2 = vals[1] if len(vals) > 1 else INF
                m1[L] = min(m1[L+1], v1)
                m2[L] = min(m2[L+1], v2)
            else:
                m1[L] = m1[L+1]
                m2[L] = m2[L+1]
        
        # Precompute prefix sums of max(0, m2[L] - L)
        # prefix_sum_m2[i] = sum_{j=1}^{i} max(0, m2[j] - j)
        prefix_sum_m2 = [0] * (n + 2)
        for L in range(1, n + 1):
            term = max(0, m2[L] - L)
            prefix_sum_m2[L] = prefix_sum_m2[L-1] + term
        
        # Calculate original total valid subarrays
        original_total = 0
        for L in range(1, n + 1):
            term = max(0, m1[L] - L)
            original_total += term
        
        max_subarrays = original_total
        
        # Helper to compute sum_{L=a}^{b} max(0, v - L)
        def sum_max_v(a: int, b: int, v: int) -> int:
            if a > b:
                return 0
            limit = min(b, v)
            if limit < a:
                return 0
            count = limit - a + 1
            # Sum of (v - L) for L from a to limit
            # = count * v - sum(L for L in a..limit)
            # sum(L) = count * a + count*(count-1)/2
            return count * v - (count * a + count * (count - 1) // 2)
        
        # Precompute max_u_less[v] = max { u' | exists pair (u', v') with v' < v }
        # This helps determine the range of L where a specific pair (u, v) is the unique minimum
        max_u_less = [0] * (n + 2)
        max_u_less[1] = 0
        for v in range(2, n + 2):
            prev_max = max_u_less[v-1]
            if pairs_by_u[v-1]: # Check if there are pairs starting at v-1? No, we need pairs ending at v-1.
                # Wait, the logic for max_u_less needs to be based on pairs where the second element is v-1.
                # But we only stored pairs by u. We need to re-group or access differently.
                # Actually, we can just iterate through all pairs again or build a separate structure.
                # Let's rebuild pairs_by_v for clarity and correctness.
                pass
            # Re-implementation of max_u_less logic below
        
        # Re-group pairs by v to correctly compute max_u_less
        pairs_by_v = [[] for _ in range(n + 2)]
        for a, b in conflictingPairs:
            u, v = (a, b) if a < b else (b, a)
            pairs_by_v[v].append(u)
        
        # Recompute max_u_less correctly
        max_u_less = [0] * (n + 2)
        current_max_u = 0
        for v in range(1, n + 2):
            if pairs_by_v[v]:
                current_max_u = max(current_max_u, max(pairs_by_v[v]))
            max_u_less[v] = current_max_u
        
        # Iterate over each pair to calculate the delta if removed
        for a, b in conflictingPairs:
            u, v = (a, b) if a < b else (b, a)
            
            # The pair (u, v) is the unique minimum for L in range [L_start, u]
            # where L_start = max_u_less[v] + 1
            L_start = max_u_less[v] + 1
            L_end = u
            
            if L_start > L_end:
                delta = 0
            else:
                # Sum of max(0, m2[L] - L) for L in [L_start, L_end]
                sum_m2 = prefix_sum_m2[L_end] - prefix_sum_m2[L_start - 1]
                # Sum of max(0, v - L) for L in [L_start, L_end]
                sum_v = sum_max_v(L_start, L_end, v)
                delta = sum_m2 - sum_v
            
            current_total = original_total + delta
            if current_total > max_subarrays:
                max_subarrays = current_total
        
        return max_subarrays