from typing import List
import random


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        # 0: DR (1,1), 1: DL (1,-1), 2: UL (-1,-1), 3: UR (-1,1)
        # clockwise 90-degree successor of d is (d+1)%4  (screen coords, row down)
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))

        def rows_for(dr):
            # visit order so the target cell (row i+dr) is already computed
            return range(n - 1, -1, -1) if dr == 1 else range(n)

        # T[d][i][j]: length of the alternating run starting at (i,j) heading in
        # direction d with NO turn; its first value is grid[i][j].
        # The successor value is fixed by the current value: 1->2, 2->0, 0->2,
        # i.e. nxt = 2 if v != 2 else 0.
        T = []
        for d in range(4):
            dr, dc = dirs[d]
            Td = [[0] * m for _ in range(n)]
            for i in rows_for(dr):
                gi = grid[i]
                Tdi = Td[i]
                ni = i + dr
                if 0 <= ni < n:
                    gn = grid[ni]
                    Tdn = Td[ni]
                else:
                    gn = None
                    Tdn = None
                for j in range(m):
                    v = gi[j]
                    nxt = 2 if v != 2 else 0
                    nj = j + dc
                    if gn is not None and 0 <= nj < m and gn[nj] == nxt:
                        Tdi[j] = 1 + Tdn[nj]
                    else:
                        Tdi[j] = 1
            T.append(Td)

        ans = 0
        # F[d][i][j]: same as T but at most one clockwise turn is allowed at any
        # cell. Straight continuation keeps the turn option; turning consumes it.
        for d in range(4):
            dr, dc = dirs[d]
            d1 = (d + 1) & 3
            dr1, dc1 = dirs[d1]
            Td1 = T[d1]
            Fd = [[0] * m for _ in range(n)]
            for i in rows_for(dr):
                gi = grid[i]
                Fdi = Fd[i]
                ni = i + dr
                if 0 <= ni < n:
                    gn = grid[ni]
                    Fdn = Fd[ni]
                else:
                    gn = None
                    Fdn = None
                ni1 = i + dr1
                if 0 <= ni1 < n:
                    gn1 = grid[ni1]
                    Td1n = Td1[ni1]
                else:
                    gn1 = None
                    Td1n = None
                for j in range(m):
                    v = gi[j]
                    nxt = 2 if v != 2 else 0
                    best = 1
                    if gn is not None:
                        nj = j + dc
                        if 0 <= nj < m and gn[nj] == nxt:
                            best = 1 + Fdn[nj]
                    if gn1 is not None:
                        nj = j + dc1
                        if 0 <= nj < m and gn1[nj] == nxt:
                            c = 1 + Td1n[nj]
                            if c > best:
                                best = c
                    Fdi[j] = best
                    if v == 1 and best > ans:
                        ans = best
        return ans


# ---------------------------------------------------------------------------
# Independent brute force #1: enumerate (start cell with 1, initial direction,
# turn position along the straight arm) and extend greedily.  For a fixed
# start/direction/turn point the maximal segment is forced, so this is exhaustive.
# ---------------------------------------------------------------------------
def brute_greedy(grid: List[List[int]]) -> int:
    n = len(grid)
    m = len(grid[0])
    dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))
    best = 0
    for si in range(n):
        for sj in range(m):
            if grid[si][sj] != 1:
                continue
            for d0 in range(4):
                dr, dc = dirs[d0]
                er, ec = dirs[(d0 + 1) & 3]
                arm = [(si, sj)]
                ci, cj = si, sj
                k = 0
                while True:
                    a, b = ci + dr, cj + dc
                    if not (0 <= a < n and 0 <= b < m):
                        break
                    if grid[a][b] != (2 if (k + 1) % 2 == 1 else 0):
                        break
                    k += 1
                    ci, cj = a, b
                    arm.append((a, b))
                if k + 1 > best:
                    best = k + 1
                for p in range(k + 1):
                    cr, cc = arm[p]
                    idx = p
                    ln = p + 1
                    while True:
                        a, b = cr + er, cc + ec
                        if not (0 <= a < n and 0 <= b < m):
                            break
                        if grid[a][b] != (2 if (idx + 1) % 2 == 1 else 0):
                            break
                        idx += 1
                        cr, cc = a, b
                        ln += 1
                    if ln > best:
                        best = ln
    return best


# ---------------------------------------------------------------------------
# Independent brute force #2: DFS over (cell, direction, turn used, next value).
# ---------------------------------------------------------------------------
def brute_dfs(grid: List[List[int]]) -> int:
    n = len(grid)
    m = len(grid[0])
    dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))
    best = 0

    def go(i, j, d, turned, nxt, length):
        nonlocal best
        if length > best:
            best = length
        options = [(d, turned)]
        if not turned:
            options.append(((d + 1) & 3, True))   # clockwise turn, no step consumed
        for nd, nt in options:
            dr, dc = dirs[nd]
            a, b = i + dr, j + dc
            if 0 <= a < n and 0 <= b < m and grid[a][b] == nxt:
                go(a, b, nd, nt, 2 if nxt == 0 else 0, length + 1)

    for i in range(n):
        for j in range(m):
            if grid[i][j] == 1:
                if best < 1:
                    best = 1
                for d0 in range(4):
                    go(i, j, d0, False, 2, 1)
    return best


def plant_segment(grid, rng) -> int:
    n = len(grid)
    m = len(grid[0])
    dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))
    d0 = rng.randrange(4)
    d1 = (d0 + 1) & 3
    dr, dc = dirs[d0]
    er, ec = dirs[d1]
    lim = max(1, min(n, m))
    a = rng.randint(1, lim)
    b = rng.randint(0, lim)
    ci = rng.randrange(n)
    cj = rng.randrange(m)
    cells = [(ci, cj)]
    for _ in range(1, a):
        ci += dr
        cj += dc
        if not (0 <= ci < n and 0 <= cj < m):
            break
        cells.append((ci, cj))
    for _ in range(b):
        ci += er
        cj += ec
        if not (0 <= ci < n and 0 <= cj < m):
            break
        cells.append((ci, cj))
    for idx, (x, y) in enumerate(cells):
        grid[x][y] = 1 if idx == 0 else (2 if idx % 2 == 1 else 0)
    return len(cells)


def main():
    sol = Solution()
    problems = []

    def report(name, grid, expect, d, b1):
        ok = (d == b1) and (expect is None or d == expect)
        print(f"  {name}: expect={expect} dp={d} brute={b1} {'ok' if ok else 'FAIL'}")
        if not ok:
            problems.append((name, grid, expect, d, b1))

    print("== provided examples ==")
    examples = [
        ("ex1", [[2, 2, 1, 2, 2], [2, 0, 2, 2, 0], [2, 0, 1, 1, 0],
                 [1, 0, 2, 2, 2], [2, 0, 0, 2, 2]], 5),
        ("ex2", [[2, 2, 2, 2, 2], [2, 0, 2, 2, 0], [2, 0, 1, 1, 0],
                 [1, 0, 2, 2, 2], [2, 0, 0, 2, 2]], 4),
        ("ex3", [[1, 2, 2, 2, 2], [2, 2, 2, 2, 0], [2, 0, 0, 0, 0],
                 [0, 0, 2, 2, 2], [2, 0, 0, 2, 0]], 5),
        ("ex4", [[1]], 1),
    ]
    for nm, g, exp in examples:
        report(nm, g, exp, sol.lenOfVDiagonal(g), brute_greedy(g))

    print("== edge cases ==")
    edges = [
        ("1x1 zero", [[0]], 0),
        ("1x1 two", [[2]], 0),
        ("1x1 one", [[1]], 1),
        ("3x3 all 2", [[2, 2, 2], [2, 2, 2], [2, 2, 2]], 0),
        ("3x3 all 1", [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1),
        ("single row", [[1, 2, 0, 2, 0]], 1),
        ("single col", [[1], [2], [0], [2], [0]], 1),
        ("2x2 mix", [[1, 2], [2, 0]], 1),
        ("2x2 diag", [[1, 2], [2, 2]], 2),
        ("no 1 anywhere", [[0, 2], [2, 0]], 0),
        ("turn at first cell", [[1, 0, 0], [0, 2, 0], [0, 0, 0]], 3),
        ("2x3", [[1, 2, 0], [0, 2, 0]], 2),
        ("sparse 3x3", [[1, 0, 0], [0, 2, 0], [0, 0, 2]], 3),
        ("isolated-ish 1", [[2, 2, 2], [2, 1, 2], [2, 2, 2]], 2),
        ("two 1s", [[1, 2, 2], [2, 2, 2], [2, 2, 1]], 2),
    ]
    for nm, g, exp in edges:
        report(nm, g, exp, sol.lenOfVDiagonal(g), brute_greedy(g))

    rng = random.Random(20240607)

    print("== random grids, n,m<=6 (dp vs greedy brute) ==")
    mism = 0
    it = 0
    for it in range(2000):
        n = rng.randint(1, 6)
        m = rng.randint(1, 6)
        r = rng.random()
        if r < 0.45:
            pool = [0, 1, 2]
        elif r < 0.75:
            pool = [0, 1, 1, 2]
        else:
            pool = [2, 0, 0, 2, 1, 1]
        g = [[rng.choice(pool) for _ in range(m)] for _ in range(n)]
        d = sol.lenOfVDiagonal(g)
        b1 = brute_greedy(g)
        if d != b1:
            mism += 1
            print(f"  MISMATCH dp={d} brute={b1} grid={g!r}")
            problems.append(("random#%d" % it, g, None, d, b1))
            if mism >= 5:
                break
    print(f"  tested {it + 1} grids, mismatches {mism}")

    print("== random grids, n,m<=5 (dp vs greedy vs dfs) ==")
    mism2 = 0
    it = 0
    for it in range(400):
        n = rng.randint(1, 5)
        m = rng.randint(1, 5)
        g = [[rng.choice([0, 1, 2]) for _ in range(m)] for _ in range(n)]
        d = sol.lenOfVDiagonal(g)
        b1 = brute_greedy(g)
        b2 = brute_dfs(g)
        if not (d == b1 == b2):
            mism2 += 1
            print(f"  MISMATCH dp={d} greedy={b1} dfs={b2} grid={g!r}")
            problems.append(("dfs#%d" % it, g, None, d, b1))
            if mism2 >= 5:
                break
    print(f"  tested {it + 1} grids, mismatches {mism2}")

    print("== planted-segment grids (dp vs greedy, dp >= planted) ==")
    mism3 = 0
    it = 0
    for it in range(300):
        n = rng.randint(1, 7)
        m = rng.randint(1, 7)
        g = [[rng.choice([0, 1, 2]) for _ in range(m)] for _ in range(n)]
        planted = plant_segment(g, rng)
        d = sol.lenOfVDiagonal(g)
        b1 = brute_greedy(g)
        if d != b1 or d < planted:
            mism3 += 1
            print(f"  MISMATCH dp={d} brute={b1} planted={planted} grid={g!r}")
            problems.append(("planted#%d" % it, g, planted, d, b1))
            if mism3 >= 5:
                break
    print(f"  tested {it + 1} grids, mismatches {mism3}")

    if problems:
        print("\nFAILURES:")
        for name, g, exp, d, b1 in problems:
            print(f"  {name}: expect={exp} dp={d} brute={b1} grid={g!r}")
    else:
        print("\nALL OK")


if __name__ == "__main__":
    main()