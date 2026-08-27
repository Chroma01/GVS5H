class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        INF = float('inf')
        
        # dp[i][c][r] = min cost for prefix [0:i] ending with character c and run length r
        # c: 0-25, r: 1,2,3 where 3 means >=3
        dp = [[[INF] * 4 for _ in range(26)] for _ in range(n)]
        
        # Initialize for i=0
        for c in range(26):
            cost = abs(ord(caption[0]) - ord('a') - c)
            dp[0][c][1] = cost
            
        # Fill DP for i=1 to n-1
        for i in range(1, n):
            for prev_c in range(26):
                for prev_r in range(1, 4):
                    if dp[i-1][prev_c][prev_r] == INF:
                        continue
                    base_cost = dp[i-1][prev_c][prev_r]
                    
                    for curr_c in range(26):
                        cost_change = abs(ord(caption[i]) - ord('a') - curr_c)
                        new_cost = base_cost + cost_change
                        
                        if curr_c == prev_c:
                            new_r = min(prev_r + 1, 3)
                        else:
                            # Only allow transition if previous run was complete (>=3)
                            if prev_r < 3:
                                continue
                            new_r = 1
                        
                        if new_cost < dp[i][curr_c][new_r]:
                            dp[i][curr_c][new_r] = new_cost
        
        # Find minimum total cost at the end
        min_total = INF
        for c in range(26):
            if dp[n-1][c][3] < min_total:
                min_total = dp[n-1][c][3]
        
        if min_total == INF:
            return ""
        
        # Backward DP for suffix costs: min_suff[i][c][r] = min cost to complete from position i+1 to n-1
        # given that at position i, the character is c and run length is r.
        # For i = n-1, min_suff[n-1][c][r] = 0 if r == 3 else INF
        min_suff = [[[INF] * 4 for _ in range(26)] for _ in range(n)]
        
        for c in range(26):
            min_suff[n-1][c][3] = 0
            min_suff[n-1][c][1] = INF
            min_suff[n-1][c][2] = INF
            
        # For i from n-2 down to 0
        for i in range(n-2, -1, -1):
            for c in range(26):
                for r in range(1, 4):
                    # Try all next characters
                    for nc in range(26):
                        if c == nc:
                            new_r = min(r + 1, 3)
                        else:
                            if r < 3:
                                continue
                            new_r = 1
                        if min_suff[i+1][nc][new_r] != INF:
                            cost_change = abs(ord(caption[i+1]) - ord('a') - nc)
                            total = cost_change + min_suff[i+1][nc][new_r]
                            if total < min_suff[i][c][r]:
                                min_suff[i][c][r] = total
        
        # Now reconstruct greedily from left to right
        result = [''] * n
        prev_c = -1  # dummy
        prev_r = 0   # dummy
        acc_cost = 0
        
        for i in range(n):
            for c in range(26):
                # Determine new_r
                if i == 0:
                    new_r = 1
                else:
                    if c == prev_c:
                        new_r = min(prev_r + 1, 3)
                    else:
                        if prev_r < 3:
                            continue
                        new_r = 1
                
                cost_change = abs(ord(caption[i]) - ord('a') - c)
                total_cost_so_far = acc_cost + cost_change
                
                # Check if this state is on an optimal path:
                # 1. The DP cost for this state must match the accumulated cost
                # 2. The remaining cost (min_suff) must be achievable such that total == min_total
                remaining = min_suff[i][c][new_r]
                if dp[i][c][new_r] == total_cost_so_far and remaining != INF and total_cost_so_far + remaining == min_total:
                    result[i] = chr(ord('a') + c)
                    acc_cost = total_cost_so_far
                    prev_c = c
                    prev_r = new_r
                    break
        
        # Verify that the total cost is min_total
        if acc_cost != min_total:
            return ""
            
        return "".join(result)