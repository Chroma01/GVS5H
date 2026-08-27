from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        
        # Four diagonal directions: 0=SE(1,1), 1=SW(1,-1), 2=NW(-1,-1), 3=NE(-1,1)
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        # Clockwise mapping: 0->1, 1->2, 2->3, 3->0
        cw_next = [1, 2, 3, 0]
        
        # dp[i][j][d] = length of valid alternating sequence starting at (i,j) going in direction d
        # Only valid if grid[i][j] == 1
        dp = [[[0] * 4 for _ in range(m)] for _ in range(n)]
        
        # Process each direction in reverse order so that dp[next] is already computed
        for d in range(4):
            di, dj = dirs[d]
            # Determine iteration order based on direction
            if di == 1 and dj == 1:  # SE: bottom-right to top-left
                i_range = range(n - 1, -1, -1)
                j_range = range(m - 1, -1, -1)
            elif di == 1 and dj == -1:  # SW: bottom-left to top-right
                i_range = range(n - 1, -1, -1)
                j_range = range(0, m)
            elif di == -1 and dj == -1:  # NW: top-left to bottom-right
                i_range = range(0, n)
                j_range = range(0, m)
            else:  # NE: top-right to bottom-left, di=-1, dj=1
                i_range = range(0, n)
                j_range = range(m - 1, -1, -1)
            
            for i in i_range:
                for j in j_range:
                    if grid[i][j] != 1:
                        continue
                    # Check next cell
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < m:
                        # Expected value at position 1 (after starting 1) is 2
                        if grid[ni][nj] == 2:
                            dp[i][j][d] = 1 + dp[ni][nj][d]
                        else:
                            dp[i][j][d] = 1
                    else:
                        dp[i][j][d] = 1
        
        ans = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] != 1:
                    continue
                # Straight segments (no turn)
                for d in range(4):
                    ans = max(ans, dp[i][j][d])
                # V-shaped with one clockwise turn
                for d1 in range(4):
                    d2 = cw_next[d1]
                    # First leg: from (i,j) in direction d1
                    # Second leg: from (i,j) in direction d2
                    # Total length = dp[i][j][d1] + dp[i][j][d2] - 1 (shared turning cell)
                    total = dp[i][j][d1] + dp[i][j][d2] - 1
                    ans = max(ans, total)
        
        return ans