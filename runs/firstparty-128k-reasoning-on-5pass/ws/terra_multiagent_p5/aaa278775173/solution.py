from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m

        # Clockwise order in matrix coordinates (rows increase downward).
        directions = [
            (1, 1),    # SE
            (1, -1),   # SW
            (-1, -1),  # NW
            (-1, 1),   # NE
        ]

        # suffix[d] contains alternating runs beginning at each cell and
        # continuing in directions[d], for expected values 0 and 2.
        suffix = []

        for dr, dc in directions:
            expect_zero = array('H', [0]) * total
            expect_two = array('H', [0]) * total

            # The next cell (r + dr, c + dc) is in a previously processed row.
            row_range = range(n - 1, -1, -1) if dr == 1 else range(n)

            for r in row_range:
                base = r * m
                nr = r + dr

                for c in range(m):
                    value = grid[r][c]
                    idx = base + c
                    nc = c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        next_idx = nr * m + nc
                    else:
                        next_idx = -1

                    if value == 0:
                        expect_zero[idx] = 1 + (
                            expect_two[next_idx] if next_idx != -1 else 0
                        )
                    elif value == 2:
                        expect_two[idx] = 1 + (
                            expect_zero[next_idx] if next_idx != -1 else 0
                        )

            suffix.append((expect_zero, expect_two))

        answer = 0

        # Compute valid first arms ending at every cell for each direction.
        for d, (dr, dc) in enumerate(directions):
            first_leg = array('H', [0]) * total

            # The predecessor (r - dr, c - dc) is in a previously processed row.
            row_range = range(n) if dr == 1 else range(n - 1, -1, -1)

            turn_d = (d + 1) % 4
            tdr, tdc = directions[turn_d]
            turn_zero, turn_two = suffix[turn_d]

            for r in row_range:
                base = r * m

                for c in range(m):
                    idx = base + c
                    value = grid[r][c]
                    length = 0

                    if value == 1:
                        length = 1
                    elif value == 0 or value == 2:
                        pr = r - dr
                        pc = c - dc

                        if 0 <= pr < n and 0 <= pc < m:
                            previous = first_leg[pr * m + pc]

                            if previous:
                                # After total length 1, 3, 5... the next
                                # sequence value is 2; otherwise it is 0.
                                expected = 2 if previous % 2 else 0
                                if value == expected:
                                    length = previous + 1

                    if length == 0:
                        continue

                    first_leg[idx] = length
                    if length > answer:
                        answer = length

                    # Try the optional clockwise turn after this endpoint.
                    nr = r + tdr
                    nc = c + tdc

                    if 0 <= nr < n and 0 <= nc < m:
                        next_idx = nr * m + nc

                        # The value required immediately after the turn follows
                        # from the parity of the full first-arm length.
                        continuation = (
                            turn_two[next_idx]
                            if length % 2 == 1
                            else turn_zero[next_idx]
                        )

                        candidate = length + continuation
                        if candidate > answer:
                            answer = candidate

        return answer