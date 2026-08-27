from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        
        n = len(grid)
        m = len(grid[0])
        
        # Directions: (dr, dc)
        # 0: Top-Left to Bottom-Right (1, 1)
        # 1: Bottom-Right to Top-Left (-1, -1)
        # 2: Top-Right to Bottom-Left (1, -1)
        # 3: Bottom-Left to Top-Left (-1, 1)
        directions = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        
        # Clockwise 90-degree turn mapping for each direction index
        # (1, 1) -> (1, -1) [0 -> 2]
        # (-1, -1) -> (-1, 1) [1 -> 3]
        # (1, -1) -> (-1, -1) [2 -> 1]
        # (-1, 1) -> (1, 1) [3 -> 0]
        clockwise_turn = [2, 3, 1, 0]
        
        # Sequence values: index 0 -> 1, index 1 -> 2, index 2 -> 0, index 3 -> 2, ...
        # The sequence is 1, 2, 0, 2, 0, ...
        seq = [1, 2, 0]
        
        max_len = 0
        
        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue
                
                # Start a new path from (r, c) with value 1
                # Try all 4 initial directions
                for start_dir in range(4):
                    curr_r, curr_c = r, c
                    curr_dir = start_dir
                    turned = False
                    length = 1  # Current path length (number of cells visited)
                    
                    while True:
                        # We are currently at step 'length - 1' (0-indexed).
                        # We need to move to step 'length'.
                        # The value required at step 'length' is seq[length % 3].
                        next_val = seq[length % 3]
                        
                        # Calculate next position in current direction
                        dr, dc = directions[curr_dir]
                        next_r, next_c = curr_r + dr, curr_c + dc
                        
                        # Check bounds
                        if not (0 <= next_r < n and 0 <= next_c < m):
                            break
                        
                        # Check value match
                        if grid[next_r][next_c] != next_val:
                            break
                        
                        # Move to next cell
                        curr_r, curr_c = next_r, next_c
                        length += 1
                        
                        # Check if we can turn (only if not already turned)
                        if not turned:
                            new_dir = clockwise_turn[curr_dir]
                            # Calculate position after turn from current cell
                            dr_turn, dc_turn = directions[new_dir]
                            turn_r, turn_c = curr_r + dr_turn, curr_c + dc_turn
                            
                            # Check bounds for the turn
                            if not (0 <= turn_r < n and 0 <= turn_c < m):
                                break
                            
                            # Check value match for the step after turn
                            # The step index is now 'length' (since we just incremented)
                            val_after_turn = seq[length % 3]
                            
                            if grid[turn_r][turn_c] == val_after_turn:
                                # Turn is valid
                                curr_dir = new_dir
                                curr_r, curr_c = turn_r, turn_c
                                length += 1
                                turned = True
                            else:
                                # Turn not possible due to value mismatch
                                break
                        else:
                            # Already turned, just continue straight
                            pass
                    
                    if length > max_len:
                        max_len = length
                        
        return max_len