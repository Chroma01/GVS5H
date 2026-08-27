from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        
        n, m = len(grid), len(grid[0])
        
        # Directions: 0: TL-BR (dr=1, dc=1), 1: TR-BL (dr=-1, dc=1), 
        #              2: BR-TL (dr=1, dc=-1), 3: BL-TR (dr=-1, dc=-1)
        # Clockwise turn mapping: (dir + 1) % 4
        dirs = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        
        # dp[d][i][j][p] = max length of straight segment starting at (i,j) in dir d
        # where p = step_index % 2. 
        # If p=0, expected value is 0 (for step > 0). If p=1, expected value is 2.
        dp = [[[ [0, 0] for _ in range(m)] for _ in range(n)] for _ in range(4)]
        
        # Precompute DP for straight segments
        for d in range(4):
            dr, dc = dirs[d]
            # Determine iteration order to process backwards
            if dr > 0:
                i_range = range(n - 1, -1, -1)
            else:
                i_range = range(n)
            
            if dc > 0:
                j_range = range(m - 1, -1, -1)
            else:
                j_range = range(m)
            
            for i in i_range:
                for j in j_range:
                    ni, nj = i + dr, j + dc
                    if 0 <= ni < n and 0 <= nj < m:
                        for p in range(2):
                            expected_val = 0 if p == 0 else 2
                            if grid[ni][nj] == expected_val:
                                dp[d][i][j][p] = 1 + dp[d][ni][nj][1 - p]
                            else:
                                dp[d][i][j][p] = 0
                    else:
                        dp[d][i][j][p] = 0
        
        max_len = 0
        
        # Iterate over every cell as a potential start point
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    # Try all 4 starting directions
                    for start_d in range(4):
                        dr, dc = dirs[start_d]
                        ni, nj = i + dr, j + dc
                        step = 1
                        current_len = 1  # Length includes the starting '1'
                        turned = False
                        
                        while 0 <= ni < n and 0 <= nj < m and not turned:
                            # Check if current cell matches expected value for this step
                            expected_val = 2 if (step % 2 == 1) else 0
                            
                            if grid[ni][nj] != expected_val:
                                break
                            
                            current_len += 1  # Extend the straight segment by 1
                            
                            # Check for a 90-degree clockwise turn
                            new_d = (start_d + 1) % 4
                            nni, nnj = ni + dirs[new_d][0], nj + dirs[new_d][1]
                            
                            if 0 <= nni < n and 0 <= nnj < m:
                                next_parity = (step + 1) % 2
                                expected_next = 2 if next_parity == 1 else 0
                                
                                if grid[nni][nnj] == expected_next:
                                    # Calculate total length if we turn here
                                    # The turn happens at (ni, nj) -> (nni, nnj).
                                    # The segment after turn starts at (nni, nnj) with step index (step + 1).
                                    # The parity for the DP lookup corresponds to the step index of the first cell in the new segment.
                                    # The first cell in the new segment is (nni, nnj), which is at step (step + 1) relative to the start.
                                    # So we look up dp[new_d][nni][nnj][(step + 1) % 2].
                                    turn_len = dp[new_d][nni][nnj][next_parity]
                                    total = current_len + turn_len
                                    if total > max_len:
                                        max_len = total
                                    
                                    # After turning, we cannot turn again. Stop simulation for this start_d.
                                    turned = True
                            
                            # Move to next cell in current direction
                            ni, nj = nni, nnj
                            step += 1
        
        return max_len