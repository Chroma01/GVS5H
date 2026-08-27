from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        size = n * m
        g = [v for row in grid for v in row]
        # expected next value: after 1 -> 2, after 2 -> 0, after 0 -> 2
        NEXT = [2, 2, 0]
        nxtf = [NEXT[v] for v in g]

        # clockwise order: SE -> SW -> NW -> NE -> SE  ((dr,dc) -> (dc,-dr))
        DIRS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]

        # ---------- f[d]: longest straight chain starting at cell, direction d ----------
        F = []
        for di, dj in DIRS:
            f = [1] * size
            rows = range(n - 2, -1, -1) if di == 1 else range(1, n)
            for i in rows:
                b = i * m
                nb = (i + di) * m
                if dj == 1:
                    if m > 1:
                        f[b:b + m - 1] = [
                            fn + 1 if gn == e else 1
                            for gn, e, fn in zip(g[nb + 1:nb + m],
                                                 nxtf[b:b + m - 1],
                                                 f[nb + 1:nb + m])
                        ]
                else:
                    if m > 1:
                        f[b + 1:b + m] = [
                            fn + 1 if gn == e else 1
                            for gn, e, fn in zip(g[nb:nb + m - 1],
                                                 nxtf[b + 1:b + m],
                                                 f[nb:nb + m - 1])
                        ]
            F.append(f)

        # ---------- h[d]: longest chain starting at cell, direction d, one CW turn left ----------
        zero_row = [0] * m
        H = []
        for d in range(4):
            di, dj = DIRS[d]
            d2 = (d + 1) % 4
            di2, dj2 = DIRS[d2]
            fp = F[d2]
            h = [1] * size
            rows = range(n - 1, -1, -1) if di == 1 else range(0, n)
            for i in rows:
                b = i * m
                ni = i + di
                mi = i + di2

                # option A: continue in direction d (uses h[d] of neighbour row)
                if 0 <= ni < n:
                    nb = ni * m
                    if dj == 1:
                        if m > 1:
                            A = [
                                x if gn == e else 0
                                for gn, e, x in zip(g[nb + 1:nb + m],
                                                    nxtf[b:b + m - 1],
                                                    h[nb + 1:nb + m])
                            ]
                            A.append(0)
                        else:
                            A = zero_row
                    else:
                        if m > 1:
                            A = [0]
                            A.extend([
                                x if gn == e else 0
                                for gn, e, x in zip(g[nb:nb + m - 1],
                                                    nxtf[b + 1:b + m],
                                                    h[nb:nb + m - 1])
                            ])
                        else:
                            A = zero_row
                else:
                    A = zero_row

                # option B: turn here into d2 (uses f[d2] of neighbour in direction d2)
                if 0 <= mi < n:
                    mb = mi * m
                    if dj2 == 1:
                        if m > 1:
                            B = [
                                x if gn == e else 0
                                for gn, e, x in zip(g[mb + 1:mb + m],
                                                    nxtf[b:b + m - 1],
                                                    fp[mb + 1:mb + m])
                            ]
                            B.append(0)
                        else:
                            B = zero_row
                    else:
                        if m > 1:
                            B = [0]
                            B.extend([
                                x if gn == e else 0
                                for gn, e, x in zip(g[mb:mb + m - 1],
                                                    nxtf[b + 1:b + m],
                                                    fp[mb:mb + m - 1])
                            ])
                        else:
                            B = zero_row
                else:
                    B = zero_row

                h[b:b + m] = [1 + (a if a > c else c) for a, c in zip(A, B)]
            H.append(h)

        ones = [idx for idx in range(size) if g[idx] == 1]
        if not ones:
            return 0
        ans = 0
        for h in H:
            for idx in ones:
                v = h[idx]
                if v > ans:
                    ans = v
        return ans


# ---------------------------------------------------------------------------
# Task E: exhaustive brute force + randomized cross-check + timing (dev only)
# ---------------------------------------------------------------------------
def _brute(grid):
    """Exhaustive enumerator: every start cell with value 1, all 4 diagonal
    directions, sequence 1 then 2,0,2,0..., at most one 90-degree CLOCKWISE
    turn, turn cell counted once."""
    n, m = len(grid), len(grid[0])
    NEXT = {1: 2, 2: 0, 0: 2}
    DIRS = [(1, 1), (1, -1), (-1, -1), (-1, 1)]  # clockwise cycle
    best = 0
    for i in range(n):
        for j in range(m):
            if grid[i][j] != 1:
                continue
            if best < 1:
                best = 1
            for d in range(4):
                di, dj = DIRS[d]
                # straight run cells starting at (i,j)
                path = [(i, j)]
                ci, cj = i, j
                while True:
                    ni, nj = ci + di, cj + dj
                    if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == NEXT[grid[ci][cj]]:
                        path.append((ni, nj))
                        ci, cj = ni, nj
                    else:
                        break
                if len(path) > best:
                    best = len(path)
                di2, dj2 = DIRS[(d + 1) % 4]
                for p in range(len(path)):
                    ci, cj = path[p]
                    L = p + 1
                    while True:
                        ni, nj = ci + di2, cj + dj2
                        if 0 <= ni < n and 0 <= nj < m and grid[ni][nj] == NEXT[grid[ci][cj]]:
                            L += 1
                            ci, cj = ni, nj
                        else:
                            break
                    if L > best:
                        best = L
    return best


if __name__ == "__main__":
    import random
    import time

    sol = Solution()

    examples = [
        ([[2, 2, 1, 2, 2],
          [2, 0, 2, 2, 0],
          [2, 0, 1, 1, 0],
          [1, 0, 2, 2, 2],
          [2, 0, 0, 2, 2]], 5),
        ([[2, 2, 2, 2, 2],
          [2, 0, 2, 2, 0],
          [2, 0, 1, 1, 0],
          [1, 0, 2, 2, 2],
          [2, 0, 0, 2, 2]], 4),
        ([[1, 2, 2, 2, 2],
          [2, 2, 2, 2, 0],
          [2, 0, 0, 0, 0],
          [0, 0, 2, 2, 2],
          [2, 0, 0, 2, 0]], 5),
        ([[1]], 1),
    ]
    ok = True
    for gr, exp in examples:
        got = sol.lenOfVDiagonal([row[:] for row in gr])
        bf = _brute(gr)
        if got != exp or bf != exp:
            ok = False
            print("EXAMPLE MISMATCH", gr, "dp=", got, "brute=", bf, "expected=", exp)

    random.seed(12345)
    shapes = [(a, b) for a in range(1, 6) for b in range(1, 6)] + [(6, 4), (4, 6), (1, 7), (7, 1)]
    for trial in range(1200):
        n, m = random.choice(shapes)
        gr = [[random.choice((0, 1, 2)) for _ in range(m)] for _ in range(n)]
        got = sol.lenOfVDiagonal([row[:] for row in gr])
        bf = _brute(gr)
        if got != bf:
            ok = False
            print("MISMATCH on grid =", gr)
            print("  dp    =", got)
            print("  brute =", bf)
            break
    print("ALL OK" if ok else "FAILURES FOUND")

    # timing on worst-case 500x500 inputs
    N = 500
    g1 = [[2] * N for _ in range(N)]
    for _ in range(1000):
        g1[random.randrange(N)][random.randrange(N)] = 1
    g2 = [[2 if (i + j) % 2 == 0 else 0 for j in range(N)] for i in range(N)]
    for _ in range(500):
        g2[random.randrange(N)][random.randrange(N)] = 1
    g3 = [[1] * N for _ in range(N)]
    for name, gg in (("scattered-1s in 2s", g1), ("alternating 2/0", g2), ("all ones", g3)):
        t = time.perf_counter()
        r = sol.lenOfVDiagonal(gg)
        print(f"{name}: result={r}  time={time.perf_counter() - t:.3f}s")