import sys


def solve():
    MOD = 998244353
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    p = 0
    H0 = int(data[p])
    W0 = int(data[p + 1])
    p += 2

    # Keep the smaller dimension as the row dimension.
    if H0 <= W0:
        H = H0
        W = W0
        trans = False
    else:
        H = W0
        W = H0
        trans = True

    # Diagonal-row storage:
    # cell (r, c), s = r + c, is at index s * stride + (r + 1).
    stride = H + 2
    max_s = H + W - 2
    size = (max_s + 1) * stride
    A = [0] * size
    int_ = int

    # Fill A directly from the input.
    if not trans:
        for r in range(H):
            idx = r * stride + r + 1
            for _ in range(W):
                A[idx] = int_(data[p])
                p += 1
                idx += stride
    else:
        inc = stride + 1
        for r0 in range(H0):
            idx = r0 * stride + 1
            for _ in range(W0):
                A[idx] = int_(data[p])
                p += 1
                idx += inc

    Q = int_(data[p])
    sh = int_(data[p + 1])
    sw = int_(data[p + 2])
    p += 3
    qdata = data[p:]
    del data

    if trans:
        sh, sw = sw, sh

    # Precompute flat index lists for every anti-diagonal.
    Hm1 = H - 1
    Wm1 = W - 1
    diag = [None] * (max_s + 1)
    for ss in range(max_s + 1):
        rs = ss - Wm1
        if rs < 0:
            rs = 0
        re = ss
        if re > Hm1:
            re = Hm1
        first = ss * stride + rs + 1
        last = ss * stride + re + 1
        diag[ss] = list(range(first, last + 1))

    mod = MOD
    st = stride
    st1 = stride + 1

    # F[j] = A[j] * (sum of path products from start to j, excluding j)
    # G[j] = A[j] * (sum of path products from j to end, excluding j)
    F = [0] * size
    G = [0] * size
    start = 1
    end = max_s * stride + H
    F[start] = A[start]
    G[end] = A[end]

    for ss in range(1, max_s + 1):
        diag_s = diag[ss]
        for idx in diag_s:
            v = F[idx - st1] + F[idx - st]
            if v >= mod:
                v -= mod
            F[idx] = v * A[idx] % mod

    for ss in range(max_s - 1, -1, -1):
        diag_s = diag[ss]
        for idx in diag_s:
            v = G[idx + st] + G[idx + st1]
            if v >= mod:
                v -= mod
            G[idx] = v * A[idx] % mod

    ans = F[end]

    r = sh - 1
    c = sw - 1
    s = r + c
    base = s * stride

    # Direction tables.
    # L=76, R=82, U=85, D=68.
    dbase = [0] * 256
    dr = [0] * 256
    dc = [0] * 256
    ds = [0] * 256

    if not trans:
        # L
        dbase[76] = -st
        dr[76] = 0
        dc[76] = -1
        ds[76] = -1
        # R
        dbase[82] = st
        dr[82] = 0
        dc[82] = 1
        ds[82] = 1
        # U
        dbase[85] = -st
        dr[85] = -1
        dc[85] = 0
        ds[85] = -1
        # D
        dbase[68] = st
        dr[68] = 1
        dc[68] = 0
        ds[68] = 1
    else:
        # Original L/R/U/D become new U/D/L/R.
        # L -> U
        dbase[76] = -st
        dr[76] = -1
        dc[76] = 0
        ds[76] = -1
        # R -> D
        dbase[82] = st
        dr[82] = 1
        dc[82] = 0
        ds[82] = 1
        # U -> L
        dbase[85] = -st
        dr[85] = 0
        dc[85] = -1
        ds[85] = -1
        # D -> R
        dbase[68] = st
        dr[68] = 0
        dc[68] = 1
        ds[68] = 1

    out = []
    append = out.append
    to_str = str

    F_l = F
    G_l = G
    A_l = A
    diag_l = diag
    dbase_l = dbase
    dr_l = dr
    dc_l = dc
    ds_l = ds
    mod_l = mod
    st_l = st
    st1_l = st1
    max_s_l = max_s
    qdata_l = qdata
    p = 0

    for _ in range(Q):
        ch = qdata_l[p][0]
        new = int_(qdata_l[p + 1])
        p += 2

        d = ds_l[ch]
        base += dbase_l[ch]
        r += dr_l[ch]
        c += dc_l[ch]
        s += d
        pos = base + r + 1

        old = A_l[pos]
        if new != old:
            if s == 0:
                l = 1
            else:
                v = F_l[pos - st1_l] + F_l[pos - st_l]
                if v >= mod_l:
                    v -= mod_l
                l = v

            if s == max_s_l:
                rr = 1
            else:
                v = G_l[pos + st_l] + G_l[pos + st1_l]
                if v >= mod_l:
                    v -= mod_l
                rr = v

            add = ((new - old) * l * rr) % mod_l
            ans += add
            if ans >= mod_l:
                ans -= mod_l

            A_l[pos] = new

            # Update only the array that will not be recomputed below.
            if d == 1:
                G_l[pos] = rr * new % mod_l
            else:
                F_l[pos] = l * new % mod_l

        # Recompute the frontier diagonal.
        if d == 1:
            diag_s = diag_l[s]
            for idx in diag_s:
                v = F_l[idx - st1_l] + F_l[idx - st_l]
                if v >= mod_l:
                    v -= mod_l
                F_l[idx] = v * A_l[idx] % mod_l
        else:
            diag_s = diag_l[s]
            for idx in diag_s:
                v = G_l[idx + st_l] + G_l[idx + st1_l]
                if v >= mod_l:
                    v -= mod_l
                G_l[idx] = v * A_l[idx] % mod_l

        append(to_str(ans))

    sys.stdout.write('\n'.join(out))


if __name__ == '__main__':
    solve()