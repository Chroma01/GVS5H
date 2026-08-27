class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        # Precompute prefix counts for each character
        # prefix[i][c] = count of char c in caption[0:i]
        prefix = [[0] * 26 for _ in range(n + 1)]
        for i in range(n):
            for c in range(26):
                prefix[i + 1][c] = prefix[i][c]
            prefix[i + 1][ord(caption[i]) - ord('a')] += 1
        
        # dp[i] = (min_cost, best_string) for prefix caption[0:i]
        # Initialize with infinity
        INF = float('inf')
        dp = [(INF, "")] * (n + 1)
        dp[0] = (0, "")
        
        # For each position i, try all group lengths L >= 3
        for i in range(n):
            if dp[i][0] == INF:
                continue
            # Try group lengths from 3 to n - i
            for L in range(3, n - i + 1):
                j = i + L
                # Compute cost and target char for caption[i:j]
                # Get frequency of each char in caption[i:j]
                freq = [0] * 26
                for c in range(26):
                    freq[c] = prefix[j][c] - prefix[i][c]
                
                # Find the lower median (to minimize cost and be lexicographically smallest)
                total = L
                cum = 0
                target = -1
                for c in range(26):
                    cum += freq[c]
                    if cum >= (total + 1) // 2:
                        target = c
                        break
                
                # Compute cost
                cost = 0
                for c in range(26):
                    if freq[c] > 0:
                        cost += freq[c] * abs(c - target)
                
                new_cost = dp[i][0] + cost
                new_string = dp[i][1] + chr(target + ord('a')) * L
                
                # Update dp[j]
                if new_cost < dp[j][0] or (new_cost == dp[j][0] and new_string < dp[j][1]):
                    dp[j] = (new_cost, new_string)
        
        if dp[n][0] == INF:
            return ""
        return dp[n][1]