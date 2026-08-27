from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m
        g = [value for row in grid for value in row]

        # Clockwise order: southeast, southwest, northwest, northeast.
        directions = ((1, 1), (1, -1), (-1, -1), (-1, 1))

        # prefix[d][cell]:
        # longest valid straight path ending at cell, starting with 1,
        # and moving in direction d.
        prefix = [array('H', [0]) * total for _ in range(4)]

        for d, (dr, dc) in enumerate(directions):
            rows = range(n) if dr == 1 else range(n - 1, -1, -1)
            cols = range(m) if dc == 1 else range(m - 1, -1, -1)
            cur = prefix[d]

            for r in rows:
                for c in cols:
                    idx = r * m + c
                    value = g[idx]

                    if value == 1:
                        cur[idx] = 1
                        continue

                    pr = r - dr
                    pc = c - dc
                    if not (0 <= pr < n and 0 <= pc < m):
                        continue

                    previous_length = cur[pr * m + pc]
                    if previous_length:
                        expected = 2 if previous_length % 2 == 1 else 0
                        if value == expected:
                            cur[idx] = previous_length + 1

        # suffix[p][d][cell]:
        # length of a valid straight continuation beginning at cell,
        # where the current cell has sequence parity p:
        # p=1 expects 2, p=0 expects 0.
        suffix = [array('H', [0]) * total for _ in range(8)]

        for p in (0, 1):
            expected = 2 if p == 1 else 0

            for d, (dr, dc) in enumerate(directions):
                rows = range(n - 1, -1, -1) if dr == 1 else range(n)
                cols = range(m - 1, -1, -1) if dc == 1 else range(m)
                cur = suffix[p * 4 + d]
                following = suffix[(p ^ 1) * 4 + d]

                for r in rows:
                    for c in cols:
                        idx = r * m + c
                        if g[idx] != expected:
                            continue

                        length = 1
                        nr = r + dr
                        nc = c + dc
                        if 0 <= nr < n and 0 <= nc < m:
                            length += following[nr * m + nc]

                        cur[idx] = length

        answer = 0

        for r in range(n):
            for c in range(m):
                idx = r * m + c

                for d, (dr, dc) in enumerate(directions):
                    first_length = prefix[d][idx]
                    if not first_length:
                        continue

                    if first_length > answer:
                        answer = first_length

                    # Turn clockwise at the current cell.
                    nd = (d + 1) & 3
                    nr = r + dr
                    nc = c + dc

                    # The next cell has sequence parity equal to the
                    # number of already-consumed cells.
                    if 0 <= nr < n and 0 <= nc < m:
                        continuation = suffix[(first_length & 1) * 4 + nd]
                        candidate = first_length + continuation[nr * m + nc]
                        if candidate > answer:
                            answer = candidate

        return answer