class Solution:
    def minCostGoodCaption(self, caption: str) -> str:
        n = len(caption)
        if n < 3:
            return ""
        
        # Precompute cost[i][c] = |ord(caption[i]) - ord(c)|
        cost = [[0]*26 for _ in range(n)]
        for i, ch in enumerate(caption):
            base = ord(ch) - ord('a')
            for c in range(26):
                cost[i][c] = abs(base - c)
        
        INF = float('inf')
        
        # Forward DP: fwd[i][c][s] = min cost for prefix [0..i] where position i is s-th char of run c
        # s=0,1,2 represent lengths 1,2,3+
        # We only need rolling arrays, but for clarity we use two arrays.
        fwd_prev = [[INF]*3 for _ in range(26)]
        for c in range(26):
            fwd_prev[c][0] = cost[0][c]
        
        best_prev = min(fwd_prev[c][2] for c in range(26))  # min cost with completed run at i=0 (impossible unless n>=3, but compute)
        
        for i in range(1, n):
            fwd_curr = [[INF]*3 for _ in range(26)]
            best_curr = INF
            
            for c in range(26):
                ci = cost[i][c]
                
                # Start new run (only if previous run is completed, i.e., best_prev < INF)
                if best_prev < INF:
                    start_cost = best_prev + ci
                    if start_cost < fwd_curr[c][0]:
                        fwd_curr[c][0] = start_cost
                
                # Continue from length 1 to 2
                if fwd_prev[c][0] < INF:
                    val = fwd_prev[c][0] + ci
                    if val < fwd_curr[c][1]:
                        fwd_curr[c][1] = val
                
                # Continue from length 2 to 3+
                if fwd_prev[c][1] < INF:
                    val = fwd_prev[c][1] + ci
                    if val < fwd_curr[c][2]:
                        fwd_curr[c][2] = val
                
                # Continue from length 3+ to 3+
                if fwd_prev[c][2] < INF:
                    val = fwd_prev[c][2] + ci
                    if val < fwd_curr[c][2]:
                        fwd_curr[c][2] = val
            
            for c in range(26):
                if fwd_curr[c][2] < best_curr:
                    best_curr = fwd_curr[c][2]
            
            fwd_prev = fwd_curr
            best_prev = best_curr
        
        target = min(fwd_prev[c][2] for c in range(26))
        if target == INF:
            return ""
        
        # Suffix DP: suf[i][c][s] = min cost to complete suffix [i..n-1] given state (c,s) at i
        # Compute backward
        # Use list of lists: suf[i] is a flat list of 78 elements indexed by c*3+s
        suf = [None] * n
        last = [INF] * 78
        for c in range(26):
            last[c*3 + 2] = cost[n-1][c]
        suf[n-1] = last
        
        for i in range(n-2, -1, -1):
            curr = [INF] * 78
            min_start_next = INF
            for c2 in range(26):
                val = suf[i+1][c2*3 + 0]
                if val < min_start_next:
                    min_start_next = val
            
            for c in range(26):
                ci = cost[i][c]
                # s=0 -> must go to s=1 at i+1 same c
                curr[c*3 + 0] = ci + suf[i+1][c*3 + 1]
                # s=1 -> must go to s=2 at i+1 same c
                curr[c*3 + 1] = ci + suf[i+1][c*3 + 2]
                # s=2 -> can continue or start new
                continue_val = suf[i+1][c*3 + 2]
                start_new_val = min_start_next
                best_next = continue_val if continue_val < start_new_val else start_new_val
                curr[c*3 + 2] = ci + best_next
            
            suf[i] = curr
        
        # Reconstruct lexicographically smallest
        res = []
        acc = 0
        c_prev = -1
        s_prev = -1
        
        for i in range(n):
            found = False
            if i == 0:
                for c in range(26):
                    if acc + suf[0][c*3 + 0] == target:
                        res.append(chr(ord('a') + c))
                        acc += cost[0][c]
                        c_prev = c
                        s_prev = 0
                        found = True
                        break
            else:
                if s_prev in (0, 1):
                    c = c_prev
                    s = s_prev + 1
                    if acc + suf[i][c*3 + s] == target:
                        res.append(chr(ord('a') + c))
                        acc += cost[i][c]
                        s_prev = s
                        found = True
                else:  # s_prev == 2
                    for c in range(26):
                        s = 2 if c == c_prev else 0
                        if acc + suf[i][c*3 + s] == target:
                            res.append(chr(ord('a') + c))
                            acc += cost[i][c]
                            c_prev = c
                            s_prev = s
                            found = True
                            break
            
            if not found:
                # Should not happen for valid inputs
                break
        
        return "".join(res)