class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        
        # Directions: 0: (1,1), 1: (1,-1), 2: (-1,-1), 3: (-1,1)
        dirs = [(1,1), (1,-1), (-1,-1), (-1,1)]
        
        # dp0[dir][i][j] = max length starting at (i,j) in dir with expected 2
        # dp1[dir][i][j] = max length starting at (i,j) in dir with expected 0
        dp0 = [[[0]*m for _ in range(n)] for _ in range(4)]
        dp1 = [[[0]*m for _ in range(n)] for _ in range(4)]
        
        for d in range(4):
            dr, dc = dirs[d]
            # Iterate in reverse order of the direction
            # The starting point for iteration depends on the direction
            if dr == 1 and dc == 1:
                rows, cols = range(n-1, -1, -1), range(m-1, -1, -1)
            elif dr == 1 and dc == -1:
                rows, cols = range(n-1, -1, -1), range(m-1, -1, -1)
            elif dr == -1 and dc == -1:
                rows, cols = range(n-1, -1, -1), range(m-1, -1, -1)
            elif dr == -1 and dc == 1:
                rows, cols = range(n-1, -1, -1), range(m-1, -1, -1)
            
            for i in rows:
                for j in cols:
                    # For dp0: expected value is 2
                    if grid[i][j] == 2:
                        ni, nj = i + dr, j + dc
                        if 0 <= ni < n and 0 <= nj < m:
                            dp0[d][i][j] = 1 + dp0[d][ni][nj]
                        else:
                            dp0[d][i][j] = 1
                    else:
                        dp0[d][i][j] = 0
                    
                    # For dp1: expected value is 0
                    if grid[i][j] == 0:
                        ni, nj = i + dr, j + dc
                        if 0 <= ni < n and 0 <= nj < m:
                            dp1[d][i][j] = 1 + dp1[d][ni][nj]
                        else:
                            dp1[d][i][j] = 1
                    else:
                        dp1[d][i][j] = 0
        
        # Clockwise turn mapping: 
        # 0 (1,1) -> 1 (1,-1)
        # 1 (1,-1) -> 3 (-1,1)
        # 2 (-1,-1) -> 0 (1,1)
        # 3 (-1,1) -> 2 (-1,-1)
        turn_map = {0: 1, 1: 3, 2: 0, 3: 2}
        
        ans = 0
        
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    # Try all 4 initial directions
                    for d in range(4):
                        dr, dc = dirs[d]
                        # Traverse the initial segment
                        # The sequence is 1, 2, 0, 2, 0, ...
                        # Step 0: 1 (current cell)
                        # Step 1: 2
                        # Step 2: 0
                        # Step 3: 2
                        # ...
                        # So for step k (k>=1), expected value is 2 if k is odd, 0 if k is even.
                        
                        # Current position in the initial segment
                        ci, cj = i, j
                        # Length of initial segment so far (including the 1)
                        length = 1
                        
                        # We can also consider not turning at all, so update ans with length
                        if length > ans:
                            ans = length
                        
                        # Move to next cell in direction d
                        ni, nj = ci + dr, cj + dc
                        step = 1
                        while 0 <= ni < n and 0 <= nj < m:
                            # Expected value for step 'step'
                            # step 1: 2, step 2: 0, step 3: 2, ...
                            expected = 2 if step % 2 == 1 else 0
                            
                            if grid[ni][nj] != expected:
                                break
                            
                            length += 1
                            if length > ans:
                                ans = length
                            
                            # Check if we can turn here
                            # The turn happens at (ni, nj), and the next segment starts from the next cell in the new direction
                            new_d = turn_map[d]
                            ndr, ndc = dirs[new_d]
                            # The next cell in the new direction
                            tni, tnj = ni + ndr, nj + ndc
                            if 0 <= tni < n and 0 <= tnj < m:
                                # The next expected value after step 'step' is for step 'step+1'
                                # If step was odd (expected 2), then step+1 is even (expected 0) -> use dp1
                                # If step was even (expected 0), then step+1 is odd (expected 2) -> use dp0
                                if step % 2 == 1: # next expected is 0
                                    additional = dp1[new_d][tni][tnj]
                                else: # next expected is 2
                                    additional = dp0[new_d][tni][tnj]
                                
                                total = length + additional
                                if total > ans:
                                    ans = total
                            
                            # Move to next cell in initial direction
                            ci, cj = ni, nj
                            ni, nj = ci + dr, cj + dc
                            step += 1
        
        return ans