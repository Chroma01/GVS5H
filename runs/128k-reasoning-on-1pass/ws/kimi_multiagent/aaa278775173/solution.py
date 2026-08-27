from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Clockwise diagonal cycle (rows increase downward):
        # down-right -> down-left -> up-left -> up-right -> back to down-right
        dirs = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # f[d][p][i][j]: longest valid run STARTING at (i,j) in direction d,
        # where the cell at offset k must be 2 if (p+k) is odd, else 0.
        # (p=1 means the first cell must be 2, p=0 means it must be 0.)
        f = [[None, None] for _ in range(4)]
        for d in range(4):
            di, dj = dirs[d]
            f0 = [[0] * m for _ in range(n)]
            f1 = [[0] * m for _ in range(n)]
            # Process so that the next cell (i+di, j+dj) is already computed.
            rows = range(n - 1, -1, -1) if di == 1 else range(n)
            cols = range(m - 1, -1, -1) if dj == 1 else range(m)
            for i in rows:
                for j in cols:
                    ni = i + di
                    nj = j + dj
                    inside = 0 <= ni < n and 0 <= nj < m
                    v = grid[i][j]
                    if v == 0:
                        f0[i][j] = 1 + (f1[ni][nj] if inside else 0)
                    elif v == 2:
                        f1[i][j] = 1 + (f0[ni][nj] if inside else 0)
            f[d][0] = f0
            f[d][1] = f1

        ans = 0
        # h[i][j]: length of THE valid segment (1,2,0,2,0,...) ENDING at (i,j)
        # while moving in direction d (0 if none). It is unique because a '1'
        # can only appear at index 0 of a valid segment.
        for d in range(4):
            di, dj = dirs[d]
            nd = (d + 1) % 4          # clockwise 90-degree turn
            ndi, ndj = dirs[nd]
            fnd0 = f[nd][0]
            fnd1 = f[nd][1]
            h = [[0] * m for _ in range(n)]
            # Process so that the previous cell (i-di, j-dj) is already computed.
            rows = range(n) if di == 1 else range(n - 1, -1, -1)
            cols = range(m) if dj == 1 else range(m - 1, -1, -1)
            for i in rows:
                hrow = h[i]
                grow = grid[i]
                for j in cols:
                    v = grow[j]
                    if v == 1:
                        L = 1
                    else:
                        pi = i - di
                        pj = j - dj
                        L = 0
                        if 0 <= pi < n and 0 <= pj < m:
                            Lp = h[pi][pj]
                            if Lp:
                                # (i,j) would be index Lp: expect 2 if Lp odd else 0
                                if Lp & 1:
                                    if v == 2:
                                        L = Lp + 1
                                else:
                                    if v == 0:
                                        L = Lp + 1
                    hrow[j] = L
                    # No-turn (straight) candidate
                    if L > ans:
                        ans = L
                    # One-turn candidate: pivot at (i,j), continue clockwise
                    # from the next cell; next index is L, so required parity
                    # is L % 2 (odd -> expect 2, even -> expect 0).
                    if L:
                        qi = i + ndi
                        qj = j + ndj
                        if 0 <= qi < n and 0 <= qj < m:
                            cont = fnd1[qi][qj] if (L & 1) else fnd0[qi][qj]
                            total = L + cont
                            if total > ans:
                                ans = total
        return ans