from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m

        # Clockwise diagonal directions:
        # NE -> SE -> SW -> NW -> NE
        directions = [
            (-1, 1),
            (1, 1),
            (1, -1),
            (-1, -1),
        ]

        # Longest continuation without using a turn.
        straight = [[0] * total for _ in range(4)]

        # Longest continuation with one clockwise turn still available.
        flexible = [[0] * total for _ in range(4)]

        for d, (dr, dc) in enumerate(directions):
            row_range = range(n - 1, -1, -1) if dr == 1 else range(n)
            col_range = range(m - 1, -1, -1) if dc == 1 else range(m)
            dp = straight[d]

            for r in row_range:
                for c in col_range:
                    value = grid[r][c]
                    if value == 1:
                        continue

                    expected = 2 if value == 0 else 0
                    nr, nc = r + dr, c + dc
                    length = 1

                    if (
                        0 <= nr < n
                        and 0 <= nc < m
                        and grid[nr][nc] == expected
                    ):
                        length += dp[nr * m + nc]

                    dp[r * m + c] = length

        for d, (dr, dc) in enumerate(directions):
            nd = (d + 1) % 4
            ndr, ndc = directions[nd]

            row_range = range(n - 1, -1, -1) if dr == 1 else range(n)
            col_range = range(m - 1, -1, -1) if dc == 1 else range(m)
            dp = flexible[d]

            for r in row_range:
                for c in col_range:
                    value = grid[r][c]
                    if value == 1:
                        continue

                    expected = 2 if value == 0 else 0
                    best = 1

                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < n
                        and 0 <= nc < m
                        and grid[nr][nc] == expected
                    ):
                        best = max(best, 1 + dp[nr * m + nc])

                    nr, nc = r + ndr, c + ndc
                    if (
                        0 <= nr < n
                        and 0 <= nc < m
                        and grid[nr][nc] == expected
                    ):
                        best = max(best, 1 + straight[nd][nr * m + nc])

                    dp[r * m + c] = best

        answer = 0

        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue

                answer = max(answer, 1)

                for d, (dr, dc) in enumerate(directions):
                    nd = (d + 1) % 4
                    ndr, ndc = directions[nd]

                    best_after_start = 0

                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < n
                        and 0 <= nc < m
                        and grid[nr][nc] == 2
                    ):
                        best_after_start = max(
                            best_after_start,
                            flexible[d][nr * m + nc],
                        )

                    nr, nc = r + ndr, c + ndc
                    if (
                        0 <= nr < n
                        and 0 <= nc < m
                        and grid[nr][nc] == 2
                    ):
                        best_after_start = max(
                            best_after_start,
                            straight[nd][nr * m + nc],
                        )

                    answer = max(answer, 1 + best_after_start)

        return answer