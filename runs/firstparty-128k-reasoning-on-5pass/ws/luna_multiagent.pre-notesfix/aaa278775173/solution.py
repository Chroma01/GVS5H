from typing import List
from array import array
import sys


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        sys.setrecursionlimit(1_000_000)

        n = len(grid)
        m = len(grid[0])

        # Clockwise order in matrix coordinates:
        # SE -> SW -> NW -> NE -> SE
        dr = (1, 1, -1, -1)
        dc = (1, -1, -1, 1)

        # State: (row, col, direction, turned, expected_value)
        # expected_value is either 2 or 0.
        state_count = n * m * 4 * 2 * 2
        memo = array("h", [-1]) * state_count

        def state_index(r: int, c: int, direction: int,
                        turned: int, expected: int) -> int:
            position = r * m + c
            expected_index = 0 if expected == 2 else 1
            return (((position * 4 + direction) * 2 + turned) * 2
                    + expected_index)

        def dfs(r: int, c: int, direction: int,
                turned: int, expected: int) -> int:
            index = state_index(r, c, direction, turned, expected)
            if memo[index] != -1:
                return memo[index]

            best = 1
            next_expected = 0 if expected == 2 else 2

            # Continue straight.
            nr = r + dr[direction]
            nc = c + dc[direction]
            if (
                0 <= nr < n
                and 0 <= nc < m
                and grid[nr][nc] == expected
            ):
                best = max(
                    best,
                    1 + dfs(
                        nr, nc, direction, turned, next_expected
                    ),
                )

            # Make the one allowed clockwise turn.
            if not turned:
                new_direction = (direction + 1) % 4
                nr = r + dr[new_direction]
                nc = c + dc[new_direction]

                if (
                    0 <= nr < n
                    and 0 <= nc < m
                    and grid[nr][nc] == expected
                ):
                    best = max(
                        best,
                        1 + dfs(
                            nr, nc, new_direction, 1, next_expected
                        ),
                    )

            memo[index] = best
            return best

        answer = 0

        for r in range(n):
            for c in range(m):
                if grid[r][c] == 1:
                    for direction in range(4):
                        answer = max(
                            answer,
                            dfs(r, c, direction, 0, 2),
                        )

        return answer