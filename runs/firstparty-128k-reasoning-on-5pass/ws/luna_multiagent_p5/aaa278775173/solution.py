from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m

        # Clockwise order:
        # southeast -> southwest -> northwest -> northeast -> southeast
        directions = [
            (1, 1),
            (1, -1),
            (-1, -1),
            (-1, 1),
        ]

        # straight[d][cell] = longest alternating sequence
        # 2, 0, 2, 0, ... beginning at cell and moving in direction d.
        straight = [array("H", [0]) * total for _ in range(4)]

        for d, (dr, dc) in enumerate(directions):
            rows = range(n - 1, -1, -1) if dr == 1 else range(n)
            cols = range(m - 1, -1, -1) if dc == 1 else range(m)

            run = straight[d]

            for r in rows:
                base = r * m
                nr = r + dr

                for c in cols:
                    idx = base + c
                    value = grid[r][c]

                    if value == 1:
                        continue

                    length = 1
                    nc = c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        next_value = grid[nr][nc]
                        if next_value != 1 and next_value != value:
                            length += run[nr * m + nc]

                    run[idx] = length

        # turnable[2*d + parity][cell]:
        # longest valid sequence beginning at cell in direction d,
        # where parity 0 expects 2 and parity 1 expects 0.
        # One clockwise turn is still available.
        turnable = [array("H", [0]) * total for _ in range(8)]

        for d, (dr, dc) in enumerate(directions):
            turn_d = (d + 1) % 4
            turn_dr, turn_dc = directions[turn_d]
            turned_run = straight[turn_d]

            rows = range(n - 1, -1, -1) if dr == 1 else range(n)
            cols = range(m - 1, -1, -1) if dc == 1 else range(m)

            for r in rows:
                base = r * m
                nr = r + dr
                nc_base = dc

                for c in cols:
                    idx = base + c
                    value = grid[r][c]

                    next_r = nr
                    next_c = c + nc_base
                    has_straight_next = (
                        0 <= next_r < n and 0 <= next_c < m
                    )
                    next_idx = (
                        next_r * m + next_c
                        if has_straight_next
                        else -1
                    )

                    # The clockwise turn is made at the current cell.
                    turn_r = r + turn_dr
                    turn_c = c + turn_dc
                    has_turn_next = (
                        0 <= turn_r < n and 0 <= turn_c < m
                    )
                    turn_idx = (
                        turn_r * m + turn_c
                        if has_turn_next
                        else -1
                    )

                    for parity, expected in enumerate((2, 0)):
                        state = turnable[2 * d + parity]

                        if value != expected:
                            continue

                        opposite = 0 if expected == 2 else 2
                        best = 0

                        # Continue in the current direction, preserving
                        # the option to turn later.
                        if has_straight_next:
                            best = turnable[2 * d + (parity ^ 1)][next_idx]

                        # Turn clockwise immediately after consuming the
                        # current cell. The next cell must have the opposite
                        # value, and no further turn is allowed.
                        if has_turn_next and grid[turn_r][turn_c] == opposite:
                            candidate = turned_run[turn_idx]
                            if candidate > best:
                                best = candidate

                        state[idx] = best + 1

        answer = 0

        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue

                answer = max(answer, 1)

                for d, (dr, dc) in enumerate(directions):
                    nr = r + dr
                    nc = c + dc

                    if (
                        0 <= nr < n
                        and 0 <= nc < m
                        and grid[nr][nc] == 2
                    ):
                        length = 1 + turnable[2 * d][nr * m + nc]
                        answer = max(answer, length)

        return answer