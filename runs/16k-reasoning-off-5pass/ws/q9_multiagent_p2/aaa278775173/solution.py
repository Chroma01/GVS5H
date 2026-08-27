from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0
        
        n, m = len(grid), len(grid[0])
        # Directions mapping to ensure clockwise turn logic (d -> (d+1)%4) works:
        # 0: (1, 1)  -> SE
        # 1: (1, -1) -> SW
        # 2: (-1, -1) -> NW
        # 3: (-1, 1) -> NE
        # Clockwise sequence: SE -> SW -> NW -> NE -> SE
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]
        
        # Memoization table: (r, c, d, turn_made, parity) -> max_length_from_here
        # parity: 1 means next value should be 2 (odd step), 0 means next value should be 0 (even step)
        # Sequence after '1': 2, 0, 2, 0...
        # Step 1 (first neighbor): expect 2 (parity=1)
        # Step 2: expect 0 (parity=0)
        memo = {}

        def get_next_val(parity: int) -> int:
            return 2 if parity == 1 else 0

        def dfs(r: int, c: int, d: int, turn_made: bool, parity: int) -> int:
            state = (r, c, d, turn_made, parity)
            if state in memo:
                return memo[state]
            
            if r < 0 or r >= n or c < 0 or c >= m:
                return 0
            
            val = grid[r][c]
            expected = get_next_val(parity)
            
            if val != expected:
                return 0
            
            res = 1
            
            # Option 1: Continue in same direction
            nr, nc = r + dirs[d][0], c + dirs[d][1]
            if 0 <= nr < n and 0 <= nc < m:
                res = max(res, 1 + dfs(nr, nc, d, turn_made, 1 - parity))
            
            # Option 2: Turn clockwise (only if not already turned)
            if not turn_made:
                nd = (d + 1) % 4
                nr, nc = r + dirs[nd][0], c + dirs[nd][1]
                if 0 <= nr < n and 0 <= nc < m:
                    res = max(res, 1 + dfs(nr, nc, nd, True, 1 - parity))
            
            memo[state] = res
            return res

        max_len = 0
        has_one = False
        
        for i in range(n):
            for j in range(m):
                if grid[i][j] == 1:
                    has_one = True
                    # If the grid is just [[1]], max_len should be 1.
                    # The loop below only updates if there is a valid neighbor.
                    if n == 1 and m == 1:
                        max_len = max(max_len, 1)
                    else:
                        for d in range(4):
                            nr, nc = i + dirs[d][0], j + dirs[d][1]
                            if 0 <= nr < n and 0 <= nc < m:
                                # Start DFS from neighbor. 
                                # This neighbor is step 1, so parity = 1 (expect 2).
                                path_len = dfs(nr, nc, d, False, 1)
                                max_len = max(max_len, path_len + 1)
        
        return max_len if has_one else 0