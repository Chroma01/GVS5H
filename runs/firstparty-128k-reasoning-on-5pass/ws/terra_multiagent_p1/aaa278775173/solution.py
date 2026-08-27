from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m

        # Clockwise direction cycle in row/column coordinates.
        # NW -> NE -> SE -> SW -> NW
        directions = [(-1, -1), (-1, 1), (1, 1), (1, -1)]

        # suffix[d] = (lengths starting with required 0, lengths starting with required 2)
        # Each length follows direction d and alternates 0, 2, 0, 2, ...
        suffix = []

        for dr, dc in directions:
            # Process every cell after its next cell in direction (dr, dc).
            r_start, r_end, r_step = (n - 1, -1, -1) if dr == 1 else (0, n, 1)
            c_start, c_end, c_step = (m - 1, -1, -1) if dc == 1 else (0, m, 1)

            start_zero = array("H", [0]) * total
            start_two = array("H", [0]) * total

            for r in range(r_start, r_end, r_step):
                nr = r + dr
                base = r * m

                for c in range(c_start, c_end, c_step):
                    idx = base + c
                    value = grid[r][c]
                    nc = c + dc

                    if value == 0:
                        if 0 <= nr < n and 0 <= nc < m:
                            start_zero[idx] = 1 + start_two[nr * m + nc]
                        else:
                            start_zero[idx] = 1
                    elif value == 2:
                        if 0 <= nr < n and 0 <= nc < m:
                            start_two[idx] = 1 + start_zero[nr * m + nc]
                        else:
                            start_two[idx] = 1

            suffix.append((start_zero, start_two))

        answer = 0
        incoming = array("H", [0]) * total

        # For each initial direction, compute the longest valid segment ending
        # at each cell before any clockwise turn.
        for d, (dr, dc) in enumerate(directions):
            # Process after the predecessor (r-dr, c-dc).
            r_start, r_end, r_step = (0, n, 1) if dr == 1 else (n - 1, -1, -1)
            c_start, c_end, c_step = (0, m, 1) if dc == 1 else (m - 1, -1, -1)

            turn_d = (d + 1) % 4
            tr, tc = directions[turn_d]
            turn_zero, turn_two = suffix[turn_d]

            for r in range(r_start, r_end, r_step):
                base = r * m
                pr = r - dr

                for c in range(c_start, c_end, c_step):
                    idx = base + c
                    value = grid[r][c]
                    length = 0
                    pc = c - dc

                    if value == 1:
                        length = 1
                    elif 0 <= pr < n and 0 <= pc < m:
                        previous = incoming[pr * m + pc]
                        if previous:
                            if (previous & 1 and value == 2) or (
                                not (previous & 1) and value == 0
                            ):
                                length = previous + 1

                    incoming[idx] = length

                    if not length:
                        continue

                    if length > answer:
                        answer = length

                    # Turn at this pivot, excluding the pivot from the suffix.
                    nr = r + tr
                    nc = c + tc
                    if 0 <= nr < n and 0 <= nc < m:
                        if length & 1:
                            extra = turn_two[nr * m + nc]
                        else:
                            extra = turn_zero[nr * m + nc]

                        candidate = length + extra
                        if candidate > answer:
                            answer = candidate

        return answer