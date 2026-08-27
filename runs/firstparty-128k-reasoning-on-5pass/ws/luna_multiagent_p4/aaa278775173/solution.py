from array import array
from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m
        values = bytearray(value for row in grid for value in row)

        # SE, SW, NW, NE; clockwise successor is (d + 1) % 4.
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))

        # straight[d * 2 + phase][cell]:
        # longest valid straight segment starting at cell.
        # phase 0 expects 2, phase 1 expects 0.
        straight = [array("H", [0]) * total for _ in range(8)]

        for d, (dr, dc) in enumerate(directions):
            row_order = range(n - 1, -1, -1) if dr == 1 else range(n)
            col_order = range(m - 1, -1, -1) if dc == 1 else range(m)

            expect_two = straight[d * 2]
            expect_zero = straight[d * 2 + 1]

            for r in row_order:
                base = r * m
                nr = r + dr

                for c in col_order:
                    idx = base + c
                    value = values[idx]
                    nc = c + dc

                    if value == 2:
                        length = 1
                        if 0 <= nr < n and 0 <= nc < m:
                            length += expect_zero[nr * m + nc]
                        expect_two[idx] = length
                    elif value == 0:
                        length = 1
                        if 0 <= nr < n and 0 <= nc < m:
                            length += expect_two[nr * m + nc]
                        expect_zero[idx] = length

        # with_turn[d * 2 + phase][cell]:
        # longest valid segment beginning at cell in direction d,
        # with one clockwise turn still available.
        with_turn = [array("H", [0]) * total for _ in range(8)]

        for d, (dr, dc) in enumerate(directions):
            turn_d = (d + 1) % 4
            trd, tcd = directions[turn_d]

            row_order = range(n - 1, -1, -1) if dr == 1 else range(n)
            col_order = range(m - 1, -1, -1) if dc == 1 else range(m)

            current_two = with_turn[d * 2]
            current_zero = with_turn[d * 2 + 1]

            turned_two = straight[turn_d * 2]
            turned_zero = straight[turn_d * 2 + 1]

            for r in row_order:
                base = r * m
                nr = r + dr
                tr = r + trd

                for c in col_order:
                    idx = base + c
                    value = values[idx]

                    nc = c + dc
                    tc = c + tcd

                    has_straight_next = 0 <= nr < n and 0 <= nc < m
                    has_turn_next = 0 <= tr < n and 0 <= tc < m

                    if value == 2:
                        best = 0

                        if has_straight_next:
                            best = with_turn[d * 2 + 1][nr * m + nc]

                        if has_turn_next:
                            candidate = turned_zero[tr * m + tc]
                            if candidate > best:
                                best = candidate

                        current_two[idx] = 1 + best

                    elif value == 0:
                        best = 0

                        if has_straight_next:
                            best = with_turn[d * 2][nr * m + nc]

                        if has_turn_next:
                            candidate = turned_two[tr * m + tc]
                            if candidate > best:
                                best = candidate

                        current_zero[idx] = 1 + best

        answer = 0

        for r in range(n):
            base = r * m

            for c in range(m):
                idx = base + c

                if values[idx] != 1:
                    continue

                answer = max(answer, 1)

                for d, (dr, dc) in enumerate(directions):
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        next_idx = nr * m + nc
                        answer = max(answer, 1 + with_turn[d * 2][next_idx])

                    # Turn immediately after the starting 1.
                    turn_d = (d + 1) % 4
                    tr, tc = directions[turn_d]
                    tr += r
                    tc += c

                    if 0 <= tr < n and 0 <= tc < m:
                        turned_idx = tr * m + tc
                        answer = max(
                            answer,
                            1 + straight[turn_d * 2][turned_idx],
                        )

        return answer