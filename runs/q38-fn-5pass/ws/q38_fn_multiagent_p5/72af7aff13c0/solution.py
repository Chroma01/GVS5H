import sys

MOD = 998244353


def solve():
    input = sys.stdin.buffer.readline

    H0, W0 = map(int, input().split())
    A0 = [list(map(int, input().split())) for _ in range(H0)]

    Q, sh, sw = map(int, input().split())
    sh -= 1
    sw -= 1

    dirs = [0] * Q
    vals = [0] * Q
    vert = 0
    horiz = 0

    for i in range(Q):
        line = input().split()
        ch = line[0][0]
        a = int(line[1])
        vals[i] = a
        if ch == 76:          # L
            dirs[i] = 0
            horiz += 1
        elif ch == 82:        # R
            dirs[i] = 1
            horiz += 1
        elif ch == 85:        # U
            dirs[i] = 2
            vert += 1
        else:                 # D
            dirs[i] = 3
            vert += 1

    # Choose orientation.  In the chosen orientation:
    # horizontal cursor moves are O(1), vertical cursor moves cost O(W).
    cost0 = vert * (W0 - 1)
    cost1 = horiz * (H0 - 1)

    if cost1 < cost0 or (cost1 == cost0 and horiz < vert):
        transpose = True
    else:
        transpose = False

    if transpose:
        H = W0
        W = H0
        A = [[0] * W for _ in range(H)]
        for i in range(H0):
            row = A0[i]
            for j in range(W0):
                A[j][i] = row[j]
        del A0

        r = sw
        c = sh

        # L -> U, R -> D, U -> L, D -> R
        mp = (2, 3, 0, 1)
        for i in range(Q):
            dirs[i] = mp[dirs[i]]
    else:
        H = H0
        W = W0
        A = A0
        r = sh
        c = sw

    mod = MOD

    # Forward DP: F[h][w] = sum of products of paths from (0,0) to (h,w), inclusive.
    F = [[0] * W for _ in range(H)]

    a0 = A[0]
    f0 = F[0]
    f0[0] = a0[0]
    left = f0[0]
    for j in range(1, W):
        left = a0[j] * left % mod
        f0[j] = left

    for i in range(1, H):
        a = A[i]
        f = F[i]
        fp = F[i - 1]
        left = 0
        for j in range(W):
            s = left + fp[j]
            if s >= mod:
                s -= mod
            left = a[j] * s % mod
            f[j] = left

    # Backward DP: B[h][w] = sum of products of paths from (h,w) to (H-1,W-1), inclusive.
    B = [[0] * W for _ in range(H)]

    a = A[H - 1]
    b = B[H - 1]
    right = a[W - 1]
    b[W - 1] = right
    for j in range(W - 2, -1, -1):
        right = a[j] * right % mod
        b[j] = right

    for i in range(H - 2, -1, -1):
        a = A[i]
        b = B[i]
        bd = B[i + 1]
        right = 0
        for j in range(W - 1, -1, -1):
            s = bd[j] + right
            if s >= mod:
                s -= mod
            right = a[j] * s % mod
            b[j] = right

    ans = F[H - 1][W - 1]

    # Full-row flags, used only for rows where the invariant requires full correctness.
    # They are conservative: False may mean "maybe not full", True is always safe.
    f_full = [True] * H
    b_full = [True] * H

    def get_fex(rr, cc, F=F, mod=mod):
        if rr == 0 and cc == 0:
            return 1
        s = 0
        if rr > 0:
            s = F[rr - 1][cc]
        if cc > 0:
            s += F[rr][cc - 1]
            if s >= mod:
                s -= mod
        return s

    def get_bex(rr, cc, B=B, H=H, W=W, mod=mod):
        if rr == H - 1 and cc == W - 1:
            return 1
        s = 0
        if rr + 1 < H:
            s = B[rr + 1][cc]
        if cc + 1 < W:
            s += B[rr][cc + 1]
            if s >= mod:
                s -= mod
        return s

    def setF(rr, cc, A=A, F=F, mod=mod):
        val = A[rr][cc]
        if rr == 0:
            if cc == 0:
                F[0][0] = val
            else:
                F[0][cc] = val * F[0][cc - 1] % mod
        else:
            left = F[rr][cc - 1] if cc else 0
            s = left + F[rr - 1][cc]
            if s >= mod:
                s -= mod
            F[rr][cc] = val * s % mod

    def setB(rr, cc, A=A, B=B, H=H, W=W, mod=mod):
        val = A[rr][cc]
        if rr == H - 1:
            if cc == W - 1:
                B[rr][cc] = val
            else:
                B[rr][cc] = val * B[rr][cc + 1] % mod
        else:
            s = B[rr + 1][cc]
            if cc + 1 < W:
                s += B[rr][cc + 1]
                if s >= mod:
                    s -= mod
            B[rr][cc] = val * s % mod

    def rf_prefix(rr, end, A=A, F=F, mod=mod):
        if end < 0:
            return
        a = A[rr]
        f = F[rr]
        if rr == 0:
            f[0] = a[0]
            left = f[0]
            for j in range(1, end + 1):
                left = a[j] * left % mod
                f[j] = left
        else:
            fp = F[rr - 1]
            left = 0
            for j in range(end + 1):
                s = left + fp[j]
                if s >= mod:
                    s -= mod
                left = a[j] * s % mod
                f[j] = left

    def rf_suffix(rr, start, A=A, F=F, W=W, mod=mod):
        if start >= W:
            return
        a = A[rr]
        f = F[rr]
        if start == 0:
            if rr == 0:
                f[0] = a[0]
                left = f[0]
                for j in range(1, W):
                    left = a[j] * left % mod
                    f[j] = left
            else:
                fp = F[rr - 1]
                left = 0
                for j in range(W):
                    s = left + fp[j]
                    if s >= mod:
                        s -= mod
                    left = a[j] * s % mod
                    f[j] = left
        else:
            left = f[start - 1]
            if rr == 0:
                for j in range(start, W):
                    left = a[j] * left % mod
                    f[j] = left
            else:
                fp = F[rr - 1]
                for j in range(start, W):
                    s = left + fp[j]
                    if s >= mod:
                        s -= mod
                    left = a[j] * s % mod
                    f[j] = left

    def rb_suffix(rr, start, A=A, B=B, H=H, W=W, mod=mod):
        if start >= W:
            return
        a = A[rr]
        b = B[rr]
        if rr == H - 1:
            right = a[W - 1]
            b[W - 1] = right
            j = W - 2
            while j >= start:
                right = a[j] * right % mod
                b[j] = right
                j -= 1
        else:
            bd = B[rr + 1]
            right = 0
            for j in range(W - 1, start - 1, -1):
                s = bd[j] + right
                if s >= mod:
                    s -= mod
                right = a[j] * s % mod
                b[j] = right

    def rb_prefix(rr, start, A=A, B=B, H=H, W=W, mod=mod):
        if start < 0:
            return
        a = A[rr]
        b = B[rr]
        if rr == H - 1:
            if start == W - 1:
                right = a[W - 1]
                b[W - 1] = right
                j = W - 2
            else:
                right = b[start + 1]
                j = start
            while j >= 0:
                right = a[j] * right % mod
                b[j] = right
                j -= 1
        else:
            bd = B[rr + 1]
            right = b[start + 1] if start + 1 < W else 0
            for j in range(start, -1, -1):
                s = bd[j] + right
                if s >= mod:
                    s -= mod
                right = a[j] * s % mod
                b[j] = right

    gF = get_fex
    gB = get_bex
    sF = setF
    sB = setB
    rfp = rf_prefix
    rfs = rf_suffix
    rbs = rb_suffix
    rbp = rb_prefix

    out = []
    append = out.append

    for qi in range(Q):
        d = dirs[qi]
        a = vals[qi]

        if d < 2:  # horizontal move: L or R
            if d == 0:
                c -= 1
            else:
                c += 1

            rr = r
            cc = c

            fex = gF(rr, cc)
            bex = gB(rr, cc)

            old = A[rr][cc]
            changed = old != a
            if changed:
                if fex and bex:
                    ans = (ans + (a - old) * fex % mod * bex) % mod
                A[rr][cc] = a

            sF(rr, cc)
            sB(rr, cc)

            if cc == W - 1:
                f_full[rr] = True
            elif changed:
                f_full[rr] = False

            if cc == 0:
                b_full[rr] = True
            elif changed:
                b_full[rr] = False

        elif d == 2:  # U
            nr = r - 1
            cc = c

            if cc + 1 < W:
                rbs(nr, cc + 1)

            fex = gF(nr, cc)
            bex = gB(nr, cc)

            old = A[nr][cc]
            changed = old != a
            if changed:
                if fex and bex:
                    ans = (ans + (a - old) * fex % mod * bex) % mod
                A[nr][cc] = a

            sF(nr, cc)

            if cc > 0 and not b_full[r]:
                rbp(r, cc - 1)
            b_full[r] = True

            sB(nr, cc)

            f_full[r] = False
            f_full[nr] = (cc == W - 1)
            b_full[nr] = (cc == 0)

            r = nr

        else:  # D
            nr = r + 1
            cc = c

            if cc > 0:
                rfp(nr, cc - 1)

            fex = gF(nr, cc)
            bex = gB(nr, cc)

            old = A[nr][cc]
            changed = old != a
            if changed:
                if fex and bex:
                    ans = (ans + (a - old) * fex % mod * bex) % mod
                A[nr][cc] = a

            if cc + 1 < W and not f_full[r]:
                rfs(r, cc + 1)
            f_full[r] = True

            sF(nr, cc)
            sB(nr, cc)

            b_full[r] = False
            f_full[nr] = (cc == W - 1)
            b_full[nr] = (cc == 0)

            r = nr

        append(str(ans))

    sys.stdout.write("\n".join(out))


if __name__ == "__main__":
    solve()