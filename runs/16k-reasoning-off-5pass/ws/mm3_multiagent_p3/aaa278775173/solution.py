from typing import List
from functools import lru_cache

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Directions: 0: down-right (↘), 1: down-left (↙), 2: up-left (↖), 3: up-right (↗)
        # Clockwise order: 0 -> 1 -> 2 -> 3 -> 0
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        # Expected value flag: 0 means next expected is 2, 1 means next expected is 0
        # Pattern after 1: 2, 0, 2, 0, ...
        expected_vals = [2, 0]
        
        @lru_cache(maxsize=None)
        def solve(i: int, j: int, d: int, p: int, t: int) -> int:
            """
            Returns the length of the longest valid V-segment starting at (i,j),
            already moving in direction d. The current cell (i,j) is valid.
            p: 0 -> next cell should be 2; 1 -> next cell should be 0.
            t: 0 -> turn not used yet; 1 -> turn already used.
            Length includes the current cell.
            """
            # Try to move straight
            ni, nj = i + dirs[d][0], j + dirs[d][1]
            best = 1  # base: stay at current cell
            if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == expected_vals[p]:
                # Move straight, flip expected value, keep turn flag
                best = max(best, 1 + solve(ni, nj, d, 1 - p, t))
            # Try clockwise turn if not used yet
            if t == 0:
                # We can turn only if the next cell (in new direction) matches expected
                nd = (d + 1) % 4
                ti, tj = i + dirs[nd][0], j + dirs[nd][1]
                if 0 <= ti < n and 0 <= ti < n and 0 <= tj < m and 0 <= tj < m and grid[ti][tj] == expected_vals[p]:
                    # Turn, then continue with flipped expected and turn_used=1
                    best = max(best, 1 + solve(ti, tj, nd, 1 - p, 1))
            return best
        
        ans = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    for d in range(4):
                        # From a 1, the next cell must be 2 (p=0), and no turn used yet.
                        length = 1 + solve(i, j, d, 0, 0)
                        if length > ans:
                            ans = length
        return ans