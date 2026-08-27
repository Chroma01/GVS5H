class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # Precompute prefix frequency array
        # pref[i][c] = count of character c in caption[0:i]
        pref = [[0] * 26 for _ in range(n + 1)]
        for i in range(1, n + 1):
            for c in range(26):
                pref[i][c] = pref[i-1][c]
            idx = ord(caption[i-1]) - ord('a')
            pref[i][idx] += 1
        
        # dp[i] = (min_cost, best_string) for prefix of length i
        # Use a large number for infinity
        INF = float('inf')
        dp = [(INF, None)] * (n + 1)
        dp[0] = (0, "")
        
        # For each position i from 1 to n
        for i in range(1, n + 1):
            # Try all possible last group lengths L from 3 to i
            for L in range(3, i + 1):
                j = i - L
                # If dp[j] is not reachable, skip
                if dp[j][0] == INF:
                    continue
                
                # Get frequency counts for segment caption[j:i]
                # freq[c] = pref[i][c] - pref[j][c]
                # We'll compute the cost for each character 'a' to 'z'
                # Using the incremental method for F(c) = sum_{d} freq[d] * |d - c|
                
                # First, get the frequency array for the segment
                freq = [0] * 26
                for c in range(26):
                    freq[c] = pref[i][c] - pref[j][c]
                
                total_freq = L  # which is i - j
                
                # Compute F[0] = sum_{d} freq[d] * d
                F0 = 0
                for d in range(26):
                    F0 += freq[d] * d
                
                # Now compute F[c] for c from 1 to 25
                # F[c] = F[c-1] + cum_c - (total_freq - cum_c)
                # where cum_c = sum_{d=0}^{c-1} freq[d]
                
                min_cost_seg = F0
                best_char_idx = 0
                
                cum_c = freq[0]  # cum_c for c=1 is freq[0]
                F_prev = F0
                for c in range(1, 26):
                    # F[c] = F[c-1] + cum_c - (total_freq - cum_c)
                    F_curr = F_prev + cum_c - (total_freq - cum_c)
                    if F_curr < min_cost_seg:
                        min_cost_seg = F_curr
                        best_char_idx = c
                    # Update cum_c for next iteration (which will be for c+1)
                    cum_c += freq[c]
                    F_prev = F_curr
                
                best_char = chr(ord('a') + best_char_idx)
                total_cost = dp[j][0] + min_cost_seg
                candidate_string = dp[j][1] + (best_char * L)
                
                # Update dp[i] if this candidate is better
                if total_cost < dp[i][0] or (total_cost == dp[i][0] and candidate_string < dp[i][1]):
                    dp[i] = (total_cost, candidate_string)
        
        if dp[n][1] is None:
            return ""
        return dp[n][1]