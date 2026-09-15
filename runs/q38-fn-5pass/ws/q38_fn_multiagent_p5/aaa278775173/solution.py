from typing import List

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m

        vals = [v for row in grid for v in row]
        del grid

        if 1 not in vals:
            return 0

        ans = 1
        max_possible = 2 * min(n, m) - 1
        if ans == max_possible:
            return ans

        # Directed diagonal directions:
        # 0: down-right, 1: down-left, 2: up-left, 3: up-right.
        # Clockwise turn is the next direction in this order.
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))

        vv = vals
        nn = n
        mm = m

        for d in range(4):
            # Clockwise turn direction for a segment whose first arm uses direction d.
            tdr, tdc = dirs[(d + 1) % 4]
            delta = tdr * mm + tdc

            # run[idx] = longest alternating 0/2 run starting at idx in the turn
            # direction, with the first value equal to grid[idx].
            # Cells with value 1 have run 0.
            run = [0] * total

            # Process reverse direction so the next cell is already computed.
            srow = range(nn - 1, -1, -1) if tdr == 1 else range(nn)
            scol = range(mm - 1, -1, -1) if tdc == 1 else range(mm)
            turn_col_ok = [c < mm - 1 if tdc == 1 else c > 0 for c in range(mm)]

            for r in srow:
                base = r * mm
                row_ok = (r < nn - 1) if tdr == 1 else (r > 0)

                for c in scol:
                    idx = base + c
                    v = vv[idx]

                    if v == 0:
                        if row_ok and turn_col_ok[c]:
                            nxt = idx + delta
                            if vv[nxt] == 2:
                                run[idx] = 1 + run[nxt]
                            else:
                                run[idx] = 1
                        else:
                            run[idx] = 1

                    elif v == 2:
                        if row_ok and turn_col_ok[c]:
                            nxt = idx + delta
                            if vv[nxt] == 0:
                                run[idx] = 1 + run[nxt]
                            else:
                                run[idx] = 1
                        else:
                            run[idx] = 1

            # pref[idx] = longest valid straight prefix ending at idx in direction d.
            # Parity is inferred from the cell value:
            #   value 1 or 0 -> odd length, next expected value is 2
            #   value 2      -> even length, next expected value is 0
            pref = [0] * total

            pdr, pdc = dirs[d]
            delta_p = pdr * mm + pdc

            # Process forward direction so the predecessor is already computed.
            prow = range(nn) if pdr == 1 else range(nn - 1, -1, -1)
            pcol = range(mm) if pdc == 1 else range(mm - 1, -1, -1)
            pred_col_ok = [c > 0 if pdc == 1 else c < mm - 1 for c in range(mm)]

            for r in prow:
                base = r * mm
                pred_row_ok = (r > 0) if pdr == 1 else (r < nn - 1)
                turn_row_ok = (r < nn - 1) if tdr == 1 else (r > 0)

                for c in pcol:
                    idx = base + c
                    v = vv[idx]

                    if v == 1:
                        pref[idx] = 1

                        # Turn immediately after the starting 1; this is also a
                        # valid straight segment in the turn direction, but counting
                        # it here is harmless and keeps the turn logic uniform.
                        if turn_row_ok and turn_col_ok[c]:
                            nxt = idx + delta
                            if vv[nxt] == 2:
                                tot = 1 + run[nxt]
                                if tot > ans:
                                    ans = tot

                    elif v == 2:
                        # Current value 2 means even prefix length.
                        # It can extend only from an odd prefix, whose last value
                        # must be 1 or 0.
                        if pred_row_ok and pred_col_ok[c]:
                            pidx = idx - delta_p
                            p = pref[pidx]

                            if p and vv[pidx] != 2:
                                length = p + 1
                                pref[idx] = length

                                if length > ans:
                                    ans = length

                                # Even length expects next value 0 after turning.
                                if turn_row_ok and turn_col_ok[c]:
                                    nxt = idx + delta
                                    if vv[nxt] == 0:
                                        tot = length + run[nxt]
                                        if tot > ans:
                                            ans = tot

                    else:  # v == 0
                        # Current value 0 means odd prefix length.
                        # It can extend only from an even prefix, whose last value
                        # must be 2.
                        if pred_row_ok and pred_col_ok[c]:
                            pidx = idx - delta_p
                            p = pref[pidx]

                            if p and vv[pidx] == 2:
                                length = p + 1
                                pref[idx] = length

                                if length > ans:
                                    ans = length

                                # Odd length expects next value 2 after turning.
                                if turn_row_ok and turn_col_ok[c]:
                                    nxt = idx + delta
                                    if vv[nxt] == 2:
                                        tot = length + run[nxt]
                                        if tot > ans:
                                            ans = tot

            if ans == max_possible:
                return ans

        return ans