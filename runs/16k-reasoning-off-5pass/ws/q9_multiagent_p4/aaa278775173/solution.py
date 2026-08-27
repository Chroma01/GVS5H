from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0
        
        n = len(grid)
        m = len(grid[0])
        
        # Directions defined to ensure clockwise rotation order:
        # 0: TL->BR (dr=1, dc=1)
        # 1: TR->BL (dr=1, dc=-1)
        # 2: BR->TL (dr=-1, dc=-1)  <-- Corrected for clockwise sequence
        # 3: BL->TR (dr=-1, dc=1)   <-- Corrected for clockwise sequence
        # Clockwise turn mapping: 0->1, 1->2, 2->3, 3->0
        dr = [1, 1, -1, -1]
        dc = [1, -1, -1, 1]
        
        max_len = 0
        
        # Check if there are any '1's
        has_one = False
        for r in range(n):
            for c in range(m):
                if grid[r][c] == 1:
                    has_one = True
                    break
            if has_one:
                break
        
        if not has_one:
            return 0
        
        # Iterative DFS for each starting '1'
        # Stack elements: (r, c, direction, steps_after_start, turn_made)
        # steps_after_start: number of cells visited after the initial '1'
        # turn_made: boolean indicating if a clockwise turn has already occurred
        
        for r in range(n):
            for c in range(m):
                if grid[r][c] == 1:
                    # Start DFS from this cell
                    # Initial state: at (r, c), 0 steps taken after start, no turn made.
                    # We can try starting in any of the 4 directions.
                    
                    stack = []
                    for d in range(4):
                        stack.append((r, c, d, 0, False))
                    
                    while stack:
                        curr_r, curr_c, curr_dir, steps, turn_made = stack.pop()
                        
                        # Current length is steps + 1 (including the starting '1')
                        current_len = steps + 1
                        if current_len > max_len:
                            max_len = current_len
                        
                        # Determine expected next value
                        # Sequence: 1 (start), then 2, 0, 2, 0...
                        # steps=0 (next is 1st element after start) -> expect 2
                        # steps=1 (next is 2nd element after start) -> expect 0
                        # So if steps is even, expect 2; if odd, expect 0.
                        expected_val = 2 if steps % 2 == 0 else 0
                        
                        # Try to continue in current direction
                        next_r, next_c = curr_r + dr[curr_dir], curr_c + dc[curr_dir]
                        if 0 <= next_r < n and 0 <= next_c < m:
                            if grid[next_r][next_c] == expected_val:
                                # Continue without turn
                                stack.append((next_r, next_c, curr_dir, steps + 1, turn_made))
                        
                        # Try to turn clockwise if not already turned
                        if not turn_made:
                            new_dir = (curr_dir + 1) % 4
                            next_r, next_c = curr_r + dr[new_dir], curr_c + dc[new_dir]
                            if 0 <= next_r < n and 0 <= next_c < m:
                                if grid[next_r][next_c] == expected_val:
                                    stack.append((next_r, next_c, new_dir, steps + 1, True))
        
        return max_len