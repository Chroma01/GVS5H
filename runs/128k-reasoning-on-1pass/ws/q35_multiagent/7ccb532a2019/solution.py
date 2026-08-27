class Solution:
    def makeStringGood(self, s: str) -> int:
        from collections import Counter
        
        n = len(s)
        min_ops = n
        
        char_counts = [0] * 26
        for ch in s:
            char_counts[ord(ch) - ord('a')] += 1
            
        for k in range(1, n + 1):
            if k > min_ops:
                break
                
            dp = [0] + [float('inf')] * k
            for c in char_counts:
                new_dp = [float('inf')] * (k + 1)
                
                suf0 = [float('inf')] * (k + 2)
                suf1 = [float('inf')] * (k + 2)
                suf2 = [float('inf')] * (k + 2)
                
                for j in range(k, -1, -1):
                    if dp[j] != float('inf'):
                        suf0[j] = min(suf0[j+1], dp[j] + c + j)
                        if c + j >= k:
                            suf1[j] = min(suf1[j+1], dp[j] + c + j - k)
                        suf2[j] = min(suf2[j+1], dp[j] - j)
                        
                min_dp_minus_j = [float('inf')] * (k + 1)
                curr_min = float('inf')
                for j in range(k + 1):
                    if dp[j] != float('inf'):
                        curr_min = min(curr_min, dp[j] - j)
                    min_dp_minus_j[j] = curr_min
                    
                for y in range(k + 1):
                    idx0 = max(0, y - c)
                    cost0 = suf0[idx0]
                    
                    if y == 0:
                        limit = k - c - 1
                        min_val2 = min_dp_minus_j[limit] if limit >= 0 else float('inf')
                        cost_k_y0 = min(cost0, min_val2 + k - c)
                        cost_k_y0 = min(cost_k_y0, suf1[0])
                        new_dp[0] = cost_k_y0
                    else:
                        idx1 = max(0, y + c - k)
                        cost_k = suf1[idx1]
                        new_dp[y] = min(cost0, cost_k)
                        
                dp = new_dp
                
            current_ans = min(dp[j] + j for j in range(k + 1))
            min_ops = min(min_ops, current_ans)
            
        return min_ops