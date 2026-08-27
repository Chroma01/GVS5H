from typing import List
from array import array
import random


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        N = n * m
        vals = [v for row in grid for v in row]

        # Clockwise diagonal order: DR, DL, UL, UR
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))

        # S[d][idx] = longest valid straight segment ending at idx, moving in direction d
        S = [array('H', [0]) * N for _ in range(4)]
        ans = 0

        for d, (dr, dc) in enumerate(dirs):
            s = S[d]
            rows = range(n) if dr == 1 else range(n - 1, -1, -1)

            for r in rows:
                base = r * m
                pr = r - dr

                if 0 <= pr < n:
                    pbase = pr * m
                    for c in range(m):
                        idx = base + c
                        val = vals[idx]

                        if val == 1:
                            length = 1
                        else:
                            length = 0
                            pc = c - dc
                            if 0 <= pc < m:
                                p = s[pbase + pc]
                                if p:
                                    if val == 2:
                                        if p & 1:
                                            length = p + 1
                                    elif val == 0:
                                        if not (p & 1):
                                            length = p + 1

                        s[idx] = length
                        if length > ans:
                            ans = length
                else:
                    for c in range(m):
                        idx = base + c
                        if vals[idx] == 1:
                            s[idx] = 1
                            if ans < 1:
                                ans = 1

        # T[d][idx] = longest valid segment ending at idx with final direction d,
        # allowing at most one clockwise turn.
        for d, (dr, dc) in enumerate(dirs):
            t = array('H', [0]) * N
            s_prev = S[(d - 1) & 3]
            rows = range(n) if dr == 1 else range(n - 1, -1, -1)

            for r in rows:
                base = r * m
                pr = r - dr

                if 0 <= pr < n:
                    pbase = pr * m
                    for c in range(m):
                        idx = base + c
                        val = vals[idx]
                        best = 0

                        pc = c - dc
                        if 0 <= pc < m:
                            pidx = pbase + pc

                            # Either extend an already-final-direction segment,
                            # or turn at the predecessor from the previous direction.
                            p = t[pidx]
                            p2 = s_prev[pidx]
                            if p2 > p:
                                p = p2

                            if p:
                                if val == 2:
                                    if p & 1:
                                        best = p + 1
                                elif val == 0:
                                    if not (p & 1):
                                        best = p + 1

                        t[idx] = best
                        if best > ans:
                            ans = best

        return ans


def brute_force(grid: List[List[int]]) -> int:
    n = len(grid)
    m = len(grid[0])
    dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))
    ans = 0

    for r in range(n):
        for c in range(m):
            if grid[r][c] != 1:
                continue

            for d in range(4):
                stack = [(r, c, d, False, 1)]
                while stack:
                    rr, cc, dd, turned, length = stack.pop()
                    if length > ans:
                        ans = length

                    # Continue in the current direction.
                    dr, dc = dirs[dd]
                    nr, nc = rr + dr, cc + dc
                    if 0 <= nr < n and 0 <= nc < m:
                        need = 2 if (length & 1) else 0
                        if grid[nr][nc] == need:
                            stack.append((nr, nc, dd, turned, length + 1))

                    # Make at most one clockwise turn.
                    if not turned:
                        ed = (dd + 1) & 3
                        dr, dc = dirs[ed]
                        nr, nc = rr + dr, cc + dc
                        if 0 <= nr < n and 0 <= nc < m:
                            need = 2 if (length & 1) else 0
                            if grid[nr][nc] == need:
                                stack.append((nr, nc, ed, True, length + 1))

    return ans


def verify() -> bool:
    sol = Solution()

    examples = [
        [[2, 2, 1, 2, 2], [2, 0, 2, 2, 0], [2, 0, 1, 1, 0], [1, 0, 2, 2, 2], [2, 0, 0, 2, 2]],
        [[2, 2, 2, 2, 2], [2, 0, 2, 2, 0], [2, 0, 1, 1, 0], [1, 0, 2, 2, 2], [2, 0, 0, 2, 2]],
        [[1, 2, 2, 2, 2], [2, 2, 2, 2, 0], [2, 0, 0, 0, 0], [0, 0, 2, 2, 2], [2, 0, 0, 2, 0]],
        [[1]],
    ]
    expected = [5, 4, 5, 1]

    for i, (grid, exp) in enumerate(zip(examples, expected), 1):
        got = sol.lenOfVDiagonal(grid)
        bf = brute_force(grid)
        if got != exp or bf != exp:
            print(f"FAIL example {i}: expected {exp}, solution {got}, brute {bf}")
            print("grid =", grid)
            return False

    edge_cases = [
        ([[1]], 1),
        ([[0]], 0),
        ([[2]], 0),
        ([[1, 2, 0, 2, 0]], 1),
        ([[1], [2], [0], [2], [0]], 1),
        ([[2, 0], [0, 2]], 0),
        ([[1, 2], [2, 0]], 2),
        ([[1, 0, 0], [0, 2, 0], [0, 0, 0]], 3),
        ([[1, 0, 0, 0], [0, 2, 0, 2], [0, 0, 0, 0], [0, 0, 0, 0]], 3),
        ([[0, 0, 2, 0], [0, 0, 0, 0], [0, 0, 2, 0], [0, 0, 0, 1]], 4),
        ([[0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 0, 2], [1, 0, 0, 0]], 4),
        ([[0, 0, 0, 0], [2, 0, 0, 0], [0, 0, 0, 1], [0, 2, 0, 0]], 4),
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1),
        ([[2, 2], [2, 2]], 0),
        ([[0, 0], [0, 0]], 0),
    ]

    for grid, exp in edge_cases:
        got = sol.lenOfVDiagonal(grid)
        bf = brute_force(grid)
        if got != exp or bf != exp:
            print(f"FAIL edge: expected {exp}, solution {got}, brute {bf}")
            print("grid =", grid)
            return False

    # Long straight diagonal.
    n = 500
    grid = [[0] * n for _ in range(n)]
    for i in range(n):
        grid[i][i] = 1 if i == 0 else (2 if (i & 1) else 0)
    got = sol.lenOfVDiagonal(grid)
    if got != n:
        print(f"FAIL long straight: expected {n}, got {got}")
        return False

    # Long V: DR to (249,249), then clockwise turn to DL to (499,0).
    grid = [[0] * n for _ in range(n)]
    pos = 0
    for i in range(250):
        grid[i][i] = 1 if pos == 0 else (2 if (pos & 1) else 0)
        pos += 1

    r, c = 249, 249
    while r < n and c >= 0:
        r += 1
        c -= 1
        grid[r][c] = 2 if (pos & 1) else 0
        pos += 1

    got = sol.lenOfVDiagonal(grid)
    if got != 500:
        print(f"FAIL long V: expected 500, got {got}")
        return False

    # Random small-grid cross-check.
    random.seed(12345)
    for _ in range(2000):
        rn = random.randint(1, 6)
        rm = random.randint(1, 6)
        grid = [[random.randint(0, 2) for _ in range(rm)] for __ in range(rn)]
        got = sol.lenOfVDiagonal(grid)
        exp = brute_force(grid)
        if got != exp:
            print("FAIL random:")
            print("grid =", grid)
            print(f"expected {exp}, got {got}")
            return False

    print("PASS")
    return True


if __name__ == "__main__":
    verify()