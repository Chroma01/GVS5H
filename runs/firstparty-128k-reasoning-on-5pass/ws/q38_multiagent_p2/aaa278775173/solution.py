from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        N = n * m

        vals = bytearray(v for row in grid for v in row)

        base_dp = array('H', [0]) * N
        base_run2 = array('H', [0]) * N
        base_run0 = array('H', [0]) * N

        has_one = False
        for i, v in enumerate(vals):
            if v == 1:
                base_dp[i] = 1
                has_one = True
            elif v == 2:
                base_run2[i] = 1
            elif v == 0:
                base_run0[i] = 1

        if not has_one:
            return 0

        ans = 1
        dp0 = [None] * 4

        # Directions: 0 = NE, 1 = SE, 2 = SW, 3 = NW.
        # For no-turn DP, pdelta gives previous cell index = idx + pdelta.
        dp_params = [
            (range(n - 2, -1, -1), range(1, m), m - 1),
            (range(1, n), range(1, m), -m - 1),
            (range(1, n), range(m - 2, -1, -1), -m + 1),
            (range(n - 2, -1, -1), range(m - 2, -1, -1), m + 1),
        ]

        for i, (rows, cols, pdelta) in enumerate(dp_params):
            dp = base_dp[:]
            for r in rows:
                base = r * m
                for c in cols:
                    idx = base + c
                    v = vals[idx]
                    if v != 1:
                        L = dp[idx + pdelta]
                        if L:
                            if (v == 2 and (L & 1)) or (v == 0 and not (L & 1)):
                                new = L + 1
                                dp[idx] = new
                                if new > ans:
                                    ans = new
            dp0[i] = dp

        # For each second direction b, ndelta gives next cell index = idx + ndelta.
        # The first direction must be a = (b + 3) % 4, i.e. b is clockwise from a.
        run_params = [
            (range(1, n), range(m - 2, -1, -1), -m + 1, 3),
            (range(n - 2, -1, -1), range(m - 2, -1, -1), m + 1, 0),
            (range(n - 2, -1, -1), range(1, m), m - 1, 1),
            (range(1, n), range(1, m), -m - 1, 2),
        ]

        for rows, cols, ndelta, a in run_params:
            run2 = base_run2[:]
            run0 = base_run0[:]
            dpa = dp0[a]

            for r in rows:
                base = r * m
                for c in cols:
                    idx = base + c
                    nidx = idx + ndelta
                    v = vals[idx]

                    if v == 2:
                        run2[idx] = run0[nidx] + 1
                    elif v == 0:
                        run0[idx] = run2[nidx] + 1

                    A = dpa[idx]
                    if A:
                        add = run2[nidx] if (A & 1) else run0[nidx]
                        total = A + add
                        if total > ans:
                            ans = total

        return ans