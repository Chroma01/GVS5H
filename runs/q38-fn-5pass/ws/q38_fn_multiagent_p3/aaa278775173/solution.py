from typing import List
from array import array

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        n = len(grid)
        m = len(grid[0])
        size = n * m

        flat = bytearray()
        for row in grid:
            flat.extend(row)

        if 1 not in flat:
            return 0
        if 2 not in flat:
            return 1

        ans = 1

        # Directions: SE, SW, NW, NE
        dr = (1, 1, -1, -1)
        dc = (1, -1, -1, 1)

        # Clockwise turn: SE -> SW -> NW -> NE -> SE
        cw = (1, 2, 3, 0)

        # Process each direction backwards along its row delta so that the
        # next cell in the same direction is already computed.
        row_ranges = (
            range(n - 1, -1, -1),
            range(n - 1, -1, -1),
            range(n),
            range(n),
        )
        col_ranges = (
            range(m - 1, -1, -1),
            range(m),
            range(m),
            range(m - 1, -1, -1),
        )

        # straight[d][p][cell]:
        #   p = 0 -> current cell must be 2
        #   p = 1 -> current cell must be 0
        # Maximum straight diagonal run starting at cell in direction d.
        straight = [None] * 4

        for d in range(4):
            arr0 = array('H', [0]) * size
            arr1 = array('H', [0]) * size

            drd = dr[d]
            dcd = dc[d]
            rr = row_ranges[d]
            cr = col_ranges[d]

            for i in rr:
                base = i * m
                ni = i + drd

                if 0 <= ni < n:
                    nbase = ni * m
                    for j in cr:
                        idx = base + j
                        nj = j + dcd
                        if 0 <= nj < m:
                            nidx = nbase + nj
                        else:
                            nidx = -1

                        v = flat[idx]
                        if v == 2:
                            if nidx >= 0:
                                arr0[idx] = arr1[nidx] + 1
                            else:
                                arr0[idx] = 1
                        elif v == 0:
                            if nidx >= 0:
                                arr1[idx] = arr0[nidx] + 1
                            else:
                                arr1[idx] = 1
                else:
                    for j in cr:
                        idx = base + j
                        v = flat[idx]
                        if v == 2:
                            arr0[idx] = 1
                        elif v == 0:
                            arr1[idx] = 1

            straight[d] = (arr0, arr1)

        # dp0/dp1 are allocated per direction to keep memory compact.
        # dp0[cell]: best continuation if this cell must be 2, no turn used yet.
        # dp1[cell]: best continuation if this cell must be 0, no turn used yet.
        for d in range(4):
            dp0 = array('H', [0]) * size
            dp1 = array('H', [0]) * size

            cd = cw[d]
            st_cw0, st_cw1 = straight[cd]

            drd = dr[d]
            dcd = dc[d]
            drt = dr[cd]
            dct = dc[cd]

            rr = row_ranges[d]
            cr = col_ranges[d]

            for i in rr:
                base = i * m

                ni = i + drd       # next in same direction
                pi = i - drd       # previous in same direction, for starts
                ti = i + drt       # next after clockwise turn

                same_row_ok = 0 <= ni < n
                turn_row_ok = 0 <= ti < n
                prev_row_ok = 0 <= pi < n

                if same_row_ok:
                    nbase = ni * m
                if turn_row_ok:
                    tbase = ti * m
                if prev_row_ok:
                    pbase = pi * m

                for j in cr:
                    idx = base + j
                    v = flat[idx]

                    if v == 2:
                        best = 0

                        # Continue straight without turning yet.
                        if same_row_ok:
                            nj = j + dcd
                            if 0 <= nj < m:
                                best = dp1[nbase + nj]

                        # Turn now: suffix starts at cell + clockwise direction.
                        if turn_row_ok:
                            tj = j + dct
                            if 0 <= tj < m:
                                b = st_cw1[tbase + tj]
                                if b > best:
                                    best = b

                        val = best + 1
                        dp0[idx] = val

                        # If the previous cell in this direction is 1, this cell
                        # can be the first cell after the start.
                        if prev_row_ok:
                            pj = j - dcd
                            if 0 <= pj < m and flat[pbase + pj] == 1:
                                cand = val + 1
                                if cand > ans:
                                    ans = cand

                    elif v == 0:
                        best = 0

                        # Continue straight without turning yet.
                        if same_row_ok:
                            nj = j + dcd
                            if 0 <= nj < m:
                                best = dp0[nbase + nj]

                        # Turn now: suffix starts at cell + clockwise direction.
                        if turn_row_ok:
                            tj = j + dct
                            if 0 <= tj < m:
                                b = st_cw0[tbase + tj]
                                if b > best:
                                    best = b

                        val = best + 1
                        dp1[idx] = val

        return ans