from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        N = n * m

        # Flatten grid for fast 1D access.
        vals = [0] * N
        for r in range(n):
            base = r * m
            row = grid[r]
            for c in range(m):
                vals[base + c] = row[c]

        # A clockwise 90-degree turn is exactly i -> (i+1)%4 with this ordering.
        # (1,1)=down-right, (1,-1)=down-left, (-1,-1)=up-left, (-1,1)=up-right
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        cw = (1, 2, 3, 0)

        # g2[d][cell]/g0[d][cell] = length of the maximal alternating run strictly
        # AFTER `cell` in direction d, with next required value 2 / 0 (NO turn left).
        g2 = [None] * 4
        g0 = [None] * 4
        for i in range(4):
            dr, dc = dirs[i]
            a2 = array('H', [0]) * N
            a0 = array('H', [0]) * N
            r_range = range(n - 1, -1, -1) if dr == 1 else range(n)
            c_range = range(m - 1, -1, -1) if dc == 1 else range(m)
            for r in r_range:
                base = r * m
                nr = r + dr
                if 0 <= nr < n:
                    nb = nr * m
                    for c in c_range:
                        nc = c + dc
                        if 0 <= nc < m:
                            ni = nb + nc
                            nv = vals[ni]
                            idx = base + c
                            if nv == 2:
                                a2[idx] = 1 + a0[ni]
                            elif nv == 0:
                                a0[idx] = 1 + a2[ni]
            g2[i] = a2
            g0[i] = a0

        ans = 0

        # h2[d][cell]/h0[d][cell] = max additional cells after `cell` in direction d,
        # with next required value 2 / 0, using AT MOST one clockwise turn.
        for i in range(4):
            dr, dc = dirs[i]
            cd = cw[i]
            dr2, dc2 = dirs[cd]
            g2_cd = g2[cd]
            g0_cd = g0[cd]
            h2 = [0] * N
            h0 = [0] * N

            r_range = range(n - 1, -1, -1) if dr == 1 else range(n)
            c_range = range(m - 1, -1, -1) if dc == 1 else range(m)

            for r in r_range:
                base = r * m
                nr = r + dr
                nr2 = r + dr2
                valid_n = 0 <= nr < n
                valid_n2 = 0 <= nr2 < n
                if valid_n:
                    nbase = nr * m
                if valid_n2:
                    nbase2 = nr2 * m
                for c in c_range:
                    idx = base + c
                    best2 = 0
                    best0 = 0
                    # option: continue straight (turn still unused)
                    if valid_n:
                        nc = c + dc
                        if 0 <= nc < m:
                            nidx = nbase + nc
                            nv = vals[nidx]
                            if nv == 2:
                                cand = 1 + h0[nidx]
                                if cand > best2:
                                    best2 = cand
                            elif nv == 0:
                                cand = 1 + h2[nidx]
                                if cand > best0:
                                    best0 = cand
                    # option: turn clockwise at the current cell, then no more turns
                    if valid_n2:
                        nc2 = c + dc2
                        if 0 <= nc2 < m:
                            nidx2 = nbase2 + nc2
                            nv2 = vals[nidx2]
                            if nv2 == 2:
                                cand = 1 + g0_cd[nidx2]
                                if cand > best2:
                                    best2 = cand
                            elif nv2 == 0:
                                cand = 1 + g2_cd[nidx2]
                                if cand > best0:
                                    best0 = cand
                    h2[idx] = best2
                    h0[idx] = best0
                    if vals[idx] == 1:
                        cand = 1 + best2
                        if cand > ans:
                            ans = cand

        return ans