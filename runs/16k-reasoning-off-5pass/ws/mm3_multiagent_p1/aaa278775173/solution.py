class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        
        # Directions: 0: (1,1), 1: (1,-1), 2: (-1,-1), 3: (-1,1)
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Precompute dp1[i][j][d]: length of segment starting at (i,j) with value 1 going in direction d
        # dp2[i][j][d]: length starting with value 2
        # dp0[i][j][d]: length starting with value 0
        # Sequence: 1 -> 2 -> 0 -> 2 -> 0 -> ...
        # If start with 2: 2 -> 0 -> 2 -> 0 -> ...
        # If start with 0: 0 -> 2 -> 0 -> 2 -> ...
        
        dp1 = [[[0]*4 for _ in range(m)] for _ in range(n)]
        dp2 = [[[0]*4 for _ in range(m)] for _ in range(n)]
        dp0 = [[[0]*4 for _ in range(m)] for _ in range(n)]
        
        # Process from bottom-right to top-left to ensure dependencies are computed
        for i in range(n-1, -1, -1):
            for j in range(m-1, -1, -1):
                for d in range(4):
                    di, dj = dirs[d]
                    ni, nj = i + di, j + dj
                    
                    # dp1: start with 1, next should be 2
                    if grid[i][j] == 1:
                        if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == 2:
                            dp1[i][j][d] = 1 + dp2[ni][nj][d]
                        else:
                            dp1[i][j][d] = 1
                    
                    # dp2: start with 2, next should be 0
                    if grid[i][j] == 2:
                        if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == 0:
                            dp2[i][j][d] = 1 + dp0[ni][nj][d]
                        else:
                            dp2[i][j][d] = 1
                    
                    # dp0: start with 0, next should be 2
                    if grid[i][j] == 0:
                        if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == 2:
                            dp0[i][j][d] = 1 + dp2[ni][nj][d]
                        else:
                            dp0[i][j][d] = 1
        
        ans = 0
        
        # Try all starting cells with value 1
        for i in range(n):
            for j in range(m):
                if grid[i][j] != 1:
                    continue
                for d in range(4):
                    # Case 1: no turn, straight segment
                    length = dp1[i][j][d]
                    if length > ans:
                        ans = length
                    
                    # Case 2: one clockwise turn
                    # Turn at each step along the straight path
                    di, dj = dirs[d]
                    # d2 is clockwise: 0->1, 1->2, 2->3, 3->0
                    d2 = (d + 1) % 4
                    
                    # Iterate over possible turn points
                    # k is the number of steps taken in first direction (0-indexed)
                    # At step k, we are at (i + k*di, j + k*dj)
                    # The value at that point must match the sequence
                    # k=0: value 1, k=1: value 2, k=2: value 0, k=3: value 2, k=4: value 0, ...
                    # We need to continue from that point in direction d2
                    # The continuation length depends on the value at the turn point
                    
                    # We can iterate up to dp1[i][j][d] steps
                    max_steps = dp1[i][j][d]
                    for k in range(max_steps):
                        ti = i + k * di
                        tj = j + k * dj
                        if not (0 <= ti < n and 0 <= tj < m):
                            break
                        
                        # Determine the value at turn point
                        # k=0: 1, k=1: 2, k=2: 0, k=3: 2, k=4: 0, ...
                        if k == 0:
                            val = 1
                        elif k % 2 == 1:
                            val = 2
                        else:
                            val = 0
                        
                        # Get continuation length in direction d2
                        if val == 1:
                            cont = dp1[ti][tj][d2]
                        elif val == 2:
                            cont = dp2[ti][tj][d2]
                        else:
                            cont = dp0[ti][tj][d2]
                        
                        # Total length: (k+1) steps in first direction + (cont - 1) steps in second direction
                        # Because the turn point is counted in both legs
                        total = (k + 1) + (cont - 1)
                        if total > ans:
                            ans = total
        
        return ans