from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        
        n = len(grid)
        m = len(grid[0])
        
        # Directions: (dr, dc)
        # 0: Top-Left to Bottom-Right (DR)  -> (1, 1)
        # 1: Bottom-Right to Top-Left (UL)  -> (-1, -1)
        # 2: Top-Right to Bottom-Left (DL)  -> (1, -1)
        # 3: Bottom-Left to Top-Right (UR)  -> (-1, 1)
        directions = [
            (1, 1),   # DR
            (-1, -1), # UL
            (1, -1),  # DL
            (-1, 1)   # UR
        ]
        
        # Clockwise mapping logic:
        # DR (0) -> DL (2)
        # DL (2) -> UL (1)
        # UL (1) -> UR (3)
        # UR (3) -> DR (0)
        clockwise_map = [2, 3, 0, 1]
        
        max_len = 0
        
        # Iterate over every cell that is '1'
        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue
                
                # Try all 4 starting directions
                for start_dir in range(4):
                    dr, dc = directions[start_dir]
                    
                    # Traverse the first leg
                    curr_r, curr_c = r, c
                    seq_idx = 0 # 0 corresponds to '1'
                    
                    # We will try to turn at every valid step of the first leg
                    while 0 <= curr_r < n and 0 <= curr_c < m:
                        # Check if current cell matches the sequence value
                        expected_val = 1 if seq_idx == 0 else (2 if seq_idx % 2 == 1 else 0)
                        if grid[curr_r][curr_c] != expected_val:
                            break
                        
                        # At this cell (curr_r, curr_c), we can consider turning
                        turn_dir = clockwise_map[start_dir]
                        t_dr, t_dc = directions[turn_dir]
                        
                        # leg1_len is the number of cells visited in the first leg including current
                        leg1_len = seq_idx + 1
                        
                        # Check second leg starting from the next cell in turn_dir
                        tr, tc = curr_r + t_dr, curr_c + t_dc
                        leg2_len = 0
                        next_seq_idx = seq_idx + 1
                        
                        while 0 <= tr < n and 0 <= tc < m:
                            # Expected value for next_seq_idx
                            exp_val = 1 if next_seq_idx == 0 else (2 if next_seq_idx % 2 == 1 else 0)
                            if grid[tr][tc] != exp_val:
                                break
                            leg2_len += 1
                            next_seq_idx += 1
                            tr += t_dr
                            tc += t_dc
                        
                        total_len = leg1_len + leg2_len
                        if total_len > max_len:
                            max_len = total_len
                        
                        # Move to next cell in first leg
                        curr_r += dr
                        curr_c += dc
                        seq_idx += 1
                        
        return max_len