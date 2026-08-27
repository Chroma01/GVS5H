from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        DIRS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]  # index+1 mod 4 = clockwise turn

        # f[d][r][c] = length of longest alternating (2,0,2,0...) run starting at
        # (r,c) going in direction d, where grid[r][c] itself may be 2 or 0
        # (0 if grid[r][c] == 1). The expected value at (r,c) is implied by its
        # actual value; callers check grid value matches the required phase.
        f = []
        for dr, dc in DIRS:
            tab = [[0] * m for _ in range(n)]
            r_iter = range(n - 1, -1, -1) if dr == 1 else range(n)
            c_iter = range(m - 1, -1, -1) if dc == 1 else range(m)
            for r in r_iter:
                row_g = grid[r]
                row_f = tab[r]
                for c in c_iter:
                    v = row_g[c]
                    if v == 1:
                        continue  # stays 0
                    nr, nc = r + dr, c + dc
                    best = 1
                    if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 2 - v:
                        best = tab[nr][nc] + 1
                    row_f[c] = best
            f.append(tab)

        ans = 0

        # No-turn candidates: start at a 1, go straight in direction d.
        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue
                if ans < 1:
                    ans = 1
                for k in range(4):
                    dr, dc = DIRS[k]
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 2:
                        cand = 1 + f[k][nr][nc]
                        if cand > ans:
                            ans = cand

        # Turn candidates: for each incoming direction d, sweep forward computing
        # leg[r][c] = longest valid first leg (cells after the starting 1) ending
        # at (r,c) arriving from direction d, with correct phase (1 -> 2 -> 0 ...).
        for k in range(4):
            dr, dc = DIRS[k]
            ndr, ndc = DIRS[(k + 1) % 4]  # clockwise turn direction
            f_next = f[(k + 1) % 4]
            leg = [[0] * m for _ in range(n)]
            r_iter = range(n) if dr == 1 else range(n - 1, -1, -1)
            c_iter = range(m) if dc == 1 else range(m - 1, -1, -1)
            for r in r_iter:
                row_g = grid[r]
                row_leg = leg[r]
                for c in c_iter:
                    v = row_g[c]
                    if v == 1:
                        continue  # leg stays 0
                    pr, pc = r - dr, c - dc
                    L = 0
                    if 0 <= pr < n and 0 <= pc < m:
                        pv = grid[pr][pc]
                        if v == 2:
                            if pv == 1:
                                L = 1
                            elif pv == 0 and leg[pr][pc] > 0:
                                L = leg[pr][pc] + 1
                        else:  # v == 0
                            if pv == 2 and leg[pr][pc] > 0:
                                L = leg[pr][pc] + 1
                    if L == 0:
                        continue
                    row_leg[c] = L
                    # Turn clockwise at (r,c); continuation must start with the
                    # alternation counterpart of v.
                    nr, nc = r + ndr, c + ndc
                    cont = 0
                    if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == 2 - v:
                        cont = f_next[nr][nc]
                    cand = 1 + L + cont
                    if cand > ans:
                        ans = cand

        return ans