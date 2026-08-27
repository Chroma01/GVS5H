import sys
from typing import List
from functools import lru_cache

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        sys.setrecursionlimit(1_000_000)
        n = len(grid)
        m = len(grid[0])
        
        # Directions: 0: down-right, 1: down-left, 2: up-left, 3: up-right
        # A clockwise turn is moving from d to (d+1)%4
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        @lru_cache(None)
        def dfs(r: int, c: int, d: int, turned: bool, expected: int) -> int:
            # Base case: current cell does not match the expected value
            if grid[r][c] != expected:
                return 0
            
            # The current cell is valid, so the length is at least 1.
            # We now find the longest path from the next cell.
            
            # Determine the next expected value in the sequence
            next_expected = 0 if expected == 2 else 2
            
            # Option 1: Continue straight
            dr, dc = dirs[d]
            nr, nc = r + dr, c + dc
            
            len_straight = 0
            if 0 <= nr < n and 0 <= nc < m:
                len_straight = dfs(nr, nc, d, turned, next_expected)
            
            max_len_from_here = 1 + len_straight
            
            # Option 2: Make a clockwise turn (if not already turned)
            if not turned:
                new_d = (d + 1) % 4
                dr, dc = dirs[new_d]
                nr, nc = r + dr, c + dc
                
                len_turn = 0
                if 0 <= nr < n and 0 <= nc < m:
                    len_turn = dfs(nr, nc, new_d, True, next_expected)
                
                max_len_from_here = max(max_len_from_here, 1 + len_turn)
                
            return max_len_from_here

        max_overall_len = 0
        for r in range(n):
            for c in range(m):
                if grid[r][c] == 1:
                    # Start a DFS from each cell containing '1'
                    for d in range(4):
                        # The path starts at (r,c) with value 1.
                        # The next expected value is 2.
                        # The length of the path is 1 (for the '1') + length of the rest.
                        current_len = 1 + dfs(r, c, d, False, 2)
                        max_overall_len = max(max_overall_len, current_len)
                        
        return max_overall_len