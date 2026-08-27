from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n, m = len(grid), len(grid[0])

        # Clockwise order in screen coordinates (rows increase downward).
        # A turn from directions[i] goes to directions[(i + 1) % 4].
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        ans = 0

        # q is the direction after the clockwise turn.
        # The first-leg direction is its preceding clockwise direction.
        for q_idx, (qr, qc) in enumerate(directions):
            dr, dc = directions[(q_idx - 1) % 4]

            # run0/run2: alternating suffix lengths in q direction,
            # conditional on the current position needing 0 or 2.
            run0 = [[0] * m for _ in range(n)]
            run2 = [[0] * m for _ in range(n)]

            # Process opposite q so (r + qr, c + qc) is already known.
            row_order = range(n - 1, -1, -1) if qr == 1 else range(n)
            col_order = range(m - 1, -1, -1) if qc == 1 else range(m)

            for r in row_order:
                for c in col_order:
                    nr, nc = r + qr, c + qc

                    if grid[r][c] == 0:
                        run0[r][c] = 1
                        if 0 <= nr < n and 0 <= nc < m:
                            run0[r][c] += run2[nr][nc]
                    elif grid[r][c] == 2:
                        run2[r][c] = 1
                        if 0 <= nr < n and 0 <= nc < m:
                            run2[r][c] += run0[nr][nc]

            # first[r][c]: longest valid 1,2,0,2,... first leg that
            # ends at (r, c), moving in (dr, dc).
            first = [[0] * m for _ in range(n)]

            # The predecessor lies in a previous/next row according to dr.
            row_order = range(n) if dr == 1 else range(n - 1, -1, -1)

            for r in row_order:
                for c in range(m):
                    value = grid[r][c]

                    if value == 1:
                        first[r][c] = 1
                    else:
                        pr, pc = r - dr, c - dc
                        if 0 <= pr < n and 0 <= pc < m:
                            prev_len = first[pr][pc]
                            if prev_len:
                                expected = 2 if (prev_len & 1) else 0
                                if value == expected:
                                    first[r][c] = prev_len + 1

                    length = first[r][c]
                    if length == 0:
                        continue

                    ans = max(ans, length)

                    # Continue after a clockwise turn. The pivot itself is
                    # already included in length, so begin at its q-neighbor.
                    nr, nc = r + qr, c + qc
                    if 0 <= nr < n and 0 <= nc < m:
                        expected = 2 if (length & 1) else 0
                        suffix = run2[nr][nc] if expected == 2 else run0[nr][nc]
                        ans = max(ans, length + suffix)

        return ans