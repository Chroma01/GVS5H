from typing import List
from array import array

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        n = len(grid)
        m = len(grid[0])
        total = n * m

        flat = [v for row in grid for v in row]
        cnt1 = flat.count(1)
        if cnt1 == 0:
            return 0

        cnt2 = flat.count(2)
        if cnt2 == 0:
            return 1

        # Directed diagonal order:
        # 0: down-right, 1: down-left, 2: up-left, 3: up-right.
        # Clockwise turns are 0 -> 1 -> 2 -> 3 -> 0.
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        cw = (1, 2, 3, 0)
        opp = (2, 3, 0, 1)
        deltas = [dr * m + dc for dr, dc in dirs]
        bases = [r * m for r in range(n)]

        # nxt[d][i] = adjacent index in direction d, or -1 if out of bounds.
        nxt = []
        for d in range(4):
            dr, dc = dirs[d]
            delta = deltas[d]
            arr = array('i', [-1]) * total

            if dr == 1:
                r0, r1 = 0, n - 1
            else:
                r0, r1 = 1, n

            if dc == 1:
                c0, c1 = 0, m - 1
            else:
                c0, c1 = 1, m

            for r in range(r0, r1):
                base = bases[r]
                nbase = base + delta
                for c in range(c0, c1):
                    arr[base + c] = nbase + c

            nxt.append(arr)

        # st[d][0]: straight run starting at cell when current expected value is 2.
        # st[d][1]: straight run starting at cell when current expected value is 0.
        st = [[array('H', [0]) * total for _ in range(2)] for __ in range(4)]
        range_m = range(m)

        for d in range(4):
            dr, _ = dirs[d]
            nxt_d = nxt[d]
            st2 = st[d][0]
            st0 = st[d][1]

            # For downward directions, next row is already processed when going bottom-up.
            # For upward directions, next row is already processed when going top-down.
            rows = range(n - 1, -1, -1) if dr == 1 else range(n)

            for r in rows:
                base = bases[r]
                for c in range_m:
                    idx = base + c
                    v = flat[idx]

                    if v == 2:
                        nidx = nxt_d[idx]
                        if nidx != -1:
                            st2[idx] = st0[nidx] + 1
                        else:
                            st2[idx] = 1
                    elif v == 0:
                        nidx = nxt_d[idx]
                        if nidx != -1:
                            st0[idx] = st2[nidx] + 1
                        else:
                            st0[idx] = 1

        # dp[d][0]: best suffix starting at cell with expected value 2,
        #           moving in direction d, with no turn used yet.
        # dp[d][1]: same, but expected value is 0.
        dp = [[array('H', [0]) * total for _ in range(2)] for __ in range(4)]

        for d in range(4):
            dr, _ = dirs[d]
            cd = cw[d]

            nxt_d = nxt[d]
            nxt_cw = nxt[cd]

            dp2 = dp[d][0]
            dp0 = dp[d][1]

            st_cw2 = st[cd][0]
            st_cw0 = st[cd][1]

            rows = range(n - 1, -1, -1) if dr == 1 else range(n)

            for r in rows:
                base = bases[r]
                for c in range_m:
                    idx = base + c
                    v = flat[idx]

                    if v == 2:
                        best = 0

                        # Continue straight; next expected value is 0.
                        nidx = nxt_d[idx]
                        if nidx != -1:
                            best = dp0[nidx]

                        # Turn clockwise now; next expected value is 0.
                        nidx_cw = nxt_cw[idx]
                        if nidx_cw != -1:
                            val = st_cw0[nidx_cw]
                            if val > best:
                                best = val

                        dp2[idx] = best + 1

                    elif v == 0:
                        best = 0

                        # Continue straight; next expected value is 2.
                        nidx = nxt_d[idx]
                        if nidx != -1:
                            best = dp2[nidx]

                        # Turn clockwise now; next expected value is 2.
                        nidx_cw = nxt_cw[idx]
                        if nidx_cw != -1:
                            val = st_cw2[nidx_cw]
                            if val > best:
                                best = val

                        dp0[idx] = best + 1

        ans = 1
        dp2_by_dir = [dp[d][0] for d in range(4)]
        nxt_local = nxt
        opp_local = opp

        # Extract answer. Scan the smaller of the 1-cells and 2-cells.
        if cnt1 <= cnt2:
            # Start at a 1 and move to an adjacent 2.
            for idx, v in enumerate(flat):
                if v == 1:
                    for d in range(4):
                        nidx = nxt_local[d][idx]
                        if nidx != -1:
                            val = dp2_by_dir[d][nidx]
                            if val:
                                cand = val + 1
                                if cand > ans:
                                    ans = cand
        else:
            # Start at a 1 immediately behind a 2 in some direction.
            for idx, v in enumerate(flat):
                if v == 2:
                    for d in range(4):
                        pidx = nxt_local[opp_local[d]][idx]
                        if pidx != -1 and flat[pidx] == 1:
                            val = dp2_by_dir[d][idx]
                            if val:
                                cand = val + 1
                                if cand > ans:
                                    ans = cand

        return ans