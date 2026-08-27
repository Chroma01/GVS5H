from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        if n == 0:
            return 0
        m = len(grid[0])
        
        # Direction vectors: (dr, dc)
        # 0: Top-Left to Bottom-Right (1, 1)
        # 1: Bottom-Right to Top-Left (-1, -1)
        # 2: Top-Right to Bottom-Left (1, -1)
        # 3: Bottom-Left to Top-Right (-1, 1)
        dirs = [(1, 1), (-1, -1), (1, -1), (-1, 1)]
        
        # Clockwise mapping:
        # 0 (1,1) -> 2 (1,-1)
        # 2 (1,-1) -> 1 (-1,-1)
        # 1 (-1,-1) -> 3 (-1,1)
        # 3 (-1,1) -> 0 (1,1)
        clockwise = [2, 3, 1, 0]
        
        # dp[r][c][dir] stores the length of the sequence ending at (r,c) coming from direction 'dir'
        dp = [[[0] * 4 for _ in range(m)] for _ in range(n)]
        
        # Pass 0: Direction 0 (1, 1) - Iterate forward
        for r in range(n):
            for c in range(m):
                if grid[r][c] == 1:
                    dp[r][c][0] = 1
                elif grid[r][c] == 2:
                    pr, pc = r - 1, c - 1
                    if pr >= 0 and pc >= 0 and dp[pr][pc][0] > 0:
                        dp[r][c][0] = dp[pr][pc][0] + 1
                elif grid[r][c] == 0:
                    pr, pc = r - 1, c - 1
                    if pr >= 0 and pc >= 0 and dp[pr][pc][0] > 0:
                        dp[r][c][0] = dp[pr][pc][0] + 1
        
        # Pass 1: Direction 1 (-1, -1) - Iterate backward
        for r in range(n - 1, -1, -1):
            for c in range(m - 1, -1, -1):
                if grid[r][c] == 1:
                    dp[r][c][1] = 1
                elif grid[r][c] == 2:
                    pr, pc = r + 1, c + 1
                    if pr < n and pc < m and dp[pr][pc][1] > 0:
                        dp[r][c][1] = dp[pr][pc][1] + 1
                elif grid[r][c] == 0:
                    pr, pc = r + 1, c + 1
                    if pr < n and pc < m and dp[pr][pc][1] > 0:
                        dp[r][c][1] = dp[pr][pc][1] + 1
                        
        # Pass 2: Direction 2 (1, -1) - Iterate forward rows, backward cols
        for r in range(n):
            for c in range(m - 1, -1, -1):
                if grid[r][c] == 1:
                    dp[r][c][2] = 1
                elif grid[r][c] == 2:
                    pr, pc = r + 1, c - 1
                    if pr < n and pc >= 0 and dp[pr][pc][2] > 0:
                        dp[r][c][2] = dp[pr][pc][2] + 1
                elif grid[r][c] == 0:
                    pr, pc = r + 1, c - 1
                    if pr < n and pc >= 0 and dp[pr][pc][2] > 0:
                        dp[r][c][2] = dp[pr][pc][2] + 1
                        
        # Pass 3: Direction 3 (-1, 1) - Iterate backward rows, forward cols
        for r in range(n - 1, -1, -1):
            for c in range(m):
                if grid[r][c] == 1:
                    dp[r][c][3] = 1
                elif grid[r][c] == 2:
                    pr, pc = r - 1, c + 1
                    if pr >= 0 and pc < m and dp[pr][pc][3] > 0:
                        dp[r][c][3] = dp[pr][pc][3] + 1
                elif grid[r][c] == 0:
                    pr, pc = r - 1, c + 1
                    if pr >= 0 and pc < m and dp[pr][pc][3] > 0:
                        dp[r][c][3] = dp[pr][pc][3] + 1
                        
        # dp_start[r][c][dir] stores the length of the sequence starting at (r,c) going in direction 'dir'
        dp_start = [[[0] * 4 for _ in range(m)] for _ in range(n)]
        
        # Pass 0: Direction 0 (1, 1) - Iterate backward
        for r in range(n - 1, -1, -1):
            for c in range(m - 1, -1, -1):
                if grid[r][c] == 1:
                    dp_start[r][c][0] = 1
                elif grid[r][c] == 2:
                    nr, nc = r + 1, c + 1
                    if nr < n and nc < m and grid[nr][nc] == 0 and dp_start[nr][nc][0] > 0:
                        dp_start[r][c][0] = 1 + dp_start[nr][nc][0]
                elif grid[r][c] == 0:
                    nr, nc = r + 1, c + 1
                    if nr < n and nc < m and grid[nr][nc] == 2 and dp_start[nr][nc][0] > 0:
                        dp_start[r][c][0] = 1 + dp_start[nr][nc][0]
                        
        # Pass 1: Direction 1 (-1, -1) - Iterate forward
        for r in range(n):
            for c in range(m):
                if grid[r][c] == 1:
                    dp_start[r][c][1] = 1
                elif grid[r][c] == 2:
                    nr, nc = r - 1, c - 1
                    if nr >= 0 and nc >= 0 and grid[nr][nc] == 0 and dp_start[nr][nc][1] > 0:
                        dp_start[r][c][1] = 1 + dp_start[nr][nc][1]
                elif grid[r][c] == 0:
                    nr, nc = r - 1, c - 1
                    if nr >= 0 and nc >= 0 and grid[nr][nc] == 2 and dp_start[nr][nc][1] > 0:
                        dp_start[r][c][1] = 1 + dp_start[nr][nc][1]
                        
        # Pass 2: Direction 2 (1, -1) - Iterate backward
        for r in range(n - 1, -1, -1):
            for c in range(m):
                if grid[r][c] == 1:
                    dp_start[r][c][2] = 1
                elif grid[r][c] == 2:
                    nr, nc = r + 1, c - 1
                    if nr < n and nc >= 0 and grid[nr][nc] == 0 and dp_start[nr][nc][2] > 0:
                        dp_start[r][c][2] = 1 + dp_start[nr][nc][2]
                elif grid[r][c] == 0:
                    nr, nc = r + 1, c - 1
                    if nr < n and nc >= 0 and grid[nr][nc] == 2 and dp_start[nr][nc][2] > 0:
                        dp_start[r][c][2] = 1 + dp_start[nr][nc][2]
                        
        # Pass 3: Direction 3 (-1, 1) - Iterate forward
        for r in range(n):
            for c in range(m - 1, -1, -1):
                if grid[r][c] == 1:
                    dp_start[r][c][3] = 1
                elif grid[r][c] == 2:
                    nr, nc = r - 1, c + 1
                    if nr >= 0 and nc < m and grid[nr][nc] == 0 and dp_start[nr][nc][3] > 0:
                        dp_start[r][c][3] = 1 + dp_start[nr][nc][3]
                elif grid[r][c] == 0:
                    nr, nc = r - 1, c + 1
                    if nr >= 0 and nc < m and grid[nr][nc] == 2 and dp_start[nr][nc][3] > 0:
                        dp_start[r][c][3] = 1 + dp_start[nr][nc][3]
                        
        max_len = 0
        
        # Check for straight segments
        for r in range(n):
            for c in range(m):
                for d in range(4):
                    if dp[r][c][d] > max_len:
                        max_len = dp[r][c][d]
                        
        # Check for V-shapes (one clockwise turn)
        for r in range(n):
            for c in range(m):
                for d_in in range(4):
                    if dp[r][c][d_in] > 0:
                        d_out = clockwise[d_in]
                        if dp_start[r][c][d_out] > 0:
                            length = dp[r][c][d_in] + dp_start[r][c][d_out] - 1
                            if length > max_len:
                                max_len = length
                                
        return max_len