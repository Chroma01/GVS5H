from array import array
from typing import List

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        INF = 10**9
        ord_a = ord('a')
        
        # Precompute original character values for each position
        orig = [ord(ch) - ord_a for ch in caption]
        
        # ---------- Forward DP (left-to-right) ----------
        # prev[c*3 + (k-1)] = minimal cost to process first i characters
        # ending with character c and current run length k (1,2,3)
        prev = [INF] * 78
        for c in range(26):
            prev[c * 3 + 0] = abs(orig[0] - c)  # k = 1
        
        for i in range(1, n):
            # Precompute smallest and second smallest values for k=3 (change transition)
            min1 = INF
            min1_idx = -1
            min2 = INF
            for c in range(26):
                val = prev[c * 3 + 2]  # k = 3
                if val < min1:
                    min2 = min1
                    min1 = val
                    min1_idx = c
                elif val < min2:
                    min2 = val
            
            curr = [INF] * 78
            for c2 in range(26):
                cost_c2 = abs(orig[i] - c2)
                # Stay transitions (continue current block)
                # from k = 1 to k = 2
                val = prev[c2 * 3 + 0]
                if val < INF:
                    curr[c2 * 3 + 1] = min(curr[c2 * 3 + 1], val + cost_c2)
                # from k = 2 to k = 3
                val = prev[c2 * 3 + 1]
                if val < INF:
                    curr[c2 * 3 + 2] = min(curr[c2 * 3 + 2], val + cost_c2)
                # from k = 3 to k = 3 (stay)
                val = prev[c2 * 3 + 2]
                if val < INF:
                    curr[c2 * 3 + 2] = min(curr[c2 * 3 + 2], val + cost_c2)
                
                # Change transition: start a new block with a different character
                # Only possible if previous block had length >= 3 (k=3)
                if c2 == min1_idx:
                    min_change = min2
                else:
                    min_change = min1
                if min_change < INF:
                    curr[c2 * 3 + 0] = min(curr[c2 * 3 + 0], min_change + cost_c2)
            
            prev = curr
        
        # Total minimal cost: any character ending with a block of length 3
        total_cost = min(prev[c * 3 + 2] for c in range(26))
        if total_cost >= INF:
            return ""  # should not happen for n >= 3
        
        # ---------- Backward DP (suffix) ----------
        # suf[i][c*3 + (k-1)] = minimal cost to convert suffix i..n-1
        # given that position i already has character c and current run length is k
        suf = [None] * n
        
        # Base case: i = n-1 (last character), must end with length 3
        row = array('i', [INF] * 78)
        for c in range(26):
            row[c * 3 + 2] = abs(orig[n - 1] - c)  # k = 3
        suf[n - 1] = row
        
        for i in range(n - 2, -1, -1):
            row_next = suf[i + 1]
            
            # Precompute min1 and min2 for k=1 of row_next (needed for change transition)
            min1 = INF
            min1_idx = -1
            min2 = INF
            for c in range(26):
                val = row_next[c * 3 + 0]  # k = 1
                if val < min1:
                    min2 = min1
                    min1 = val
                    min1_idx = c
                elif val < min2:
                    min2 = val
            
            row = array('i', [INF] * 78)
            for c in range(26):
                cost_c = abs(orig[i] - c)
                # k = 1: must continue (cannot end block yet)
                stay1 = row_next[c * 3 + 1]  # k = 2 at i+1
                row[c * 3 + 0] = cost_c + stay1
                # k = 2: must continue
                stay2 = row_next[c * 3 + 2]  # k = 3 at i+1
                row[c * 3 + 1] = cost_c + stay2
                # k = 3: stay (continue) or start a new block with different character
                stay3 = row_next[c * 3 + 2]  # stay
                if c == min1_idx:
                    min_change = min2
                else:
                    min_change = min1
                best3 = stay3 if stay3 <= min_change else min_change
                row[c * 3 + 2] = cost_c + best3
            
            suf[i] = row
        
        # ---------- Reconstruction (left-to-right) for lexicographically smallest optimal caption ----------
        res = [''] * n
        
        # Choose the smallest first character that can start an optimal solution
        for c in range(26):
            if suf[0][c * 3 + 0] == total_cost:  # k = 1
                cur_char = c
                cur_k = 1
                res[0] = chr(ord_a + c)
                prefix_cost = abs(orig[0] - c)
                break
        
        for i in range(1, n):
            row = suf[i]
            found = False
            for c2 in range(26):
                if c2 == cur_char:
                    # Continue current block
                    k2 = cur_k + 1
                    if k2 > 3:
                        k2 = 3
                    if prefix_cost + row[c2 * 3 + (k2 - 1)] == total_cost:
                        res[i] = chr(ord_a + c2)
                        prefix_cost += abs(orig[i] - c2)
                        cur_char = c2
                        cur_k = k2
                        found = True
                        break
                else:
                    # Start a new block – only allowed if previous block has length >= 3
                    if cur_k != 3:
                        continue
                    if prefix_cost + row[c2 * 3 + 0] == total_cost:  # k = 1
                        res[i] = chr(ord_a + c2)
                        prefix_cost += abs(orig[i] - c2)
                        cur_char = c2
                        cur_k = 1
                        found = True
                        break
            # The DP guarantees a solution exists
        
        return ''.join(res)