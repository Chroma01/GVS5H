class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        if n == 0 or m == 0:
            return 0
        
        # Directions: 0: (1,1) down-right, 1: (1,-1) down-left, 2: (-1,-1) up-left, 3: (-1,1) up-right
        directions = [(1,1), (1,-1), (-1,-1), (-1,1)]
        # Clockwise turn mapping: 0->1, 1->2, 2->3, 3->0
        clockwise = [1, 2, 3, 0]
        
        # Precompute even_len and odd_len for each direction
        # even_len[d][i][j]: length of valid segment starting at (i,j) in direction d, where grid[i][j] should be 2
        # odd_len[d][i][j]: length of valid segment starting at (i,j) in direction d, where grid[i][j] should be 0
        even_len = [[[0]*m for _ in range(n)] for _ in range(4)]
        odd_len = [[[0]*m for _ in range(n)] for _ in range(4)]
        
        for d in range(4):
            dr, dc = directions[d]
            # We need to iterate in reverse order of traversal
            # For direction (dr, dc), we iterate from the end backwards
            if dr == 1 and dc == 1:
                rows = range(n-1, -1, -1)
                cols = range(m-1, -1, -1)
            elif dr == 1 and dc == -1:
                rows = range(n-1, -1, -1)
                cols = range(m-1, -1, -1)
            elif dr == -1 and dc == -1:
                rows = range(n-1, -1, -1)
                cols = range(m-1, -1, -1)
            elif dr == -1 and dc == 1:
                rows = range(n-1, -1, -1)
                cols = range(m-1, -1, -1)
            
            for i in rows:
                for j in cols:
                    ni, nj = i + dr, j + dc
                    # For even_len: current cell should be 2
                    if grid[i][j] == 2:
                        if 0 <= ni < n and 0 <= nj < m:
                            # After 2, next should be 0, so we add odd_len of next cell
                            even_len[d][i][j] = 1 + odd_len[d][ni][nj]
                        else:
                            even_len[d][i][j] = 1
                    else:
                        even_len[d][i][j] = 0
                    
                    # For odd_len: current cell should be 0
                    if grid[i][j] == 0:
                        if 0 <= ni < n and 0 <= nj < m:
                            # After 0, next should be 2, so we add even_len of next cell
                            odd_len[d][i][j] = 1 + even_len[d][ni][nj]
                        else:
                            odd_len[d][i][j] = 1
                    else:
                        odd_len[d][i][j] = 0
        
        max_len = 0
        
        # For each cell with value 1, try all 4 initial directions
        for i in range(n):
            for j in range(m):
                if grid[i][j] != 1:
                    continue
                
                for d1 in range(4):
                    dr1, dc1 = directions[d1]
                    # Start from the '1' at (i,j)
                    # The initial run: 
                    #   k=0: (i,j) is 1
                    #   k=1: (i+dr1, j+dc1) should be 2
                    #   k=2: (i+2*dr1, j+2*dc1) should be 0
                    #   etc.
                    
                    ci, cj = i, j
                    # k is the index in the run (0-indexed)
                    for k in range(1000):  # max possible length is n+m
                        # The turn point is (ci, cj)
                        # The next value in sequence (for the turn) is at offset k+1
                        # Offset 1 (first after 1) should be 2, offset 2 should be 0, etc.
                        # So if (k+1) is odd, expected is 2; if even, expected is 0.
                        expected = 2 if (k + 1) % 2 == 1 else 0
                        
                        # Determine turn direction (clockwise)
                        d2 = clockwise[d1]
                        dr2, dc2 = directions[d2]
                        
                        # The next cell in the new direction from turn point
                        ni2, nj2 = ci + dr2, cj + dc2
                        
                        # Check if we can turn: next cell in new direction must be in bounds and have expected value
                        if 0 <= ni2 < n and 0 <= nj2 < m:
                            if grid[ni2][nj2] == expected:
                                # Get the length of the second part
                                if expected == 2:
                                    second_len = even_len[d2][ni2][nj2]
                                else:
                                    second_len = odd_len[d2][ni2][nj2]
                                total = k + 1 + second_len
                                if total > max_len:
                                    max_len = total
                            # Else: cannot turn here, but we continue to next k (next turn point)
                        
                        # Move to next cell in initial direction for next iteration
                        ci += dr1
                        cj += dc1
                        # Check if next cell in initial direction is valid and continues the pattern
                        if not (0 <= ci < n and 0 <= cj < m):
                            break
                        # The value at (ci, cj) should be: 2 if (k+1) is odd, 0 if even
                        expected_init = 2 if (k + 1) % 2 == 1 else 0
                        if grid[ci][cj] != expected_init:
                            break
        
        return max_len