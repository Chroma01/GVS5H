class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # dp[i][c] = minimum cost to complete the string from index i,
        # given that the FIRST group of the suffix starts at i with character c.
        # c is 0-25 representing 'a'-'z'.
        INF = float('inf')
        dp = [[INF] * 26 for _ in range(n + 1)]
        
        # Base case: at index n, the cost to complete is 0.
        for c in range(26):
            dp[n][c] = 0
            
        # Precompute best and second best characters for each index to optimize transitions
        best_c_min = [-1] * (n + 1)
        best_c_sec = [-1] * (n + 1)
        
        # Fill best/second best arrays backwards
        for k in range(n, -1, -1):
            candidates = []
            for c in range(26):
                if dp[k][c] != INF:
                    candidates.append((dp[k][c], c))
            
            if not candidates:
                continue
                
            # Sort by cost, then by character
            candidates.sort(key=lambda x: (x[0], x[1]))
            
            if len(candidates) >= 1:
                best_c_min[k] = candidates[0][1]
            if len(candidates) >= 2:
                best_c_sec[k] = candidates[1][1]
        
        # Fill DP table backwards
        for i in range(n - 1, -1, -1):
            next_states_info = {}
            for L in [3, 4, 5]:
                if i + L <= n:
                    idx = i + L
                    if idx not in next_states_info:
                        next_states_info[idx] = (best_c_min[idx], best_c_sec[idx])
            
            for c in range(26):
                min_val = INF
                
                for L in [3, 4, 5]:
                    if i + L > n:
                        continue
                    
                    idx = i + L
                    
                    # Calculate cost of current segment [i, i+L) converted to char c
                    seg_cost = 0
                    for k in range(L):
                        char_code = ord(caption[i+k]) - ord('a')
                        seg_cost += abs(char_code - c)
                    
                    # Find min cost from next state with char != c
                    b1_char, b2_char = next_states_info[idx]
                    
                    if b1_char != c:
                        cost_next = dp[idx][b1_char]
                    else:
                        cost_next = dp[idx][b2_char]
                    
                    if cost_next == INF:
                        continue
                        
                    total = seg_cost + cost_next
                    if total < min_val:
                        min_val = total
                
                dp[i][c] = min_val
        
        # Find global minimum cost at dp[0][c]
        global_min = INF
        for c in range(26):
            if dp[0][c] < global_min:
                global_min = dp[0][c]
        
        if global_min == INF:
            return ""
            
        # Reconstruct the lexicographically smallest string
        res = []
        curr = 0
        
        while curr < n:
            # 1. Find the smallest character 'c' that can start a group at 'curr'
            best_c = -1
            for c in range(26):
                if dp[curr][c] == global_min:
                    best_c = c
                    break
            
            if best_c == -1:
                break # Should not happen
            
            candidates = []
            for L in [3, 4, 5]:
                if curr + L > n:
                    continue
                
                # Calculate cost of this specific segment
                seg_cost = 0
                for k in range(L):
                    char_code = ord(caption[curr+k]) - ord('a')
                    seg_cost += abs(char_code - best_c)
                
                idx = curr + L
                
                # Determine cost of rest
                b1_char, b2_char = best_c_min[idx], best_c_sec[idx]
                
                if b1_char != best_c:
                    cost_next = dp[idx][b1_char]
                else:
                    cost_next = dp[idx][b2_char]
                
                if cost_next == INF:
                    continue
                
                if seg_cost + cost_next != global_min:
                    continue
                
                # Determine starting char of next group
                if idx == n:
                    next_c = 26 
                else:
                    if b1_char != best_c:
                        next_c = b1_char
                    else:
                        next_c = b2_char
                
                candidates.append((L, next_c))
            
            # Select best L
            best_L = -1
            for L, next_c in candidates:
                if next_c < best_c:
                    if best_L == -1 or L < best_L:
                        best_L = L
                elif next_c > best_c:
                    if best_L == -1 or L > best_L:
                        best_L = L
            
            res.append(best_c * best_L)
            curr += best_L
            
        return "".join(res)