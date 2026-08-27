class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # Precompute prefix sums of absolute differences for each character
        # P[i][c] = sum(|caption[k] - c| for k in 0..i-1)
        # Dimensions: (n+1) x 26
        P = [[0] * 26 for _ in range(n + 1)]
        for i in range(n):
            char_code = ord(caption[i]) - ord('a')
            for c in range(26):
                P[i+1][c] = P[i][c] + abs(char_code - c)
        
        # dp[i] = minimum cost to make prefix caption[0:i] a good caption
        dp = [float('inf')] * (n + 1)
        dp[0] = 0
        
        # best_prev_val[c] stores min(dp[j] - P[j][c]) for valid j (where j <= i-3)
        # best_j_for_val[c] stores the j that achieved this minimum
        best_prev_val = [float('inf')] * 26
        best_j_for_val = [-1] * 26
        
        # Initialize for j=0 (valid for i >= 3)
        # P[0][c] is 0 for all c
        for c in range(26):
            best_prev_val[c] = dp[0] - P[0][c]
            best_j_for_val[c] = 0
        
        # To reconstruct the lexicographically smallest string, we store the best transition
        # best_prev[i] = (j, c) that yields dp[i]
        best_prev = [None] * (n + 1)
        
        for i in range(1, n + 1):
            # Update best_prev_val with dp[i-3] if i-3 >= 0
            # This makes j = i-3 available for the current state i (since segment length >= 3)
            if i - 3 >= 0:
                prev = i - 3
                for c in range(26):
                    val = dp[prev] - P[prev][c]
                    if val < best_prev_val[c]:
                        best_prev_val[c] = val
                        best_j_for_val[c] = prev
                    elif val == best_prev_val[c]:
                        # Tie in value: prefer smaller j
                        if prev < best_j_for_val[c]:
                            best_j_for_val[c] = prev
            
            # Compute dp[i]
            min_cost = float('inf')
            best_c = -1
            best_j = -1
            
            for c in range(26):
                j = best_j_for_val[c]
                if j == -1:
                    continue
                
                # Cost to transition from j to i with character c
                cost = best_prev_val[c] + P[i][c]
                
                if cost < min_cost:
                    min_cost = cost
                    best_c = c
                    best_j = j
                elif cost == min_cost:
                    # Tie-breaking:
                    # 1. Smaller character c is preferred (lexicographically smaller block)
                    if c < best_c:
                        best_c = c
                        best_j = j
                    elif c == best_c:
                        # 2. Smaller start index j is preferred
                        if j < best_j:
                            best_j = j
            
            dp[i] = min_cost
            if best_j != -1:
                best_prev[i] = (best_j, best_c)
            else:
                # If no valid transition found, dp[i] remains inf
                best_prev[i] = None
            
            if min_cost == float('inf'):
                return ""
        
        # Reconstruct the string
        if dp[n] == float('inf'):
            return ""
        
        res = []
        curr = n
        while curr > 0:
            prev_idx, char_code = best_prev[curr]
            char = chr(ord('a') + char_code)
            length = curr - prev_idx
            res.append(char * length)
            curr = prev_idx
        
        return "".join(reversed(res))