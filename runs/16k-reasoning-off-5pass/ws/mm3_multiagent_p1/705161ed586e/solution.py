class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        INF = 10**18
        # dp[ch][run] = minimum cost to reach position i with state (ch, run)
        # run: 0 -> length 1, 1 -> length 2, 2 -> length >=3
        prev = [[INF] * 3 for _ in range(26)]
        # back[i][ch][run] = (prev_ch, prev_run) for reconstruction, or -2 for start
        back = []
        
        # Initialize for position 0
        orig0 = ord(caption[0]) - ord('a')
        back0 = [[-1] * 3 for _ in range(26)]
        for ch in range(26):
            cost = abs(ch - orig0)
            prev[ch][0] = cost  # run length 1
            back0[ch][0] = -2  # sentinel meaning "start"
        back.append(back0)
        
        # Process positions 1..n-1
        for i in range(1, n):
            cur = [[INF] * 3 for _ in range(26)]
            back_i = [[-1] * 3 for _ in range(26)]
            orig = ord(caption[i]) - ord('a')
            
            for ch in range(26):
                cost_to_ch = abs(ch - orig)
                
                # Option 1: start a new run with character ch (run length 1)
                best_cost = INF
                best_prev = -1
                for prev_ch in range(26):
                    if prev_ch == ch:
                        continue
                    for prev_run in range(3):
                        if prev[prev_ch][prev_run] < INF:
                            c = prev[prev_ch][prev_run] + cost_to_ch
                            if c < best_cost:
                                best_cost = c
                                best_prev = (prev_ch, prev_run)
                if best_cost < INF:
                    cur[ch][0] = best_cost
                    back_i[ch][0] = best_prev
                
                # Option 2: continue the same character ch
                best_cost_cont = INF
                best_prev_cont = -1
                best_prev_run_used = -1
                for prev_run in range(3):
                    if prev[ch][prev_run] < INF:
                        c = prev[ch][prev_run] + cost_to_ch
                        if c < best_cost_cont:
                            best_cost_cont = c
                            best_prev_cont = (ch, prev_run)
                            best_prev_run_used = prev_run
                if best_cost_cont < INF:
                    # Determine new run index
                    if best_prev_run_used == 0:
                        new_run = 1
                    elif best_prev_run_used == 1:
                        new_run = 2
                    else:  # best_prev_run_used == 2
                        new_run = 2  # capped at >=3
                    cur[ch][new_run] = best_cost_cont
                    back_i[ch][new_run] = best_prev_cont
            
            prev = cur
            back.append(back_i)
        
        # Find minimum cost among end states with run length >=3 (index 2)
        best_total = INF
        for ch in range(26):
            if prev[ch][2] < best_total:
                best_total = prev[ch][2]
        
        if best_total == INF:
            return ""
        
        # Collect all end states with minimum cost
        candidates = []
        for ch in range(26):
            if prev[ch][2] == best_total:
                candidates.append((ch, 2))
        
        # Reconstruct each candidate and pick lexicographically smallest
        best_string = None
        for end_ch, end_run in candidates:
            result = []
            cur_ch, cur_run = end_ch, end_run
            for i in range(n - 1, -1, -1):
                result.append(chr(cur_ch + ord('a')))
                bp = back[i][cur_ch][cur_run]
                if bp == -2:
                    break
                cur_ch, cur_run = bp
            candidate_str = ''.join(reversed(result))
            if best_string is None or candidate_str < best_string:
                best_string = candidate_str
        
        return best_string