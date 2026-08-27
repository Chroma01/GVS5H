from array import array

class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n == 0:
            return ""
        s = [ord(c) - ord('a') for c in caption]
        INF = 10**9
        # DP array: size (n+1) * 26 * 3
        size = (n + 1) * 26 * 3
        dp = array('i', [INF]) * size
        
        # Base case: i = n
        for c in range(26):
            idx = n * 78 + c * 3 + 2  # k=3
            dp[idx] = 0
        
        # Fill backward DP
        for i in range(n - 1, -1, -1):
            # Compute best[c] = |s[i] - c| + dp[i+1][c][1] for all c
            best = [0] * 26
            min1 = INF
            min2 = INF
            argmin = -1
            count = 0
            for c in range(26):
                idx_next = (i + 1) * 78 + c * 3 + 0  # k=1
                val = abs(s[i] - c) + dp[idx_next]
                best[c] = val
                if val < min1:
                    min2 = min1
                    min1 = val
                    argmin = c
                    count = 1
                elif val == min1:
                    count += 1
                elif val < min2:
                    min2 = val
            
            for c in range(26):
                cost_char = abs(s[i] - c)
                # k=1
                cont_run = 2  # min(1+1,3)=2
                cont = dp[(i + 1) * 78 + c * 3 + (cont_run - 1)]
                new = INF
                dp_idx = i * 78 + c * 3 + 0
                dp[dp_idx] = cost_char + min(cont, new)
                # k=2
                cont_run = 3
                cont = dp[(i + 1) * 78 + c * 3 + (cont_run - 1)]
                new = INF
                dp_idx = i * 78 + c * 3 + 1
                dp[dp_idx] = cost_char + min(cont, new)
                # k=3
                cont_run = 3
                cont = dp[(i + 1) * 78 + c * 3 + (cont_run - 1)]
                new = INF
                if min1 < INF:
                    if count > 1:
                        new = min1
                    else:  # count == 1
                        if c != argmin:
                            new = min1
                        else:
                            new = min2
                dp_idx = i * 78 + c * 3 + 2
                dp[dp_idx] = cost_char + min(cont, new)
        
        # Compute global minimum cost: min over first character c of (|s[0]-c| + dp[1][c][1])
        global_min = INF
        for c in range(26):
            cost = abs(s[0] - c) + dp[1 * 78 + c * 3 + 0]
            if cost < global_min:
                global_min = cost
        
        if global_min >= INF:
            return ""
        
        # Reconstruct the lexicographically smallest string with minimum cost
        result = []
        current_cost = 0
        prev_c = 0
        prev_k = 0
        for i in range(n):
            found = False
            for c in range(26):
                if i == 0:
                    new_k = 1
                else:
                    if c == prev_c:
                        new_k = min(prev_k + 1, 3)
                    elif prev_k == 3:
                        new_k = 1
                    else:
                        continue
                # Remaining cost from i+1 onward given state (c, new_k) at position i+1
                if i + 1 <= n:
                    remaining = dp[(i + 1) * 78 + c * 3 + (new_k - 1)]
                else:
                    remaining = 0
                if current_cost + abs(s[i] - c) + remaining == global_min:
                    result.append(chr(c + ord('a')))
                    current_cost += abs(s[i] - c)
                    prev_c = c
                    prev_k = new_k
                    found = True
                    break
            if not found:
                return ""  # Should not happen
        return ''.join(result)