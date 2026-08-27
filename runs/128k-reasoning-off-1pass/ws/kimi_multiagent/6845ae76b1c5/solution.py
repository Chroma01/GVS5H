import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    p = 0
    N = int(data[p]); p += 1
    A = np.array(data[p:p + N], dtype=np.int64); p += N
    B = np.array(data[p:p + N], dtype=np.int64); p += N
    K = int(data[p]); p += 1
    X = [0] * K
    Y = [0] * K
    for k in range(K):
        X[k] = int(data[p]); Y[k] = int(data[p + 1]); p += 2

    C = 1000  # checkpoint spacing

    # y-checkpoints: sorted B-prefix (int32 values) + prefix sums (int64)
    ny = N // C
    sortedB = [None] * (ny + 1)
    psB = [None] * (ny + 1)
    for yi in range(1, ny + 1):
        s = np.sort(B[:yi * C].astype(np.int32))
        sortedB[yi] = s
        psB[yi] = np.concatenate((np.zeros(1, dtype=np.int64),
                                  s.astype(np.int64).cumsum()))

    # x-checkpoints: sorted A-prefix (int32 values) + prefix sums (int64)
    nx = N // C
    sortedA = [None] * (nx + 1)
    psA = [None] * (nx + 1)
    for xi in range(1, nx + 1):
        s = np.sort(A[:xi * C].astype(np.int32))
        sortedA[xi] = s
        psA[xi] = np.concatenate((np.zeros(1, dtype=np.int64),
                                  s.astype(np.int64).cumsum()))

    # grid[xi][yi] = F(xi*C, yi*C) = sum_{i<=xi*C, j<=yi*C} |A_i - B_j|
    # Full answers can reach 1e10 pairs * 2e8 = 2e21 > int64 max, so grid
    # entries are Python ints. Per-block g sums are <= 1000 * 2e13 = 2e16
    # (int64-safe) and are accumulated into a Python-int running total.
    grid = [[0] * (ny + 1) for _ in range(nx + 1)]
    A32 = A.astype(np.int32)
    for yi in range(1, ny + 1):
        s = sortedB[yi]
        ps = psB[yi]
        n = yi * C
        idx = np.searchsorted(s, A32, side='left').astype(np.int64)
        ple = ps[idx]
        # g_i = sum_{j<=yc} |A_i - B_j|, each <= 1e5 * 2e8 = 2e13 (int64-safe)
        g = A * idx - ple + (ps[n] - ple) - A * (n - idx)
        running = 0  # Python int
        for xi in range(1, nx + 1):
            block = g[(xi - 1) * C: xi * C]
            running += int(block.sum())  # <= 2e16, int64-safe
            grid[xi][yi] = running

    out = []
    for k in range(K):
        x = X[k]; y = Y[k]
        xi = x // C
        yi = y // C
        xc = xi * C
        yc = yi * C
        ans = grid[xi][yi]  # Python int

        stripX = A[xc:x]          # A_i for i in (xc, x]
        stripY = B[yc:y]          # B_j for j in (yc, y]

        # part 1: sum_{i in stripX} sum_{j<=yc} |A_i - B_j|
        if yi > 0 and stripX.size:
            s = sortedB[yi]
            ps = psB[yi]
            n = yc
            idx = np.searchsorted(s, stripX.astype(np.int32),
                                  side='left').astype(np.int64)
            ple = ps[idx]
            g = stripX * idx - ple + (ps[n] - ple) - stripX * (n - idx)
            ans += int(g.sum())  # <= 999 * 2e13, int64-safe

        # part 2: sum_{j in stripY} sum_{i<=xc} |A_i - B_j|
        if xi > 0 and stripY.size:
            s = sortedA[xi]
            ps = psA[xi]
            n = xc
            idx = np.searchsorted(s, stripY.astype(np.int32),
                                  side='left').astype(np.int64)
            ple = ps[idx]
            h = stripY * idx - ple + (ps[n] - ple) - stripY * (n - idx)
            ans += int(h.sum())

        # corner: sum_{i in stripX, j in stripY} |A_i - B_j|
        if stripX.size and stripY.size:
            t = np.sort(stripY)
            pt = np.concatenate((np.zeros(1, dtype=np.int64), t.cumsum()))
            m = t.size
            idx = np.searchsorted(t, stripX,
                                  side='left').astype(np.int64)
            ple = pt[idx]
            c = stripX * idx - ple + (pt[m] - ple) - stripX * (m - idx)
            ans += int(c.sum())

        out.append(str(ans))

    sys.stdout.write("\n".join(out) + "\n")


main()