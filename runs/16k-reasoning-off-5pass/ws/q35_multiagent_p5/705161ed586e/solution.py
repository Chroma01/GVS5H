class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # Precompute prefix sums P[i][c] = sum of abs(s[k] - c) for k in 0..i-1
        # P[0][c] = 0
        # P[i][c] = P[i-1][c] + abs(ord(caption[i-1]) - ord(c))
        # We'll use a list of lists: P[i][c] where c is 0-25
        P = [[0] * 26 for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            char_idx = ord(caption[i-1]) - ord('a')
            for c in range(26):
                P[i][c] = P[i-1][c] + abs(char_idx - c)
        
        # dp[i] = min cost to make prefix s[0:i] a good caption
        INF = float('inf')
        dp = [INF] * (n + 1)
        dp[0] = 0
        
        # best[c] = min_{j <= i-3} (dp[j] - P[j][c])
        # best_j[c] = the j that achieved the minimum for best[c]
        best = [INF] * 26
        best_j = [-1] * 26
        
        # choice_c[i] and choice_j[i] store the character and start index of the last group for dp[i]
        choice_c = [-1] * (n + 1)
        choice_j = [-1] * (n + 1)
        
        for i in range(1, n + 1):
            # Before computing dp[i], if i >= 3, we can add j = i-3 to best
            if i >= 3:
                j = i - 3
                # Update best[c] with j
                for c in range(26):
                    val = dp[j] - P[j][c]
                    if val < best[c]:
                        best[c] = val
                        best_j[c] = j
            
            # Now compute dp[i] if i >= 3
            if i >= 3:
                min_cost = INF
                chosen_c = -1
                chosen_j = -1
                
                for c in range(26):
                    if best[c] == INF:
                        continue
                    cost = best[c] + P[i][c]
                    # We want minimum cost, and for ties, lexicographically smallest character
                    if cost < min_cost:
                        min_cost = cost
                        chosen_c = c
                        chosen_j = best_j[c]
                    elif cost == min_cost:
                        # Choose lexicographically smaller character
                        if c < chosen_c:
                            chosen_c = c
                            chosen_j = best_j[c]
                
                if min_cost < INF:
                    dp[i] = min_cost
                    choice_c[i] = chosen_c
                    choice_j[i] = chosen_j
        
        if dp[n] == INF:
            return ""
        
        # Reconstruct the result
        res = [''] * n
        i = n
        while i > 0:
            c = choice_c[i]
            j = choice_j[i]
            # The group is from j to i-1, all converted to character c
            char = chr(c + ord('a'))
            for k in range(j, i):
                res[k] = char
            i = j
        
        return ''.join(res)