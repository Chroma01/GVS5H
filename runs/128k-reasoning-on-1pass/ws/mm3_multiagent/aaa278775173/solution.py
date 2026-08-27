from typing import List
import sys

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        # Increase recursion limit for deep diagonal walks
        sys.setrecursionlimit(1000000)

        n = len(grid)
        if n == 0:
            return 0
        m = len(grid[0])
        if m == 0:
            return 0

        # Four diagonal directions
        # 0: down‑right, 1: down‑left, 2: up‑left, 3: up‑right
        dx = [1, 1, -1, -1]
        dy = [1, -1, -1, 1]

        # Total DP states = n*m * 4 (dir) * 2 (turn flag) * 2 (parity) = n*m*16
        total_states = n * m * 16
        dp = [-1] * total_states          # -1 means not computed yet

        def encode(i: int, j: int, d: int, t: int, p: int) -> int:
            """Encode (i,j,d,turns_left,parity) into a single index."""
            return ((i * m + j) << 4) | (d << 2) | (t << 1) | p

        # Expected value for a given parity (0 → 0, 1 → 2)
        expected_for_parity = [0, 2]

        def dfs(i: int, j: int, d: int, t: int, p: int) -> int:
            """
            Return the maximal length of a valid segment that starts at
            cell (i,j) with current direction d.
            t = 1  → a clockwise turn is still allowed,
            t = 0  → no turn left.
            p = parity of the distance from the real start
                (0 = even distance, 1 = odd distance).
            The current cell is already counted (1).
            """
            idx = encode(i, j, d, t, p)
            if dp[idx] != -1:
                return dp[idx]

            best = 1  # count current cell

            # Parity after one more step
            np = 1 - p
            exp = expected_for_parity[np]

            # Option 1: continue in the same diagonal direction
            ni = i + dx[d]
            nj = j + dy[d]
            if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == exp:
                cand = 1 + dfs(ni, nj, d, t, np)
                if cand > best:
                    best = cand

            # Option 2: turn clockwise 90° (if still allowed)
            if t:
                nd = (d + 1) & 3          # clockwise turn
                ni = i + dx[nd]
                nj = j + dy[nd]
                if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == exp:
                    cand = 1 + dfs(ni, nj, nd, t - 1, np)
                    if cand > best:
                        best = cand

            dp[idx] = best
            return best

        answer = 0

        # Every cell with value 1 can be a segment start
        for i in range(n):
            for j in range(m):
                if grid[i][j] != 1:
                    continue

                # Segment consisting of only this cell has length 1
                answer = max(answer, 1)

                # Try each of the four diagonals as the first step
                for d in range(4):
                    ni = i + dx[d]
                    nj = j + dy[d]
                    if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == 2:
                        length = 1 + dfs(ni, nj, d, 1, 1)  # distance = 1
                        answer = max(answer, length)

        return answer