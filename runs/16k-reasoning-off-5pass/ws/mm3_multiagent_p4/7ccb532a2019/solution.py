class Solution:
    def makeStringGood(self, s: str) -> int:
        n = len(s)
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        
        # Candidate target frequencies: 1, n, and all distinct non-zero counts
        candidates = {1, n}
        for c in cnt:
            if c > 0:
                candidates.add(c)
        candidates = sorted(candidates)
        
        min_ops = float('inf')
        offset = n
        INF = float('inf')
        
        for f in candidates:
            # DP over 26 letters: dp[carry][active] = min cost
            # carry from -n to n, offset by n
            # active: 0 (no f yet), 1 (at least one f)
            dp = [[INF, INF] for _ in range(2 * n + 1)]
            dp[offset][0] = 0
            
            for i in range(26):
                c = cnt[i]
                new_dp = [[INF, INF] for _ in range(2 * n + 1)]
                for carry_idx in range(2 * n + 1):
                    cur_carry = carry_idx - offset
                    for active in (0, 1):
                        cur_cost = dp[carry_idx][active]
                        if cur_cost == INF:
                            continue
                        
                        # Option 1: t[i] = 0
                        new_carry1 = cur_carry - c
                        if -n <= new_carry1 <= n:
                            new_idx1 = new_carry1 + offset
                            if cur_cost + c < new_dp[new_idx1][active]:
                                new_dp[new_idx1][active] = cur_cost + c
                        
                        # Option 2: t[i] = f
                        if f >= c:
                            if cur_carry > 0:
                                # Use positive carry to cover deficit
                                used = min(cur_carry, f - c)
                                cost2 = (f - c) - used
                                # Each unit of used carry saves 1 operation
                                new_carry2 = cur_carry - used
                            else:
                                cost2 = f - c
                                new_carry2 = cur_carry
                        else:
                            # c > f: we have excess
                            # We can delete or change to right
                            # The excess adds to carry
                            cost2 = c - f
                            new_carry2 = cur_carry + (c - f)
                        
                        if -n <= new_carry2 <= n:
                            new_idx2 = new_carry2 + offset
                            new_active = 1
                            if cur_cost + cost2 < new_dp[new_idx2][new_active]:
                                new_dp[new_idx2][new_active] = cur_cost + cost2
                
                dp = new_dp
            
            # Get minimum cost among states with active=1
            for carry_idx in range(2 * n + 1):
                if dp[carry_idx][1] < min_ops:
                    min_ops = dp[carry_idx][1]
        
        return min_ops