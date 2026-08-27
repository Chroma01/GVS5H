from typing import List
from array import array


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        total = n * m
        values = [value for row in grid for value in row]

        # Clockwise order under row-down coordinates:
        # southeast -> southwest -> northwest -> northeast -> southeast
        directions = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # alternate[d][idx] is the maximum alternating 0/2 suffix length
        # beginning at idx while moving in directions[d].
        alternate = []

        for dr, dc in directions:
            dp = array('H', [0]) * total

            # The next cell is in row r + dr, so process that row first.
            row_range = range(n - 1, -1, -1) if dr == 1 else range(n)

            for r in row_range:
                base = r * m
                for c in range(m):
                    idx = base + c
                    value = values[idx]

                    if value == 1:
                        continue

                    length = 1
                    nr = r + dr
                    nc = c + dc

                    if 0 <= nr < n and 0 <= nc < m:
                        next_idx = nr * m + nc
                        if values[next_idx] == 2 - value:
                            length += dp[next_idx]

                    dp[idx] = length

            alternate.append(dp)

        answer = 0

        # prefix[idx] is the valid first-arm length ending at idx.
        for d, (dr, dc) in enumerate(directions):
            prefix = array('H', [0]) * total

            # The predecessor is at r - dr, so process it first.
            row_range = range(n) if dr == 1 else range(n - 1, -1, -1)

            # One clockwise 90-degree turn.
            turn_direction = (d + 1) % 4
            tr, tc = directions[turn_direction]
            turned_suffix = alternate[turn_direction]

            for r in row_range:
                base = r * m

                for c in range(m):
                    idx = base + c
                    value = values[idx]

                    if value == 1:
                        current = 1
                    else:
                        current = 0
                        pr = r - dr
                        pc = c - dc

                        if 0 <= pr < n and 0 <= pc < m:
                            previous = prefix[pr * m + pc]

                            if previous:
                                expected = 2 if previous % 2 == 1 else 0
                                if value == expected:
                                    current = previous + 1

                    prefix[idx] = current

                    if not current:
                        continue

                    answer = max(answer, current)

                    # First element on the second arm must continue 2,0,2,0,...
                    nr = r + tr
                    nc = c + tc

                    if 0 <= nr < n and 0 <= nc < m:
                        next_idx = nr * m + nc
                        expected = 2 if current % 2 == 1 else 0

                        if values[next_idx] == expected:
                            answer = max(answer, current + turned_suffix[next_idx])

        return answer