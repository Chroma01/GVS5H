from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m

        # southeast, southwest, northwest, northeast.
        # The next direction in this order is a clockwise turn.
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))

        # straight[d][r*m+c] is the longest valid alternating sequence
        # starting at (r, c) and continuing only in direction d.
        straight = []

        for dr, dc in directions:
            dp = array("H", [0]) * total

            row_range = range(n - 1, -1, -1) if dr == 1 else range(n)
            col_range = range(m - 1, -1, -1) if dc == 1 else range(m)

            for r in row_range:
                base = r * m
                nr = r + dr

                for c in col_range:
                    value = grid[r][c]
                    if value not in (0, 2):
                        continue

                    length = 1
                    nc = c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        if grid[nr][nc] == 2 - value:
                            length += dp[nr * m + nc]

                    dp[base + c] = length

            straight.append(dp)

        # one_turn[d][cell] is the longest valid sequence starting at cell,
        # traveling in direction d, with at most one clockwise turn.
        one_turn = []

        for d, (dr, dc) in enumerate(directions):
            dp = array("H", [0]) * total
            next_direction = (d + 1) % 4
            tdr, tdc = directions[next_direction]
            turned_straight = straight[next_direction]

            row_range = range(n - 1, -1, -1) if dr == 1 else range(n)
            col_range = range(m - 1, -1, -1) if dc == 1 else range(m)

            for r in row_range:
                base = r * m
                nr = r + dr

                for c in col_range:
                    value = grid[r][c]
                    if value not in (0, 2):
                        continue

                    best = 1
                    nc = c + dc

                    # Continue without turning.
                    if 0 <= nr < n and 0 <= nc < m:
                        if grid[nr][nc] == 2 - value:
                            best = max(best, 1 + dp[nr * m + nc])

                    # Turn clockwise at this cell.
                    tr = r + tdr
                    tc = c + tdc
                    if 0 <= tr < n and 0 <= tc < m:
                        if grid[tr][tc] == 2 - value:
                            best = max(
                                best,
                                1 + turned_straight[tr * m + tc]
                            )

                    dp[base + c] = best

            one_turn.append(dp)

        answer = 0

        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue

                answer = max(answer, 1)

                for d, (dr, dc) in enumerate(directions):
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        if grid[nr][nc] == 2:
                            answer = max(
                                answer,
                                1 + one_turn[d][nr * m + nc]
                            )

        return answer