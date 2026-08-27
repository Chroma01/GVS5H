class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        
        INF = float('inf')
        ans = n  # delete all characters gives a valid good string (empty)
        
        for k in range(0, n + 1):
            # Precompute node costs
            C0 = [0] * 26
            C1 = [0] * 26
            for i in range(26):
                C0[i] = cnt[i]
                C1[i] = abs(cnt[i] - k)
            
            # Precompute excess and deficit for each position
            excess = [max(0, cnt[i] - k) for i in range(26)]
            deficit = [max(0, k - cnt[i]) for i in range(26)]
            
            # DP: dp[j][t] = min cost for first i+1 positions, j targets, t = is target at i
            # Initialize for i=0
            dp = [[INF] * 2 for _ in range(27)]
            dp[0][0] = C0[0]
            dp[1][1] = C1[0]
            
            for i in range(1, 26):
                new_dp = [[INF] * 2 for _ in range(27)]
                for j in range(27):
                    # Current position is not a target (t=0)
                    # B(0,0) = 0, B(1,0) = 0
                    cost0 = dp[j][0] + C0[i]
                    cost1 = dp[j][1] + C0[i]
                    new_dp[j][0] = min(cost0, cost1)
                    
                    # Current position is a target (t=1)
                    if j > 0:
                        # B(0,1): prev not target, curr target
                        # Shift from i-1 (non-target) to i (target)
                        # Available at i-1: cnt[i-1] (all)
                        # Deficit at i: deficit[i]
                        b01 = -min(cnt[i-1], deficit[i])
                        cost_prev0 = dp[j-1][0] + C1[i] + b01
                        
                        # B(1,1): prev target, curr target
                        # Shift from i-1 (target) to i (target)
                        # Available at i-1: excess[i-1]
                        # Deficit at i: deficit[i]
                        b11 = -min(excess[i-1], deficit[i])
                        cost_prev1 = dp[j-1][1] + C1[i] + b11
                        
                        new_dp[j][1] = min(cost_prev0, cost_prev1)
                
                dp = new_dp
            
            # Find min cost over all d (number of targets)
            for d in range(27):
                cost = min(dp[d][0], dp[d][1])
                if cost < ans:
                    ans = cost
        
        return ans