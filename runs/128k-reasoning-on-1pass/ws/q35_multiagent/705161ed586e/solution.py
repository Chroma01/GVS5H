import sys

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # Precompute prefix counts for O(1) range count queries
        # pref[i][c] = count of char c in caption[:i]
        pref = [[0] * 26 for _ in range(n + 1)]
        for i in range(n):
            pref[i+1] = pref[i][:]
            pref[i+1][ord(caption[i]) - 97] += 1
            
        # Precompute block info: for each start index i and length L in {3,4,5}
        # store (min_cost, list_of_optimal_chars)
        block_info = [[None] * 3 for _ in range(n)]
        for i in range(n):
            for L_idx, L in enumerate([3, 4, 5]):
                if i + L <= n:
                    counts = [pref[i+L][c] - pref[i][c] for c in range(26)]
                    min_cost = float('inf')
                    best_chars = []
                    for c in range(26):
                        cost = 0
                        for k in range(26):
                            cost += counts[k] * abs(k - c)
                        if cost < min_cost:
                            min_cost = cost
                            best_chars = [c]
                        elif cost == min_cost:
                            best_chars.append(c)
                    block_info[i][L_idx] = (min_cost, best_chars)
                    
        # DP to find minimum operations
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        for i in range(1, n + 1):
            for L_idx, L in enumerate([3, 4, 5]):
                if i - L >= 0:
                    cost, _ = block_info[i - L][L_idx]
                    if dp[i - L] + cost < dp[i]:
                        dp[i] = dp[i - L] + cost
                        
        if dp[n] == float('inf'):
            return ""
            
        # Store best choice for each position to reconstruct lexicographically smallest result
        # best_choice[i] = (L, c)
        best_choice = [None] * (n + 1)
        
        # Helper to compare two candidates at position i
        # Returns True if (L1, c1) yields a lexicographically smaller string than (L2, c2)
        def is_better(i, L1, c1, L2, c2):
            # Compare character by character
            idx1, idx2 = i, i
            len1, len2 = L1, L2
            while True:
                # Get current character from candidate 1
                if len1 > 0:
                    char1 = c1
                    len1 -= 1
                else:
                    # Move to next block
                    if best_choice[idx1] is None:
                        char1 = 255 # Should not happen if dp is valid
                    else:
                        nl, nc = best_choice[idx1]
                        idx1 += nl
                        len1 = nl - 1
                        char1 = nc
                        
                # Get current character from candidate 2
                if len2 > 0:
                    char2 = c2
                    len2 -= 1
                else:
                    if best_choice[idx2] is None:
                        char2 = 255
                    else:
                        nl, nc = best_choice[idx2]
                        idx2 += nl
                        len2 = nl - 1
                        char2 = nc
                        
                if char1 < char2:
                    return True
                if char1 > char2:
                    return False
                # If equal, continue to next character
                # Safety break to avoid infinite loops in case of bugs
                if idx1 >= n and idx2 >= n:
                    return False
                    
        # Process from right to left to determine best choices
        for i in range(n - 1, -1, -1):
            if dp[i] == float('inf'):
                continue
                
            best_L, best_c = None, None
            
            for L_idx, L in enumerate([3, 4, 5]):
                if i + L <= n:
                    cost, chars = block_info[i][L_idx]
                    if dp[i + L] != float('inf') and dp[i] == dp[i + L] + cost:
                        for c in chars:
                            if best_L is None or is_better(i, L, c, best_L, best_c):
                                best_L, best_c = L, c
                                
            best_choice[i] = (best_L, best_c)
            
        # Reconstruct the result
        res = []
        i = 0
        while i < n:
            L, c = best_choice[i]
            res.append(chr(c + 97) * L)
            i += L
            
        return "".join(res)