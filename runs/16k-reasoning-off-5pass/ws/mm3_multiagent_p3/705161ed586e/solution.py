class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # Precompute prefix sums of absolute differences for each character
        # prefAbs[i+1][c] = sum_{k=0}^{i} |caption[k] - c|
        prefAbs = [[0] * 26 for _ in range(n + 1)]
        for i, ch in enumerate(caption):
            val = ord(ch) - ord('a')
            for c in range(26):
                prefAbs[i + 1][c] = prefAbs[i][c] + abs(val - c)
        
        INF = 10**18
        dp = [INF] * n
        choice_c = [0] * n  # chosen character for segment ending at i
        choice_j = [0] * n  # previous index (start of segment - 1)
        
        # Pool for each character: best value dp[j] - prefAbs[j+1][c] and corresponding j
        bestVal = [0] * 26  # initially for j = -1, dp[-1]=0, prefAbs[0][c]=0
        bestJ = [-1] * 26
        
        for i in range(n):
            if i >= 2:
                # Compute dp[i] using current pool
                for c in range(26):
                    # Check if the candidate j is valid (segment length >= 3)
                    if i - bestJ[c] >= 3:
                        candidate = prefAbs[i + 1][c] + bestVal[c]
                        if candidate < dp[i]:
                            dp[i] = candidate
                            choice_c[i] = c
                            choice_j[i] = bestJ[c]
                        elif candidate == dp[i]:
                            # Tie-breaking: smaller character first, then larger j (shorter segment)
                            if c < choice_c[i] or (c == choice_c[i] and bestJ[c] > choice_j[i]):
                                choice_c[i] = c
                                choice_j[i] = bestJ[c]
            
            # Update pool with j = i for future use, if dp[i] is finite
            if dp[i] < INF:
                for c in range(26):
                    new_val = dp[i] - prefAbs[i + 1][c]
                    if new_val < bestVal[c]:
                        bestVal[c] = new_val
                        bestJ[c] = i
                    elif new_val == bestVal[c] and i > bestJ[c]:
                        # Keep larger j (shorter segment) for tie-breaking
                        bestJ[c] = i
        
        if dp[n - 1] >= INF:
            return ""
        
        # Reconstruct the string
        result = []
        i = n - 1
        while i >= 0:
            c = choice_c[i]
            j = choice_j[i]
            length = i - j
            result.append(chr(ord('a') + c) * length)
            i = j
        
        return ''.join(reversed(result))