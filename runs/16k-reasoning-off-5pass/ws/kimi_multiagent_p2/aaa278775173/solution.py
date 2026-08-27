from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Directions: 0: down-right, 1: down-left, 2: up-left, 3: up-right
        # Clockwise 90-degree turn: (dr, dc) -> (dc, -dr)
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # dp0[d][i][j]: max length of valid segment ending at (i,j) with direction d, 0 turns used
        # dp1[d][i][j]: max length of valid segment ending at (i,j) with direction d, 1 turn used
        dp0 = [[[0] * m for _ in range(n)] for _ in range(4)]
        dp1 = [[[0] * m for _ in range(n)] for _ in range(4)]
        
        ans = 0
        
        for d in range(4):
            dr, dc = dirs[d]
            # Previous direction (d-1) is the one that turns clockwise into d
            pd = (d - 1 + 4) % 4
            pdr, pdc = dirs[pd]
            
            # Determine iteration order so that predecessors are processed first
            if dr == 1:
                i_range = range(n)
            else:
                i_range = range(n - 1, -1, -1)
            
            if dc == 1:
                j_range = range(m)
            else:
                j_range = range(m - 1, -1, -1)
                
            for i in i_range:
                for j in j_range:
                    val = grid[i][j]
                    
                    # Case 1: Start a new segment at (i,j)
                    if val == 1:
                        dp0[d][i][j] = 1
                        if 1 > ans:
                            ans = 1
                    
                    # Case 2: Continue straight from predecessor in direction d
                    pi, pj = i - dr, j - dc
                    if 0 <= pi < n and 0 <= pj < m:
                        # From dp0 (0 turns -> 0 turns)
                        prev_len = dp0[d][pi][pj]
                        if prev_len > 0:
                            # Next position is prev_len + 1.
                            # If even, expect 2. If odd (and >1), expect 0.
                            expected = 2 if (prev_len + 1) % 2 == 0 else 0
                            if val == expected:
                                new_len = prev_len + 1
                                if new_len > dp0[d][i][j]:
                                    dp0[d][i][j] = new_len
                                if new_len > ans:
                                    ans = new_len
                        
                        # From dp1 (1 turn -> 1 turn)
                        prev_len = dp1[d][pi][pj]
                        if prev_len > 0:
                            expected = 2 if (prev_len + 1) % 2 == 0 else 0
                            if val == expected:
                                new_len = prev_len + 1
                                if new_len > dp1[d][i][j]:
                                    dp1[d][i][j] = new_len
                                if new_len > ans:
                                    ans = new_len

                    # Case 3: Turn clockwise from direction pd to d at (i,j)
                    # Predecessor is in direction pd
                    pi, pj = i - pdr, j - pdc
                    if 0 <= pi < n and 0 <= pj < m:
                        prev_len = dp0[pd][pi][pj]
                        if prev_len > 0:
                            expected = 2 if (prev_len + 1) % 2 == 0 else 0
                            if val == expected:
                                new_len = prev_len + 1
                                if new_len > dp1[d][i][j]:
                                    dp1[d][i][j] = new_len
                                if new_len > ans:
                                    ans = new_len
                                    
        return ans