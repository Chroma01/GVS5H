from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m
        values = [value for row in grid for value in row]

        # Clockwise diagonal order:
        # NW -> NE -> SE -> SW -> NW
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        # straight[d][i] = longest alternating 0/2 path beginning at i
        # and continuing only in direction d.
        straight = [array('H', [0]) * total for _ in range(4)]

        for d, (dr, dc) in enumerate(directions):
            dp = straight[d]
            row_range = range(n - 1, -1, -1) if dr > 0 else range(n)
            col_range = range(m - 1, -1, -1) if dc > 0 else range(m)

            for r in row_range:
                base = r * m
                nr = r + dr

                for c in col_range:
                    idx = base + c
                    value = values[idx]

                    if value == 1:
                        continue

                    best = 1
                    nc = c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        nxt = nr * m + nc
                        if values[nxt] == 2 - value:
                            best += dp[nxt]

                    dp[idx] = best

        # bent[d][i] = longest alternating 0/2 path beginning at i,
        # initially moving in d and using at most one clockwise turn.
        bent = [array('H', [0]) * total for _ in range(4)]

        for d, (dr, dc) in enumerate(directions):
            dp = bent[d]
            clockwise = (d + 1) % 4
            after_turn = straight[clockwise]
            turn_dr, turn_dc = directions[clockwise]

            row_range = range(n - 1, -1, -1) if dr > 0 else range(n)
            col_range = range(m - 1, -1, -1) if dc > 0 else range(m)

            for r in row_range:
                base = r * m
                nr = r + dr
                turn_nr = r + turn_dr

                for c in col_range:
                    idx = base + c
                    value = values[idx]

                    if value == 1:
                        continue

                    expected = 2 - value
                    best = 1

                    # Keep going in the original direction. A turn remains available.
                    nc = c + dc
                    if 0 <= nr < n and 0 <= nc < m:
                        nxt = nr * m + nc
                        if values[nxt] == expected:
                            best = max(best, 1 + dp[nxt])

                    # Make the clockwise turn immediately after this cell.
                    turn_nc = c + turn_dc
                    if 0 <= turn_nr < n and 0 <= turn_nc < m:
                        nxt = turn_nr * m + turn_nc
                        if values[nxt] == expected:
                            best = max(best, 1 + after_turn[nxt])

                    dp[idx] = best

        answer = 0

        for r in range(n):
            for c in range(m):
                idx = r * m + c
                if values[idx] != 1:
                    continue

                answer = max(answer, 1)

                for d, (dr, dc) in enumerate(directions):
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        nxt = nr * m + nc
                        if values[nxt] == 2:
                            answer = max(answer, 1 + bent[d][nxt])

        return answer