import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)

    H = int(next(it))
    W = int(next(it))
    N = H * W

    grid = [0] * N
    for i in range(N):
        grid[i] = int(next(it))

    Q = int(next(it))
    sh = int(next(it))
    sw = int(next(it))

    queries = []
    cnt_lr = 0
    cnt_ud = 0
    for _ in range(Q):
        d = next(it)[0]
        a = int(next(it))
        queries.append((d, a))
        if d == 76 or d == 82:  # L, R
            cnt_lr += 1
        else:                   # U, D
            cnt_ud += 1

    del data, it

    # Choose orientation.  Usually the smaller dimension is best, but if both
    # dimensions are moderate, the walk direction counts can make the other
    # orientation cheaper.
    MAX_R = 700
    best = None

    # No transpose: rows = H, horizontal moves are original L/R.
    if H <= MAX_R or H <= W:
        cost = H * (Q + cnt_lr)
        best = (cost, H, False)

    # Transpose: rows = W, horizontal moves are original U/D.
    if W <= MAX_R or W < H:
        cost = W * (Q + cnt_ud)
        if best is None or cost < best[0] or (cost == best[0] and W < best[1]):
            best = (cost, W, True)

    transposed = best[2]

    if transposed:
        R, C = W, H
        # New column = original row, new row = original column.
        A = [grid[i * W:(i + 1) * W] for i in range(H)]
        r = sw - 1
        c = sh - 1
    else:
        R, C = H, W
        # New column = original column, new row = original row.
        A = [grid[i::W] for i in range(W)]
        r = sh - 1
        c = sw - 1

    del grid

    mod = MOD

    # Forward DP: F[c][i] = sum of products from (0,0) to (i,c), inclusive.
    F = [[0] * R for _ in range(C)]
    for c0 in range(C):
        colA = A[c0]
        colF = F[c0]
        if c0 == 0:
            colF[0] = colA[0]
            for i in range(1, R):
                colF[i] = colA[i] * colF[i - 1] % mod
        else:
            prevF = F[c0 - 1]
            colF[0] = colA[0] * prevF[0] % mod
            for i in range(1, R):
                s = colF[i - 1] + prevF[i]
                if s >= mod:
                    s -= mod
                colF[i] = colA[i] * s % mod

    # Backward DP stored reversed by row:
    # G[c][k] = B[c][R-1-k], where B is sum from (i,c) to (R-1,C-1), inclusive.
    # This makes affected parts of B also recomputable top-down.
    G = [[0] * R for _ in range(C)]
    for c0 in range(C - 1, -1, -1):
        colA = A[c0]
        colG = G[c0]
        if c0 == C - 1:
            colG[0] = colA[R - 1]
            for k in range(1, R):
                colG[k] = colA[R - 1 - k] * colG[k - 1] % mod
        else:
            nextG = G[c0 + 1]
            colG[0] = colA[R - 1] * nextG[0] % mod
            for k in range(1, R):
                s = colG[k - 1] + nextG[k]
                if s >= mod:
                    s -= mod
                colG[k] = colA[R - 1 - k] * s % mod

    ans = F[C - 1][R - 1]

    # Direction maps in the chosen orientation.
    dr = [0] * 91
    dc = [0] * 91
    if transposed:
        # original L -> up, R -> down, U -> left, D -> right
        dr[76] = -1
        dr[82] = 1
        dc[85] = -1
        dc[68] = 1
    else:
        # original L -> left, R -> right, U -> up, D -> down
        dc[76] = -1
        dc[82] = 1
        dr[85] = -1
        dr[68] = 1

    out = []
    append = out.append

    for d, a in queries:
        dcm = dc[d]
        r += dr[d]
        c += dcm

        colA = A[c]
        old = colA[r]

        # If the value does not change, only a stale DP column may need refresh.
        if old == a:
            if dcm > 0:  # moved right: F[c] may be stale
                colF = F[c]
                if c == 0:
                    colF[0] = colA[0]
                    for i in range(1, R):
                        colF[i] = colA[i] * colF[i - 1] % mod
                else:
                    prevF = F[c - 1]
                    colF[0] = colA[0] * prevF[0] % mod
                    for i in range(1, R):
                        s = colF[i - 1] + prevF[i]
                        if s >= mod:
                            s -= mod
                        colF[i] = colA[i] * s % mod
            elif dcm < 0:  # moved left: G[c] may be stale
                colG = G[c]
                if c == C - 1:
                    colG[0] = colA[R - 1]
                    for k in range(1, R):
                        colG[k] = colA[R - 1 - k] * colG[k - 1] % mod
                else:
                    nextG = G[c + 1]
                    colG[0] = colA[R - 1] * nextG[0] % mod
                    for k in range(1, R):
                        s = colG[k - 1] + nextG[k]
                        if s >= mod:
                            s -= mod
                        colG[k] = colA[R - 1 - k] * s % mod

            append(str(ans))
            continue

        if dcm == 0:
            # Vertical move: both F[c] and G[c] are fresh.
            colF = F[c]
            colG = G[c]

            if r == 0 and c == 0:
                L = 1
            else:
                L = 0
                if r > 0:
                    L = colF[r - 1]
                if c > 0:
                    L += F[c - 1][r]
                    if L >= mod:
                        L -= mod

            srow = R - 1 - r
            if r == R - 1 and c == C - 1:
                Rex = 1
            else:
                Rex = 0
                if srow > 0:
                    Rex = colG[srow - 1]
                if c + 1 < C:
                    Rex += G[c + 1][srow]
                    if Rex >= mod:
                        Rex -= mod

            ans = (ans + (a - old) * L % mod * Rex) % mod
            colA[r] = a

            # Recompute affected suffix of F[c].
            if c == 0:
                if r == 0:
                    colF[0] = colA[0]
                    start = 1
                else:
                    start = r
                for i in range(start, R):
                    colF[i] = colA[i] * colF[i - 1] % mod
            else:
                prevF = F[c - 1]
                if r == 0:
                    colF[0] = colA[0] * prevF[0] % mod
                    start = 1
                else:
                    start = r
                for i in range(start, R):
                    s = colF[i - 1] + prevF[i]
                    if s >= mod:
                        s -= mod
                    colF[i] = colA[i] * s % mod

            # Recompute affected suffix of reversed G[c].
            if c == C - 1:
                if srow == 0:
                    colG[0] = colA[R - 1]
                    start = 1
                else:
                    start = srow
                for k in range(start, R):
                    colG[k] = colA[R - 1 - k] * colG[k - 1] % mod
            else:
                nextG = G[c + 1]
                if srow == 0:
                    colG[0] = colA[R - 1] * nextG[0] % mod
                    start = 1
                else:
                    start = srow
                for k in range(start, R):
                    s = colG[k - 1] + nextG[k]
                    if s >= mod:
                        s -= mod
                    colG[k] = colA[R - 1 - k] * s % mod

        elif dcm > 0:
            # Moved right: F[c] may be stale, G[c] is fresh.
            colF = F[c]
            colG = G[c]
            prevF = F[c - 1]

            # Compute old prefix of F[c] needed for L.
            if r > 0:
                colF[0] = colA[0] * prevF[0] % mod
                for i in range(1, r):
                    s = colF[i - 1] + prevF[i]
                    if s >= mod:
                        s -= mod
                    colF[i] = colA[i] * s % mod
                L = colF[r - 1] + prevF[r]
                if L >= mod:
                    L -= mod
            else:
                L = prevF[0]

            srow = R - 1 - r
            if r == R - 1 and c == C - 1:
                Rex = 1
            else:
                Rex = 0
                if srow > 0:
                    Rex = colG[srow - 1]
                if c + 1 < C:
                    Rex += G[c + 1][srow]
                    if Rex >= mod:
                        Rex -= mod

            ans = (ans + (a - old) * L % mod * Rex) % mod
            colA[r] = a

            # Finish F[c] with the new value.
            if r == 0:
                colF[0] = colA[0] * prevF[0] % mod
                start = 1
            else:
                start = r
            for i in range(start, R):
                s = colF[i - 1] + prevF[i]
                if s >= mod:
                    s -= mod
                colF[i] = colA[i] * s % mod

            # Update affected suffix of G[c].
            if c == C - 1:
                if srow == 0:
                    colG[0] = colA[R - 1]
                    start = 1
                else:
                    start = srow
                for k in range(start, R):
                    colG[k] = colA[R - 1 - k] * colG[k - 1] % mod
            else:
                nextG = G[c + 1]
                if srow == 0:
                    colG[0] = colA[R - 1] * nextG[0] % mod
                    start = 1
                else:
                    start = srow
                for k in range(start, R):
                    s = colG[k - 1] + nextG[k]
                    if s >= mod:
                        s -= mod
                    colG[k] = colA[R - 1 - k] * s % mod

        else:
            # Moved left: G[c] may be stale, F[c] is fresh.
            colF = F[c]
            colG = G[c]

            if r == 0 and c == 0:
                L = 1
            else:
                L = 0
                if r > 0:
                    L = colF[r - 1]
                if c > 0:
                    L += F[c - 1][r]
                    if L >= mod:
                        L -= mod

            srow = R - 1 - r
            nextG = G[c + 1]

            # Compute old prefix of reversed G[c] needed for Rex.
            if srow > 0:
                colG[0] = colA[R - 1] * nextG[0] % mod
                for k in range(1, srow):
                    s = colG[k - 1] + nextG[k]
                    if s >= mod:
                        s -= mod
                    colG[k] = colA[R - 1 - k] * s % mod
                Rex = colG[srow - 1] + nextG[srow]
                if Rex >= mod:
                    Rex -= mod
            else:
                Rex = nextG[0]

            ans = (ans + (a - old) * L % mod * Rex) % mod
            colA[r] = a

            # Finish G[c] with the new value.
            if srow == 0:
                colG[0] = colA[R - 1] * nextG[0] % mod
                start = 1
            else:
                start = srow
            for k in range(start, R):
                s = colG[k - 1] + nextG[k]
                if s >= mod:
                    s -= mod
                colG[k] = colA[R - 1 - k] * s % mod

            # Update affected suffix of F[c].
            if c == 0:
                if r == 0:
                    colF[0] = colA[0]
                    start = 1
                else:
                    start = r
                for i in range(start, R):
                    colF[i] = colA[i] * colF[i - 1] % mod
            else:
                prevF = F[c - 1]
                if r == 0:
                    colF[0] = colA[0] * prevF[0] % mod
                    start = 1
                else:
                    start = r
                for i in range(start, R):
                    s = colF[i - 1] + prevF[i]
                    if s >= mod:
                        s -= mod
                    colF[i] = colA[i] * s % mod

        append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    main()