class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        
        # Directions: NE, SE, SW, NW
        # NE: (-1, 1), SE: (1, 1), SW: (1, -1), NW: (-1, -1)
        dirs = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
        dir_names = ['NE', 'SE', 'SW', 'NW']
        
        # Precompute dp2[r][c][d]: length of longest sequence starting at (r,c) in direction d
        # that matches 2,0,2,0,... (i.e., grid[r][c] must be 2, then 0, etc.)
        # Precompute dp0[r][c][d]: length of longest sequence starting at (r,c) in direction d
        # that matches 0,2,0,2,... (i.e., grid[r][c] must be 0, then 2, etc.)
        
        dp2 = [[[0]*4 for _ in range(m)] for _ in range(n)]
        dp0 = [[[0]*4 for _ in range(m)] for _ in range(n)]
        
        # We fill DP tables in reverse order of traversal for each direction.
        # For direction d, we iterate from the end of the grid in that direction backwards.
        
        for d in range(4):
            dr, dc = dirs[d]
            # Determine iteration order: 
            # If dr > 0, iterate rows from n-1 down to 0; if dr < 0, iterate rows from 0 to n-1.
            # Similarly for dc.
            if dr > 0:
                row_order = range(n-1, -1, -1)
            else:
                row_order = range(n)
            if dc > 0:
                col_order = range(m-1, -1, -1)
            else:
                col_order = range(m)
            
            for r in row_order:
                for c in col_order:
                    # For dp2: current must be 2, next must be 0, then 2, etc.
                    if grid[r][c] == 2:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < m:
                            # Next should be 0, so we look at dp0[nr][nc][d]
                            dp2[r][c][d] = 1 + dp0[nr][nc][d]
                        else:
                            dp2[r][c][d] = 1
                    else:
                        dp2[r][c][d] = 0
                        
                    # For dp0: current must be 0, next must be 2, then 0, etc.
                    if grid[r][c] == 0:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < m:
                            # Next should be 2, so we look at dp2[nr][nc][d]
                            dp0[r][c][d] = 1 + dp2[nr][nc][d]
                        else:
                            dp0[r][c][d] = 1
                    else:
                        dp0[r][c][d] = 0
        
        # Clockwise turns: 
        # NE -> SE, SE -> SW, SW -> NW, NW -> NE
        # Index mapping: 0:NE, 1:SE, 2:SW, 3:NW
        # Clockwise: 0->1, 1->2, 2->3, 3->0
        clockwise_turns = {0: 1, 1: 2, 2: 3, 3: 0}
        
        max_len = 0
        
        # For each cell that is 1, try all 4 starting directions
        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue
                
                for d1 in range(4):
                    dr1, dc1 = dirs[d1]
                    # Extend in direction d1 as long as the sequence 1,2,0,2,0,... holds
                    # Start at (r,c) with value 1 (index 0)
                    # Next should be 2 (index 1), then 0 (index 2), etc.
                    
                    # We can simulate the extension
                    cur_r, cur_c = r, c
                    length = 1  # includes the starting 1
                    
                    # The next expected value after index i (0-indexed) is:
                    # i=0 (value 1) -> next is 2
                    # i=1 (value 2) -> next is 0
                    # i=2 (value 0) -> next is 2
                    # i=3 (value 2) -> next is 0
                    # So for i>=1: if i is odd -> 2, if i is even -> 0
                    
                    # Extend as far as possible
                    while True:
                        # Current index in sequence is length-1
                        idx = length - 1
                        # Expected next value
                        if idx == 0:
                            expected = 2
                        else:
                            if idx % 2 == 1:
                                expected = 0
                            else:
                                expected = 2
                        
                        nr, nc = cur_r + dr1, cur_c + dc1
                        if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == expected:
                            length += 1
                            cur_r, cur_c = nr, nc
                        else:
                            break
                    
                    # Now, the segment ends at (cur_r, cur_c) with length 'length'
                    # The last value in the sequence is at index 'length-1'
                    # Determine what value is expected next for a continuation (for the turn)
                    idx_last = length - 1
                    if idx_last == 0:
                        expected_next = 2
                    else:
                        if idx_last % 2 == 1:
                            expected_next = 0
                        else:
                            expected_next = 2
                    
                    # Update max_len with the straight segment (no turn)
                    if length > max_len:
                        max_len = length
                    
                    # Try all clockwise turns from d1
                    d2 = clockwise_turns[d1]
                    dr2, dc2 = dirs[d2]
                    
                    # Check the next cell in direction d2 from (cur_r, cur_c)
                    nr2, nc2 = cur_r + dr2, cur_c + dc2
                    if 0 <= nr2 < n and 0 <= nc2 < m:
                        if grid[nr2][nc2] == expected_next:
                            # Add the length of the chain starting from (nr2, nc2) in direction d2
                            if expected_next == 2:
                                suffix_len = dp2[nr2][nc2][d2]
                            else:
                                suffix_len = dp0[nr2][nc2][d2]
                            
                            total_len = length + suffix_len
                            if total_len > max_len:
                                max_len = total_len
        
        return max_len