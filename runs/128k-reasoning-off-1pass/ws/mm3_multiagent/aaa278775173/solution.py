import sys
from typing import List
from array import array

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Directions in clockwise order:
        # 0: down-right (1,1), 1: down-left (1,-1), 2: up-left (-1,-1), 3: up-right (-1,1)
        dirs = [(1,1), (1,-1), (-1,-1), (-1,1)]
        
        # Memoization array: -1 means uncomputed
        # State: (r, c, d, turned, step) -> index = (r*m + c)*16 + d*4 + turned*2 + step
        size = n * m * 16
        memo = array('h', [-1]) * size
        
        sys.setrecursionlimit(10000)
        
        def dfs(r: int, c: int, d: int, turned: int, step: int) -> int:
            idx = (r * m + c) * 16 + d * 4 + turned * 2 + step
            if memo[idx] != -1:
                return memo[idx]
            
            # step: 0 means next expected is 2, 1 means next expected is 0
            expected = 2 if step == 0 else 0
            max_len = 1  # current cell counts as 1
            
            # Try moving straight
            dr, dc = dirs[d]
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == expected:
                res = 1 + dfs(nr, nc, d, turned, 1 - step)
                if res > max_len:
                    max_len = res
            
            # Try making a clockwise turn (if not already used)
            if not turned:
                nd = (d + 1) % 4
                dr, dc = dirs[nd]
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == expected:
                    res = 1 + dfs(nr, nc, nd, 1, 1 - step)
                    if res > max_len:
                        max_len = res
            
            memo[idx] = max_len
            return max_len
        
        ans = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    for d in range(4):
                        # Start: at (i,j) which is 1. Next expected is 2 (step=0). Turn not used.
                        res = dfs(i, j, d, 0, 0)
                        if res > ans:
                            ans = res
        return ans