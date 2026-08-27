from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        n, m = len(grid), len(grid[0])
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))  # DR, DL, UL, UR
        nxt = (2, 2, 0)                              # next value after 0, 1, 2
        ans = 0
        g = grid

        for d in range(4):
            dr, dc = dirs[d]
            odr, odc = dirs[(d + 1) % 4]  # clockwise outgoing direction

            # F[i][j]: longest straight continuation starting at (i,j)
            # in the outgoing direction, counting (i,j).
            F = [[1] * m for _ in range(n)]
            f_rows = range(n - 1, -1, -1) if odr > 0 else range(n)
            f_cols = range(m - 1, -1, -1) if odc > 0 else range(m)

            for i in f_rows:
                gi = g[i]
                Fi = F[i]
                ni = i + odr
                if 0 <= ni < n:
                    gni = g[ni]
                    Fni = F[ni]
                    for j in f_cols:
                        nj = j + odc
                        if 0 <= nj < m and gni[nj] == nxt[gi[j]]:
                            Fi[j] = Fni[nj] + 1

            # B[i][j]: longest valid straight prefix ending at (i,j)
            # in the incoming direction, enforcing that it started with 1.
            B = [[0] * m for _ in range(n)]
            b_rows = range(n) if dr > 0 else range(n - 1, -1, -1)
            b_cols = range(m) if dc > 0 else range(m - 1, -1, -1)

            for i in b_rows:
                gi = g[i]
                Bi = B[i]
                Fi = F[i]
                pi = i - dr

                if 0 <= pi < n:
                    gpi = g[pi]
                    Bpi = B[pi]
                    for j in b_cols:
                        val = gi[j]
                        if val == 1:
                            Bi[j] = 1
                        else:
                            pj = j - dc
                            if 0 <= pj < m:
                                prev_len = Bpi[pj]
                                if prev_len > 0 and val == nxt[gpi[pj]]:
                                    Bi[j] = prev_len + 1

                        blen = Bi[j]
                        if blen > 0:
                            total = blen + Fi[j] - 1
                            if total > ans:
                                ans = total
                else:
                    for j in b_cols:
                        if gi[j] == 1:
                            Bi[j] = 1
                            total = Fi[j]
                            if total > ans:
                                ans = total

        return ans