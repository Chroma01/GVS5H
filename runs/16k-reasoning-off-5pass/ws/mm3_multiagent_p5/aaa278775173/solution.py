from typing import List
from functools import lru_cache

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Directions: 0=NE, 1=SE, 2=SW, 3=NW (clockwise order)
        # dx, dy per direction
        DIR = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

        @lru_cache(maxsize=None)
        def solve(i: int, j: int, d: int, turned: int) -> int:
            """
            Returns the max length of a V-segment that:
              - starts at cell (i, j) (which already has its value placed),
              - will move next in direction d,
              - has already made 'turned' clockwise turns (0 or 1).
            The current cell's value is already included in the length.
            """
            # Best we can do is just stay at this cell
            best = 1
            # Expected next value based on current cell's value
            cur = grid[i][j]
            if cur == 1:
                expect = 2
            elif cur == 2:
                expect = 0
            else:  # cur == 0
                expect = 2

            # 1) Try going straight in same direction
            ni = i + DIR[d][0]
            nj = j + DIR[d][1]
            if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == expect:
                best = max(best, 1 + solve(ni, nj, d, turned))

            # 2) Try making a clockwise 90-degree turn (if not already turned)
            if turned == 0:
                nd = (d + 1) % 4
                ni2 = i + DIR[nd][0]
                nj2 = j + DIR[nd][1]
                if 0 <= ni2 < n and 0 <= nj2 < m and grid[ni2][nj2] == expect:
                    best = max(best, 1 + solve(ni2, nj2, nd, 1))

            return best

        ans = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    for d in range(4):
                        ans = max(ans, solve(i, j, d, 0))
        return ans