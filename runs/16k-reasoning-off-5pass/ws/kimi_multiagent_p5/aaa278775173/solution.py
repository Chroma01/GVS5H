from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])

        # Diagonal unit vectors ordered so that (d+1)%4 is the 90-degree
        # clockwise rotation of d: (dr,dc) -> (dc,-dr).
        DIRS = ((1, 1), (1, -1), (-1, -1), (-1, 1))

        # fe[d][i][j]: longest valid chain ending at (i,j) arriving along
        # direction d whose last step index is even (chain length odd).
        # fo[d][i][j]: same with odd last step index (chain length even).
        # A chain always starts at a cell with value 1 (step index 0, even).
        fe = [[[0] * m for _ in range(n)] for _ in range(4)]
        fo = [[[0] * m for _ in range(n)] for _ in range(4)]

        # ge[d][i][j]: longest continuation starting at (i,j) moving along
        # direction d where the NEXT cell (one step away) must have an even
        # step index (i.e. value 0). Length counts (i,j) itself.
        # go[d][i][j]: same but the next cell must have an odd step index
        # (value 2).
        ge = [[[0] * m for _ in range(n)] for _ in range(4)]
        go = [[[0] * m for _ in range(n)] for _ in range(4)]

        ans = 0

        for d in range(4):
            dr, dc = DIRS[d]
            fe_d = fe[d]
            fo_d = fo[d]
            ge_d = ge[d]
            go_d = go[d]

            # Row order so that the predecessor (i-dr, j-dc) is already done.
            if dr == 1:
                rows = range(n)
            else:
                rows = range(n - 1, -1, -1)

            for i in rows:
                fe_row = fe_d[i]
                fo_row = fo_d[i]
                ge_row = ge_d[i]
                go_row = go_d[i]
                g_row = grid[i]

                # Column order so that the predecessor is already done.
                if dc == 1:
                    cols = range(m)
                else:
                    cols = range(m - 1, -1, -1)

                pi = i - dr
                gi = i + dr
                pi_in = 0 <= pi < n
                gi_in = 0 <= gi < n
                if pi_in:
                    fe_prev = fe_d[pi]
                    fo_prev = fo_d[pi]
                if gi_in:
                    ge_next = ge_d[gi]
                    go_next = go_d[gi]

                for j in cols:
                    v = g_row[j]
                    if v == 1:
                        fe_row[j] = 1
                        # fo_row[j] stays 0
                    else:
                        pj = j - dc
                        if pi_in and 0 <= pj < m:
                            if v == 2:
                                # value 2 sits at odd step index -> follows even
                                pe = fe_prev[pj]
                                if pe:
                                    fo_row[j] = pe + 1
                            else:  # v == 0
                                # value 0 sits at even step index -> follows odd
                                po = fo_prev[pj]
                                if po:
                                    fe_row[j] = po + 1

                    # Continuation DP (successor (i+dr, j+dc) already computed
                    # because it was processed earlier in this traversal).
                    nj = j + dc
                    if gi_in and 0 <= nj < m:
                        nv = grid[gi][nj]
                        if nv == 0:
                            # next cell has even step index -> its next is odd
                            ge_row[j] = go_next[nj] + 1
                        elif nv == 2:
                            # next cell has odd step index -> its next is even
                            go_row[j] = ge_next[nj] + 1

                    # Combine: first leg along d ending here, optional
                    # clockwise turn into direction d2 = (d+1)%4.
                    e = fe_row[j]
                    if e:
                        if e > ans:
                            ans = e
                        # last step index even -> next must be odd (value 2)
                        s = go[(d + 1) & 3][i][j]
                        if s:
                            tot = e + s - 1
                            if tot > ans:
                                ans = tot
                    o = fo_row[j]
                    if o:
                        if o > ans:
                            ans = o
                        # last step index odd -> next must be even (value 0)
                        s = ge[(d + 1) & 3][i][j]
                        if s:
                            tot = o + s - 1
                            if tot > ans:
                                ans = tot

        return ans