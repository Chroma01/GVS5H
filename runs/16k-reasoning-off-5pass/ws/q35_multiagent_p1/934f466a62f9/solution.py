import sys

def solve():
    # Increase recursion depth just in case, though we use iterative DP
    sys.setrecursionlimit(2000)
    
    input = sys.stdin.read
    data = input().split()
    iterator = iter(data)
    
    try:
        T_str = next(iterator, None)
        if T_str is None:
            return
        T = int(T_str)
    except StopIteration:
        return

    out_lines = []
    
    for _ in range(T):
        try:
            N = int(next(iterator))
            K = int(next(iterator))
        except StopIteration:
            break
            
        cakes = []
        for i in range(N):
            x = int(next(iterator))
            y = int(next(iterator))
            z = int(next(iterator))
            cakes.append((x, y, z))
            
        if N <= 20:
            # Brute force for small N using DP with bitmask
            # Precompute pair weights
            # weight[i][j] for i < j
            weight = [[0] * N for _ in range(N)]
            for i in range(N):
                xi, yi, zi = cakes[i]
                for j in range(i + 1, N):
                    xj, yj, zj = cakes[j]
                    w = max(xi + xj, yi + yj, zi + zj)
                    weight[i][j] = w
                    weight[j][i] = w
            
            # dp[mask] = max total weight for the subset of items represented by mask
            # We want to find max weight for any mask with exactly 2*K bits set.
            # However, computing dp for all masks is O(2^N * N^2) which is too slow for N=20.
            # 2^20 * 400 = 400M operations. Might be TLE in Python.
            
            # Better approach: Recursive backtracking with pruning or simple recursion.
            # Since we need exactly K pairs, we can just try to form K pairs.
            
            best_total = 0
            used = [False] * N
            
            # To speed up, we can precompute the list of pairs and sort them?
            # No, backtracking is better for exact K.
            
            def backtrack(k_left, current_total):
                nonlocal best_total
                if k_left == 0:
                    if current_total > best_total:
                        best_total = current_total
                    return
                
                # Find first unused item
                try:
                    i = used.index(False)
                except ValueError:
                    return # Should not happen if logic is correct
                
                # Try pairing i with any other unused j
                for j in range(i + 1, N):
                    if not used[j]:
                        used[i] = True
                        used[j] = True
                        w = weight[i][j]
                        backtrack(k_left - 1, current_total + w)
                        used[i] = False
                        used[j] = False
                        
            backtrack(K, 0)
            out_lines.append(str(best_total))
            
        else:
            # For larger N, use Binary Search on Answer + DP on a subset of cakes
            # Heuristic: Select the top 2K cakes (capped at 20 for DP feasibility)
            # based on the sum of their coordinates.
            
            # Sort indices by sum of coordinates descending
            indices = list(range(N))
            indices.sort(key=lambda i: cakes[i][0] + cakes[i][1] + cakes[i][2], reverse=True)
            
            # Take top M = min(N, 2*K + 10) cakes? 
            # If 2K is small, we take all relevant. If 2K is large, we cap at 20.
            limit = 2 * K
            if limit > 20:
                limit = 20 # Cap at 20 for brute force feasibility
            
            selected_indices = indices[:limit]
            n_sel = len(selected_indices)
            
            # Map original index to new index 0..n_sel-1
            # We don't need the map, just use selected_indices
            
            # Precompute weights for selected cakes
            w_mat = [[0] * n_sel for _ in range(n_sel)]
            for i in range(n_sel):
                ci = cakes[selected_indices[i]]
                for j in range(i + 1, n_sel):
                    cj = cakes[selected_indices[j]]
                    w = max(ci[0]+cj[0], ci[1]+cj[1], ci[2]+cj[2])
                    w_mat[i][j] = w
                    w_mat[j][i] = w
            
            # We need to find max weight matching of size K_eff in this subgraph?
            # K_eff = min(K, n_sel // 2)
            K_eff = min(K, n_sel // 2)
            
            # DP for max weight matching of size k in small graph
            # dp[mask] = max weight for subset mask
            num_states = 1 << n_sel
            dp = [-1] * num_states
            dp[0] = 0
            
            # Iterate over masks
            # To save time, we can iterate by number of set bits or just all.
            # Since n_sel <= 20, 2^20 = 1M states.
            # For each state, we find the first unused bit and try pairing it.
            
            # Optimization: Precompute unused bits? No, just compute on fly.
            
            for mask in range(num_states):
                if dp[mask] == -1:
                    continue
                
                # Find first unused bit in mask
                # unused = ((1 << n_sel) - 1) ^ mask
                # i = (unused & -unused).bit_length() - 1
                # This gives the lowest set bit in unused, which is the first unused item.
                
                unused = ((1 << n_sel) - 1) ^ mask
                if unused == 0:
                    continue
                    
                i = (unused & -unused).bit_length() - 1
                
                # Try pairing i with any other unused j
                temp_unused = unused ^ (1 << i)
                while temp_unused:
                    j = (temp_unused & -temp_unused).bit_length() - 1
                    temp_unused ^= (1 << j)
                    
                    new_mask = mask | (1 << i) | (1 << j)
                    new_val = dp[mask] + w_mat[i][j]
                    if new_val > dp[new_mask]:
                        dp[new_mask] = new_val
                        
            # Find max weight for any mask with exactly 2*K_eff bits set
            max_w = 0
            target_bits = 2 * K_eff
            
            # Iterate over all masks and check popcount
            # This is O(2^N_sel) which is 1M, fast enough.
            for mask in range(num_states):
                if bin(mask).count('1') == target_bits:
                    if dp[mask] > max_w:
                        max_w = dp[mask]
                        
            # Binary Search on Answer
            # Range: 0 to 10^14
            low = 0
            high = 10**14
            ans = 0
            
            while low <= high:
                mid = (low + high) // 2
                if max_w >= mid:
                    ans = mid
                    low = mid + 1
                else:
                    high = mid - 1
                    
            out_lines.append(str(ans))

    sys.stdout.write('\n'.join(out_lines) + '\n')

solve()