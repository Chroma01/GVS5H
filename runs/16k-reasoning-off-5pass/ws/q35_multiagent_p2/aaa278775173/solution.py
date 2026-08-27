class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        
        # Directions: (dr, dc)
        # 0: (1, 1)     bottom-right
        # 1: (1, -1)    bottom-left
        # 2: (-1, -1)   top-left
        # 3: (-1, 1)    top-right
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Clockwise turn mapping:
        # (1,1) -> (1,-1) : 0 -> 1
        # (1,-1) -> (-1,-1) : 1 -> 2
        # (-1,-1) -> (-1,1) : 2 -> 3
        # (-1,1) -> (1,1) : 3 -> 0
        clockwise = [1, 2, 3, 0]
        
        # dp_odd[d][r][c]: length of valid sequence starting at (r,c) in direction d
        #                  assuming current index is odd (value should be 2)
        # dp_even[d][r][c]: length of valid sequence starting at (r,c) in direction d
        #                   assuming current index is even and >0 (value should be 0)
        # dp0[d][r][c]: length of valid sequence starting at (r,c) in direction d
        #               assuming current index is 0 (value should be 1)
        
        dp_odd = [[0] * m for _ in range(n)]
        dp_even = [[0] * m for _ in range(n)]
        dp0 = [[0] * m for _ in range(n)]
        
        # Fill DP tables in reverse order (from bottom-right to top-left generally, 
        # but we need to process in an order such that next cells are computed first.
        # Since directions can go in any direction, we iterate r from n-1 to 0 and c from m-1 to 0
        # is not sufficient for all directions. Instead, we can iterate in reverse topological order.
        # For diagonal directions, iterating r from n-1 to 0 and c from m-1 to 0 works for (1,1) and (1,-1) 
        # if we consider the "next" cell is further in the direction.
        # Actually, for direction (dr, dc), the next cell is (r+dr, c+dc).
        # To ensure next cell is computed first, we should iterate in reverse of the direction.
        # For (1,1): iterate r from n-1 to 0, c from m-1 to 0.
        # For (1,-1): iterate r from n-1 to 0, c from 0 to m-1.
        # For (-1,-1): iterate r from 0 to n-1, c from 0 to m-1.
        # For (-1,1): iterate r from 0 to n-1, c from m-1 to 0.
        
        # We'll create a list of (r, c) in the correct order for each direction and process.
        # But simpler: just iterate r from n-1 down to 0 and c from m-1 down to 0 for all? 
        # That doesn't work for directions going up.
        # Instead, we process each direction separately with appropriate iteration order.
        
        for d in range(4):
            dr, dc = dirs[d]
            # Determine iteration order
            if dr == 1:
                r_start, r_end, r_step = n - 1, -1, -1
            else:
                r_start, r_end, r_step = 0, n, 1
                
            if dc == 1:
                c_start, c_end, c_step = m - 1, -1, -1
            else:
                c_start, c_end, c_step = 0, m, 1
                
            for r in range(r_start, r_end, r_step):
                for c in range(c_start, c_end, c_step):
                    nr, nc = r + dr, c + dc
                    
                    # Compute dp_odd: current index is odd, value should be 2
                    if grid[r][c] == 2:
                        if 0 <= nr < n and 0 <= nc < m:
                            dp_odd[d][r][c] = 1 + dp_even[d][nr][nc]
                        else:
                            dp_odd[d][r][c] = 1
                    else:
                        dp_odd[d][r][c] = 0
                        
                    # Compute dp_even: current index is even (>0), value should be 0
                    if grid[r][c] == 0:
                        if 0 <= nr < n and 0 <= nc < m:
                            dp_even[d][r][c] = 1 + dp_odd[d][nr][nc]
                        else:
                            dp_even[d][r][c] = 1
                    else:
                        dp_even[d][r][c] = 0
                        
                    # Compute dp0: current index is 0, value should be 1
                    if grid[r][c] == 1:
                        if 0 <= nr < n and 0 <= nc < m:
                            dp0[d][r][c] = 1 + dp_odd[d][nr][nc]
                        else:
                            dp0[d][r][c] = 1
                    else:
                        dp0[d][r][c] = 0
                        
        ans = 0
        
        # For each cell that is a start (value 1)
        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue
                    
                # For each initial direction
                for d1 in range(4):
                    # The first leg starts at (r,c) with index 0.
                    # The maximum length of the first leg is dp0[d1][r][c]
                    # But we can turn at any point in the first leg.
                    # Let k be the index of the pivot cell (0-indexed).
                    # The pivot cell is at index k in the first leg.
                    # The first leg has length L1 = dp0[d1][r][c].
                    # The pivot can be at any k from 0 to L1-1.
                    # However, we don't need to iterate k explicitly if we use the DP values.
                    
                    # If we turn at the pivot cell (which is at global index k),
                    # the second leg starts at the next cell in direction d2 = clockwise[d1].
                    # The index for the second leg start is k+1.
                    # The length of the second leg is:
                    #   if (k+1) is odd: dp_odd[d2][pivot_next_r][pivot_next_c]
                    #   if (k+1) is even: dp_even[d2][pivot_next_r][pivot_next_c]
                    # Total length = (k+1) + second_leg_length
                    
                    # Instead of iterating k, note that:
                    # The first leg from (r,c) in direction d1 has a certain structure.
                    # We can compute the length of the first leg up to each cell.
                    # But a simpler approach: 
                    # For a fixed start (r,c) and direction d1, the first leg is fixed.
                    # We can traverse the first leg and at each step, consider turning.
                    
                    # Traverse first leg
                    curr_r, curr_c = r, c
                    # k is the index in the sequence for the current cell in the first leg
                    k = 0
                    while 0 <= curr_r < n and 0 <= curr_c < m:
                        # Check if current cell matches expected value for index k
                        if k == 0:
                            expected = 1
                        elif k % 2 == 1:
                            expected = 2
                        else:
                            expected = 0
                            
                        if grid[curr_r][curr_c] != expected:
                            break
                            
                        # Consider turning at this pivot cell (index k)
                        d2 = clockwise[d1]
                        # The next cell for the second leg is in direction d2 from (curr_r, curr_c)
                        nr2, nc2 = curr_r + dirs[d2][0], curr_c + dirs[d2][1]
                        
                        second_leg_len = 0
                        if 0 <= nr2 < n and 0 <= nc2 < m:
                            # The index for the second leg start is k+1
                            if (k + 1) % 2 == 1:
                                # odd index, use dp_odd
                                second_leg_len = dp_odd[d2][nr2][nc2]
                            else:
                                # even index (>0), use dp_even
                                second_leg_len = dp_even[d2][nr2][nc2]
                        
                        total_len = (k + 1) + second_leg_len
                        if total_len > ans:
                            ans = total_len
                            
                        # Move to next cell in first leg
                        curr_r += dirs[d1][0]
                        curr_c += dirs[d1][1]
                        k += 1
                        
        return ans