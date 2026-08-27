class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        
        # Directions: (dr, dc)
        # Order: (1,1), (1,-1), (-1,-1), (-1,1)
        # Clockwise turn mapping: 
        #   (1,1) -> (1,-1)  [index 0 -> 1]
        #   (1,-1) -> (-1,-1) [index 1 -> 2]
        #   (-1,-1) -> (-1,1) [index 2 -> 3]
        #   (-1,1) -> (1,1)   [index 3 -> 0]
        dirs = [(1,1), (1,-1), (-1,-1), (-1,1)]
        clockwise_next = [1, 2, 3, 0]
        
        # dp[dir_idx][r][c][0] = len2: length of valid sequence starting at (r,c) in dir, expecting 2
        # dp[dir_idx][r][c][1] = len0: length of valid sequence starting at (r,c) in dir, expecting 0
        # We'll use two 3D arrays: len2[dir][r][c] and len0[dir][r][c]
        len2 = [[[0]*m for _ in range(n)] for _ in range(4)]
        len0 = [[[0]*m for _ in range(n)] for _ in range(4)]
        
        # Fill DP tables backwards
        for d in range(4):
            dr, dc = dirs[d]
            # We need to iterate in reverse order of the direction
            # For direction (dr, dc), we iterate r from n-1 to 0 if dr>0, else 0 to n-1
            # Similarly for c
            if dr > 0:
                r_range = range(n-1, -1, -1)
            else:
                r_range = range(0, n)
            if dc > 0:
                c_range = range(m-1, -1, -1)
            else:
                c_range = range(0, m)
                
            for r in r_range:
                for c in c_range:
                    # For len2: current cell must be 2
                    if grid[r][c] == 2:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < m:
                            # Next expected value is 0
                            len2[d][r][c] = 1 + len0[d][nr][nc]
                        else:
                            len2[d][r][c] = 1
                    else:
                        len2[d][r][c] = 0
                        
                    # For len0: current cell must be 0
                    if grid[r][c] == 0:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < m:
                            # Next expected value is 2
                            len0[d][r][c] = 1 + len2[d][nr][nc]
                        else:
                            len0[d][r][c] = 1
                    else:
                        len0[d][r][c] = 0
                        
        ans = 0
        
        # Iterate over all cells that are 1
        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue
                    
                # Try each initial direction
                for d1 in range(4):
                    dr1, dc1 = dirs[d1]
                    
                    # First segment: starts at (r,c) with 1, next should be 2
                    nr1, nc1 = r + dr1, c + dc1
                    if 0 <= nr1 < n and 0 <= nc1 < m and grid[nr1][nc1] == 2:
                        L1 = 1 + len2[d1][nr1][nc1]
                    else:
                        L1 = 1  # Only the starting 1
                    
                    # The vertex is at:
                    vr = r + (L1 - 1) * dr1
                    vc = c + (L1 - 1) * dc1
                    
                    # Update answer with straight segment (no turn)
                    ans = max(ans, L1)
                    
                    # Try turning 90 degrees clockwise
                    d2 = clockwise_next[d1]
                    dr2, dc2 = dirs[d2]
                    
                    # The next cell in the new direction should be at index L1 in the sequence
                    # If L1 is odd (1,3,5,...), expected value is 2
                    # If L1 is even (2,4,6,...), expected value is 0
                    nr2, nc2 = vr + dr2, vc + dc2
                    if 0 <= nr2 < n and 0 <= nc2 < m:
                        if L1 % 2 == 1:  # odd, expect 2
                            add = len2[d2][nr2][nc2]
                        else:  # even, expect 0
                            add = len0[d2][nr2][nc2]
                        ans = max(ans, L1 + add)
                        
        return ans