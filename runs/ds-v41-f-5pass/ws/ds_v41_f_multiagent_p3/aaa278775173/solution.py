from typing import List


class Solution:
    def lenOfVDiagonal(self, grid: List[List[int]]) -> int:
        n = len(grid)
        m = len(grid[0])
        size = n * m
        g = [grid[r][c] for r in range(n) for c in range(m)]

        # value at position k of the sequence: k=0 -> 1, odd k -> 2, even k>=2 -> 0
        nxt = (2, 2, 0)              # nxt[0]=2, nxt[1]=2, nxt[2]=0
        DR, DL, UL, UR = 0, 1, 2, 3
        dr = (1, 1, -1, -1)          # DR, DL, UL, UR
        dc = (1, -1, -1, 1)
        cw = (DL, UL, UR, DR)        # clockwise 90 degree turn

        # ---- out[d][i]: length of the straight run starting at cell i in direction d,
        #      values following the sequence starting from g[i] ----
        out = [None] * 4
        for d in range(4):
            drd = dr[d]
            dcd = dc[d]
            od = [1] * size
            step = drd * m + dcd
            if drd == 1:                       # successor is r+1: row n-1 has none
                rows = range(n - 2, -1, -1)
            else:
                rows = range(1, n)
            if dcd == 1:                       # successor is c+1: col m-1 has none
                cols = range(m - 2, -1, -1)
            else:
                cols = range(1, m)
            for r in rows:
                base = r * m
                nb = base + step
                for c in cols:
                    i = base + c
                    j = nb + c
                    if g[j] == nxt[g[i]]:
                        od[i] = od[j] + 1
            out[d] = od

        # ---- f[i]: longest valid straight prefix ending at i, i.e. a chain that
        #      starts at a value-1 cell and follows 1,2,0,2,0,... ----
        base_f = [1 if x == 1 else 0 for x in g]   # cells without a predecessor
        ans = 1 if 1 in g else 0
        for d in range(4):
            drd = dr[d]
            dcd = dc[d]
            ocd = out[cw[d]]
            step = drd * m + dcd
            f = base_f[:]                          # boundary cells keep their base value
            if drd == 1:                           # travel downwards
                rows = range(1, n)
            else:
                rows = range(n - 2, -1, -1)
            if dcd == 1:                           # travel rightwards
                cols = range(1, m)
            else:
                cols = range(m - 2, -1, -1)
            for r in rows:
                base = r * m
                pb = base - step
                for c in cols:
                    idx = base + c
                    v = g[idx]
                    pidx = pb + c
                    pv = g[pidx]
                    if v == 1:
                        pre = 1
                    elif v == 2:                   # predecessor may be 1 or 0
                        pf = f[pidx]
                        pre = pf + 1 if (pf and pv != 2) else 0
                    else:                          # v == 0, predecessor must be 2
                        pf = f[pidx]
                        pre = pf + 1 if (pf and pv == 2) else 0
                    f[idx] = pre
                    if pre:
                        if pre > ans:
                            ans = pre
                        t = pre + ocd[idx] - 1     # one turn here, sharing the cell
                        if t > ans:
                            ans = t
        return ans


if __name__ == "__main__":
    import random
    import time

    # ---------------- sample tests ----------------
    samples = [
        ([[2, 2, 1, 2, 2], [2, 0, 2, 2, 0], [2, 0, 1, 1, 0],
          [1, 0, 2, 2, 2], [2, 0, 0, 2, 2]], 5),
        ([[2, 2, 2, 2, 2], [2, 0, 2, 2, 0], [2, 0, 1, 1, 0],
          [1, 0, 2, 2, 2], [2, 0, 0, 2, 2]], 4),
        ([[1, 2, 2, 2, 2], [2, 2, 2, 2, 0], [2, 0, 0, 0, 0],
          [0, 0, 2, 2, 2], [2, 0, 0, 2, 0]], 5),
        ([[1]], 1),
    ]
    sol = Solution()
    all_ok = True
    for i, (gr, exp) in enumerate(samples, 1):
        got = sol.lenOfVDiagonal(gr)
        ok = got == exp
        all_ok = all_ok and ok
        print("Example %d: got %d, expected %d -> %s" % (i, got, exp, "OK" if ok else "FAIL"))
    print("sample tests:", "all pass" if all_ok else "FAILURE")

    # ---------------- brute force simulator ----------------
    def brute(grid):
        n = len(grid)
        m = len(grid[0])
        seq = [1] + [2 if (k & 1) else 0 for k in range(1, n + m + 5)]
        dirs = ((1, 1), (1, -1), (-1, -1), (-1, 1))   # DR, DL, UL, UR (clockwise order)
        best = 0
        for r in range(n):
            for c in range(m):
                if grid[r][c] != 1:
                    continue
                for d0 in range(4):
                    dr0, dc0 = dirs[d0]
                    # maximal straight run from (r,c) in direction d0
                    path = [(r, c)]
                    cr, cc, k = r, c, 1
                    while True:
                        nr, nc = cr + dr0, cc + dc0
                        if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == seq[k]:
                            path.append((nr, nc))
                            cr, cc, k = nr, nc, k + 1
                        else:
                            break
                    if len(path) > best:
                        best = len(path)
                    # clockwise 90 degree turn at each prefix cell
                    dr1, dc1 = dirs[(d0 + 1) & 3]
                    for t in range(len(path)):
                        tr, tc = path[t]
                        cr, cc, k, ln = tr, tc, t + 1, t + 1
                        while True:
                            nr, nc = cr + dr1, cc + dc1
                            if 0 <= nr < n and 0 <= nc < m and grid[nr][nc] == seq[k]:
                                ln += 1
                                cr, cc, k = nr, nc, k + 1
                            else:
                                break
                        if ln > best:
                            best = ln
        return best

    # ---------------- differential test ----------------
    random.seed(20240517)
    tests = []
    for _ in range(500):
        n = random.randint(1, 6)
        m = random.randint(1, 6)
        alpha = random.choice([[0, 1, 2], [1, 2], [2, 0], [1, 0], [1], [2], [0], [0, 2]])
        tests.append([[random.choice(alpha) for _ in range(m)] for _ in range(n)])
    # structured edge cases
    tests.append([[1]])
    tests.append([[1, 2], [2, 0]])
    tests.append([[2, 0], [0, 2]])
    tests.append([[1] * 4 for _ in range(4)])
    tests.append([[2] * 4 for _ in range(4)])
    tests.append([[0] * 4 for _ in range(4)])
    tests.append([[1 if (r + c) % 3 == 0 else (2 if (r + c) % 3 == 1 else 0)
                   for c in range(6)] for r in range(6)])
    tests.append([[1 if (r - c) % 3 == 0 else (2 if (r - c) % 3 == 1 else 0)
                   for c in range(6)] for r in range(6)])
    tests.append([[1, 0, 2, 0, 2], [2, 2, 2, 2, 2], [0, 0, 0, 0, 0],
                  [2, 2, 2, 2, 2], [0, 0, 0, 0, 0]])
    tests.append([[1, 2, 0, 2, 0], [2, 0, 2, 2, 2], [0, 2, 1, 2, 0],
                  [2, 2, 2, 0, 2], [0, 0, 2, 2, 2]])

    mism = 0
    for gr in tests:
        a = sol.lenOfVDiagonal(gr)
        b = brute(gr)
        if a != b:
            mism += 1
            if mism <= 5:
                print("MISMATCH dp=%d brute=%d grid=%r" % (a, b, gr))
    print("differential test: %d grids, %d mismatches" % (len(tests), mism))

    # ---------------- performance sanity check ----------------
    big = [[random.choice([0, 1, 2]) for _ in range(500)] for _ in range(500)]
    t0 = time.time()
    res = sol.lenOfVDiagonal(big)
    print("500x500 random grid: result=%d, time=%.3fs" % (res, time.time() - t0))