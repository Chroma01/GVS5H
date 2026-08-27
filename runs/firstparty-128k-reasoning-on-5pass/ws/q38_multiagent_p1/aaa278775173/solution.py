from typing import List
from array import array

class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        n = len(grid)
        m = len(grid[0])
        total = n * m

        flat = [0] * total
        idx = 0
        has_one = False
        for r in range(n):
            row = grid[r]
            for c, v in enumerate(row):
                flat[idx] = v
                if v == 1:
                    has_one = True
                idx += 1

        if not has_one:
            return 0

        # Directions: DR, DL, UL, UR. Clockwise next is (d + 1) % 4.
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))
        orders = (
            (range(n), range(m)),
            (range(n), range(m - 1, -1, -1)),
            (range(n - 1, -1, -1), range(m - 1, -1, -1)),
            (range(n - 1, -1, -1), range(m)),
        )

        dp0 = []
        ans = 0

        # dp0[d][i]: longest no-turn valid segment ending at i moving in direction d.
        for d in range(4):
            dr, dc = dirs[d]
            step = dr * m + dc
            arr = array('H', [0]) * total
            dp0.append(arr)

            for r in orders[d][0]:
                base = r * m
                for c in orders[d][1]:
                    i = base + c
                    v = flat[i]
                    best = 1 if v == 1 else 0

                    pr = r - dr
                    pc = c - dc
                    if 0 <= pr < n and 0 <= pc < m:
                        plen = arr[i - step]
                        if plen:
                            need = 2 if (plen & 1) else 0
                            if v == need:
                                cand = plen + 1
                                if cand > best:
                                    best = cand

                    arr[i] = best
                    if best > ans:
                        ans = best

        # dp1[i]: longest one-turn valid segment ending at i moving in current direction d.
        for d in range(4):
            dr, dc = dirs[d]
            step = dr * m + dc
            prev_dir = (d + 3) % 4
            dp0_prev = dp0[prev_dir]
            dp1 = array('H', [0]) * total

            for r in orders[d][0]:
                base = r * m
                for c in orders[d][1]:
                    i = base + c
                    v = flat[i]
                    best = 0

                    pr = r - dr
                    pc = c - dc
                    if 0 <= pr < n and 0 <= pc < m:
                        p = i - step

                        # Continue an already turned segment.
                        plen1 = dp1[p]
                        if plen1:
                            need = 2 if (plen1 & 1) else 0
                            if v == need:
                                cand = plen1 + 1
                                if cand > best:
                                    best = cand

                        # Make the single clockwise turn at p.
                        plen0 = dp0_prev[p]
                        if plen0 >= 2:
                            need = 2 if (plen0 & 1) else 0
                            if v == need:
                                cand = plen0 + 1
                                if cand > best:
                                    best = cand

                    dp1[i] = best
                    if best > ans:
                        ans = best

        return ans


def _run_samples() -> None:
    cases = [
        (
            [[2, 2, 1, 2, 2],
             [2, 0, 2, 2, 0],
             [2, 0, 1, 1, 0],
             [1, 0, 2, 2, 2],
             [2, 0, 0, 2, 2]],
            5,
        ),
        (
            [[2, 2, 2, 2, 2],
             [2, 0, 2, 2, 0],
             [2, 0, 1, 1, 0],
             [1, 0, 2, 2, 2],
             [2, 0, 0, 2, 2]],
            4,
        ),
        (
            [[1, 2, 2, 2, 2],
             [2, 2, 2, 2, 0],
             [2, 0, 0, 0, 0],
             [0, 0, 2, 2, 2],
             [2, 0, 0, 2, 0]],
            5,
        ),
        ([[1]], 1),
    ]

    sol = Solution()
    overall = True
    for idx, (grid, expected) in enumerate(cases, 1):
        actual = sol.lenOfVDiagonal(grid)
        passed = actual == expected
        overall = overall and passed
        verdict = "PASSED" if passed else "FAILED"
        print(f"Sample {idx}: actual={actual} expected={expected} {verdict}")
    print(f"Overall: {'PASSED' if overall else 'FAILED'}")


if __name__ == "__main__":
    _run_samples()