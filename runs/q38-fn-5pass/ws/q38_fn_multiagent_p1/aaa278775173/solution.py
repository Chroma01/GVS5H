from typing import List
from array import array

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        n, m = len(grid), len(grid[0])
        size = n * m

        flat = bytearray(size)
        for i, row in enumerate(grid):
            base = i * m
            flat[base:base + m] = bytes(row)

        if 1 not in flat:
            return 0

        # Directions: NE, SE, SW, NW.
        # Clockwise diagonal order is NE -> SE -> SW -> NW -> NE.
        dirs = ((-1, 1), (1, 1), (1, -1), (-1, -1))
        cw = (1, 2, 3, 0)

        # cont2[d][cell]: longest straight run starting at cell in direction d
        # if this cell is expected to be 2, then 0, then 2, ...
        # cont0[d][cell]: same, but this cell is expected to be 0, then 2, ...
        cont2 = [array('H', [0]) * size for _ in range(4)]
        cont0 = [array('H', [0]) * size for _ in range(4)]

        for d, (dr, dc) in enumerate(dirs):
            c2 = cont2[d]
            c0 = cont0[d]

            # Process so that the next cell in this direction is already computed.
            row_iter = range(n) if dr < 0 else range(n - 1, -1, -1)
            col_iter = range(m - 1, -1, -1) if dc > 0 else range(m)

            for i in row_iter:
                base = i * m
                ni = i + dr
                ni_ok = 0 <= ni < n
                nbase = ni * m if ni_ok else 0

                for j in col_iter:
                    idx = base + j
                    v = flat[idx]

                    if v == 2:
                        if ni_ok:
                            nj = j + dc
                            if 0 <= nj < m:
                                c2[idx] = c0[nbase + nj] + 1
                            else:
                                c2[idx] = 1
                        else:
                            c2[idx] = 1

                    elif v == 0:
                        if ni_ok:
                            nj = j + dc
                            if 0 <= nj < m:
                                c0[idx] = c2[nbase + nj] + 1
                            else:
                                c0[idx] = 1
                        else:
                            c0[idx] = 1

        ans = 1

        # For the current incoming direction:
        # end1[cell] = longest valid straight segment ending at cell,
        #              ending value 2, hence even length.
        # end2[cell] = longest valid straight segment ending at cell,
        #              ending value 0, hence odd length >= 3.
        # A segment ending at value 1 has length 1 and needs no array.
        end1 = [0] * size
        end2 = [0] * size

        for d, (dr, dc) in enumerate(dirs):
            c2_cur = cont2[d]

            cd = cw[d]
            c2_cw = cont2[cd]
            c0_cw = cont0[cd]
            odr, odc = dirs[cd]

            # Process so that the previous cell in this direction is already computed.
            row_iter = range(n - 1, -1, -1) if dr < 0 else range(n)
            col_iter = range(m) if dc > 0 else range(m - 1, -1, -1)

            for i in row_iter:
                base = i * m

                pi = i - dr
                pi_ok = 0 <= pi < n
                pbase = pi * m if pi_ok else 0

                ni = i + dr
                ni_ok = 0 <= ni < n
                nbase = ni * m if ni_ok else 0

                oi = i + odr
                oi_ok = 0 <= oi < n
                obase = oi * m if oi_ok else 0

                for j in col_iter:
                    idx = base + j
                    v = flat[idx]

                    e1 = 0
                    e2 = 0

                    if v == 1:
                        # No-turn segment starting here in the current direction.
                        if ni_ok:
                            nj = j + dc
                            if 0 <= nj < m:
                                total = 1 + c2_cur[nbase + nj]
                                if total > ans:
                                    ans = total

                        # Incoming length 1, then turn clockwise.
                        # This is also a valid no-turn segment in the clockwise direction.
                        if oi_ok:
                            oj = j + odc
                            if 0 <= oj < m:
                                total = 1 + c2_cw[obase + oj]
                                if total > ans:
                                    ans = total

                    elif v == 2:
                        # End with value 2: length is even, next expected value is 0.
                        if pi_ok:
                            pj = j - dc
                            if 0 <= pj < m:
                                pidx = pbase + pj

                                # Length 2 case: previous cell is the starting 1.
                                if flat[pidx] == 1:
                                    e1 = 2

                                # Longer even lengths extend an odd segment ending in 0.
                                pe2 = end2[pidx]
                                if pe2:
                                    cand = pe2 + 1
                                    if cand > e1:
                                        e1 = cand

                        if e1 and oi_ok:
                            oj = j + odc
                            if 0 <= oj < m:
                                total = e1 + c0_cw[obase + oj]
                                if total > ans:
                                    ans = total

                    else:  # v == 0
                        # End with value 0: length is odd >= 3, next expected value is 2.
                        if pi_ok:
                            pj = j - dc
                            if 0 <= pj < m:
                                pidx = pbase + pj
                                pe1 = end1[pidx]
                                if pe1:
                                    e2 = pe1 + 1

                        if e2 and oi_ok:
                            oj = j + odc
                            if 0 <= oj < m:
                                total = e2 + c2_cw[obase + oj]
                                if total > ans:
                                    ans = total

                    end1[idx] = e1
                    end2[idx] = e2

        return ans