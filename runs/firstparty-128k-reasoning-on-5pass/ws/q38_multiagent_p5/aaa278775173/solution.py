from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        n = len(grid)
        m = len(grid[0])

        # Padded flat grid. Sentinel value 3 is never processed; it only makes
        # diagonal neighbor indices safe without boundary checks.
        W = m + 2
        P = (n + 2) * W
        vals = bytearray([3]) * P

        for r in range(n):
            base = (r + 1) * W + 1
            vals[base:base + m] = bytearray(grid[r])

        ans = 0

        # suf0[d][idx]: longest 0,2,0,2,... run starting at idx in direction d.
        # suf2[d][idx]: longest 2,0,2,0,... run starting at idx in direction d.
        suf0 = [array('H', [0]) * P for _ in range(4)]
        suf2 = [array('H', [0]) * P for _ in range(4)]

        # Clockwise diagonal directions in screen coordinates.
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))

        # Suffix DP in reverse topological order.
        for d, (dr, dc) in enumerate(dirs):
            s0 = suf0[d]
            s2 = suf2[d]
            fd = dr * W + dc

            r_range = range(n, 0, -1) if dr == 1 else range(1, n + 1)
            c_desc = (dc == 1)

            for r in r_range:
                base = r * W
                if c_desc:
                    idx_range = range(base + m, base, -1)
                else:
                    idx_range = range(base + 1, base + m + 1)

                for idx in idx_range:
                    v = vals[idx]
                    nidx = idx + fd

                    if v == 0:
                        s0[idx] = s2[nidx] + 1
                    elif v == 2:
                        s2[idx] = s0[nidx] + 1
                    else:  # v == 1: straight segment starting here
                        cand = s2[nidx] + 1
                        if cand > ans:
                            ans = cand

        # Prefix/end DP in forward order, combined with clockwise outgoing suffix.
        for d, (dr, dc) in enumerate(dirs):
            # eo[idx]: best valid straight segment ending at idx in direction d, odd length.
            # ee[idx]: best valid straight segment ending at idx in direction d, even length.
            eo = array('H', [0]) * P
            ee = array('H', [0]) * P

            fd = dr * W + dc
            r_range = range(1, n + 1) if dr == 1 else range(n, 0, -1)
            c_desc = (dc == -1)

            out = (d + 1) & 3
            s0_out = suf0[out]
            s2_out = suf2[out]

            for r in r_range:
                base = r * W
                if c_desc:
                    idx_range = range(base + m, base, -1)
                else:
                    idx_range = range(base + 1, base + m + 1)

                for idx in idx_range:
                    v = vals[idx]
                    eo_cur = 0
                    ee_cur = 0

                    if v == 1:
                        eo_cur = 1
                    elif v == 2:
                        peo = eo[idx - fd]
                        if peo:
                            ee_cur = peo + 1
                    else:  # v == 0
                        pee = ee[idx - fd]
                        if pee:
                            eo_cur = pee + 1

                    eo[idx] = eo_cur
                    ee[idx] = ee_cur

                    # Odd first leg longer than 1 ends in 0, so suffix must start with 0.
                    if eo_cur > 1:
                        s = s0_out[idx]
                        if s:
                            cand = eo_cur + s - 1
                            if cand > ans:
                                ans = cand

                    # Even first leg ends in 2, so suffix must start with 2.
                    if ee_cur:
                        s = s2_out[idx]
                        if s:
                            cand = ee_cur + s - 1
                            if cand > ans:
                                ans = cand

        return ans