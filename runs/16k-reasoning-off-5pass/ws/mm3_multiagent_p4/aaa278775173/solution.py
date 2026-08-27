from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        
        # Directions: 0: (1,1) SE, 1: (1,-1) SW, 2: (-1,1) NE, 3: (-1,-1) NW
        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        # Clockwise mapping: 0->1, 1->3, 3->2, 2->0
        clockwise = [1, 3, 0, 2]
        
        # Precompute dp for each direction and parity
        # dp2[d][i][j] = length of alternating tail starting at (i,j) in direction d, expecting 2
        # dp0[d][i][j] = length of alternating tail starting at (i,j) in direction d, expecting 0
        dp2 = [[[0]*m for _ in range(n)] for _ in range(4)]
        dp0 = [[[0]*m for _ in range(n)] for _ in range(4)]
        
        # For each direction, iterate in reverse order
        for d in range(4):
            di, dj = dirs[d]
            if di == 1 and dj == 1:  # SE: from bottom-right to top-left
                i_range = range(n-1, -1, -1)
                j_range = range(m-1, -1, -1)
            elif di == 1 and dj == -1:  # SW: from bottom-left to top-right
                i_range = range(n-1, -1, -1)
                j_range = range(0, m)
            elif di == -1 and dj == 1:  # NE: from top-right to bottom-left
                i_range = range(0, n)
                j_range = range(m-1, -1, -1)
            else:  # di == -1 and dj == -1: NW: from top-left to bottom-right
                i_range = range(0, n)
                j_range = range(0, m)
            
            for i in i_range:
                for j in j_range:
                    # Compute dp2: expecting 2
                    if grid[i][j] == 2:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < n and 0 <= nj < m:
                            dp2[d][i][j] = 1 + dp0[d][ni][nj]
                        else:
                            dp2[d][i][j] = 1
                    # Compute dp0: expecting 0
                    if grid[i][j] == 0:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < n and 0 <= nj < m:
                            dp0[d][i][j] = 1 + dp2[d][ni][nj]
                        else:
                            dp0[d][i][j] = 1
        
        ans = 0
        # Iterate over all starting cells (value 1)
        for i in range(n):
            for j in range(m):
                if grid[i][j] != 1:
                    continue
                # For each initial direction
                for d in range(4):
                    di, dj = dirs[d]
                    # No turn case
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == 2:
                        ans = max(ans, 1 + dp2[d][ni][nj])
                    
                    # With turn case
                    d2 = clockwise[d]
                    di2, dj2 = dirs[d2]
                    k = 1
                    x, y = i + di, j + dj
                    while 0 <= x < n and 0 <= y < m:
                        # Expected value at step k: 2 if k odd, 0 if k even
                        expected = 2 if k % 2 == 1 else 0
                        if grid[x][y] != expected:
                            break
                        # Try turning at this cell
                        # Next expected value after this cell is opposite
                        p2 = 1 if expected == 2 else 0
                        x2, y2 = x + di2, y + dj2
                        if 0 <= x2 < n and 0 <= y2 < m:
                            if p2 == 0:  # expecting 2
                                length = 1 + k + dp2[d2][x2][y2]
                            else:  # expecting 0
                                length = 1 + k + dp0[d2][x2][y2]
                        else:
                            length = 1 + k
                        ans = max(ans, length)
                        
                        k += 1
                        x += di
                        y += dj
        
        return ans

# Test with the provided examples
if __name__ == "__main__":
    sol = Solution()
    
    # Example 1
    grid1 = [[2,2,1,2,2],[2,0,2,2,0],[2,0,1,1,0],[1,0,2,2,2],[2,0,0,2,2]]
    print(f"Example 1: {sol.lenOfVDiagonal(grid1)} (expected: 5)")
    
    # Example 2
    grid2 = [[2,2,2,2,2],[2,0,2,2,0],[2,0,1,1,0],[1,0,2,2,2],[2,0,0,2,2]]
    print(f"Example 2: {sol.lenOfVDiagonal(grid2)} (expected: 4)")
    
    # Example 3
    grid3 = [[1,2,2,2,2],[2,2,2,2,0],[2,0,0,0,0],[0,0,2,2,2],[2,0,0,2,0]]
    print(f"Example 3: {sol.lenOfVDiagonal(grid3)} (expected: 5)")
    
    # Example 4
    grid4 = [[1]]
    print(f"Example 4: {sol.lenOfVDiagonal(grid4)} (expected: 1)")