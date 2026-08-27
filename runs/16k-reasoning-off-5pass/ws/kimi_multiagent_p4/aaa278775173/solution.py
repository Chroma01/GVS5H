from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # Directions in clockwise order:
        # 0: up-left, 1: up-right, 2: down-right, 3: down-left
        dirs = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        # f[d][p][i][j]: longest run starting at (i,j) going in direction d,
        # where grid[i][j] must equal (2 if p == 1 else 0), and subsequent
        # cells alternate. p here is the parity of the position index k
        # (k odd -> expect 2, k even -> expect 0).
        f = [[[0] * m for _ in range(n)] for _ in range(2)]
        f = [[f[0], f[1]] for _ in range(4)]  # f[d][p]

        for d in range(4):
            di, dj = dirs[d]
            # Iterate cells in reverse order along direction d so that the
            # "next" cell (i+di, j+dj) is computed before (i,j).
            if di > 0:
                irange = range(n - 1, -1, -1)
            else:
                irange = range(n)
            if dj > 0:
                jrange = range(m - 1, -1, -1)
            else:
                jrange = range(m)
            fd0 = f[d][0]
            fd1 = f[d][1]
            for i in irange:
                for j in jrange:
                    v = grid[i][j]
                    ni, nj = i + di, j + dj
                    nxt0 = nxt1 = 0
                    if 0 <= ni < n and 0 <= nj < m:
                        nxt0 = fd1[ni][nj]  # next position has opposite parity
                        nxt1 = fd0[ni][nj]
                    if v == 0:
                        fd0[i][j] = 1 + nxt0
                    # else fd0 stays 0
                    if v == 2:
                        fd1[i][j] = 1 + nxt1
                    # else fd1 stays 0

        ans = 0
        for i in range(n):
            for j in range(m):
                if grid[i][j] != 1:
                    continue
                for d in range(4):
                    di, dj = dirs[d]
                    nd = (d + 1) % 4
                    ndi, ndj = dirs[nd]
                    fnd = f[nd]
                    ci, cj = i, j
                    k = 0
                    while True:
                        # candidate without turn
                        cur = k + 1
                        if cur > ans:
                            ans = cur
                        # candidate with clockwise turn at (ci,cj):
                        # next position index k+1, parity (k+1)%2
                        ti, tj = ci + ndi, cj + ndj
                        if 0 <= ti < n and 0 <= tj < m:
                            cand = cur + fnd[(k + 1) & 1][ti][tj]
                            if cand > ans:
                                ans = cand
                        # advance along current direction
                        ni, nj = ci + di, cj + dj
                        if not (0 <= ni < n and 0 <= nj < m):
                            break
                        nk = k + 1
                        expected = 2 if (nk & 1) else 0
                        if grid[ni][nj] != expected:
                            break
                        ci, cj = ni, nj
                        k = nk
        return ans