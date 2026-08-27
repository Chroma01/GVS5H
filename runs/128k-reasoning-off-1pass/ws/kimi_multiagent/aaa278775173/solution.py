from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Diagonal directions in clockwise order:
        # 0: down-right, 1: down-left, 2: up-left, 3: up-right
        DIRS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # f[d][r][c] = length of the longest run starting at (r, c) going in
        # direction d such that values strictly alternate between 2 and 0
        # (starting with whatever value grid[r][c] has, as long as it is 0 or 2).
        f = [[[0] * m for _ in range(n)] for _ in range(4)]

        for d in range(4):
            dr, dc = DIRS[d]
            fd = f[d]
            # Iterate cells in the order opposite to the movement direction so
            # that the "next" cell is always computed before the current one.
            rows = range(n - 1, -1, -1) if dr == 1 else range(n)
            cols = range(m - 1, -1, -1) if dc == 1 else range(m)
            for r in rows:
                gr = grid[r]
                fdr = fd[r]
                for c in cols:
                    v = gr[c]
                    if v == 1:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == (2 - v):
                        fdr[c] = fd[nr][nc] + 1
                    else:
                        fdr[c] = 1

        # g[d][r][c] = length of the longest run starting at (r, c) going in
        # direction d, alternating 2/0, and allowed to make at most one
        # clockwise 90-degree turn at some later cell.
        g = [[[0] * m for _ in range(n)] for _ in range(4)]

        for d in range(4):
            dr, dc = DIRS[d]
            cdr, cdc = DIRS[(d + 1) % 4]  # clockwise direction
            fd_cw = f[(d + 1) % 4]
            gd = g[d]
            rows = range(n - 1, -1, -1) if dr == 1 else range(n)
            cols = range(m - 1, -1, -1) if dc == 1 else range(m)
            for r in rows:
                gr = grid[r]
                gdr = gd[r]
                for c in cols:
                    v = gr[c]
                    if v == 1:
                        continue
                    nxt_val = 2 - v
                    best = 0
                    # Continue straight (may still turn later).
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == nxt_val:
                        best = gd[nr][nc]
                    # Turn clockwise right after this cell (straight run only).
                    tr, tc = r + cdr, c + cdc
                    if 0 <= tr < n and 0 <= tc < m and grid[tr][tc] == nxt_val:
                        if fd_cw[tr][tc] > best:
                            best = fd_cw[tr][tc]
                    gdr[c] = best + 1

        ans = 0
        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue
                # Segment consisting of just this cell.
                if ans < 1:
                    ans = 1
                for d in range(4):
                    dr, dc = DIRS[d]
                    cdr, cdc = DIRS[(d + 1) % 4]
                    # Go straight first (turn may happen at any later cell).
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 2:
                        cand = 1 + g[d][nr][nc]
                        if cand > ans:
                            ans = cand
                    # Turn clockwise immediately at the starting cell.
                    tr, tc = r + cdr, c + cdc
                    if 0 <= tr < n and 0 <= tc < m and grid[tr][tc] == 2:
                        cand = 1 + f[(d + 1) % 4][tr][tc]
                        if cand > ans:
                            ans = cand
        return ans