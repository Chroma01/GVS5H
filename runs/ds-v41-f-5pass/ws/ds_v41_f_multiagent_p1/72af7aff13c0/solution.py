import sys

try:
    import numpy as np
    HAVE_NUMPY = True
except Exception:
    HAVE_NUMPY = False

MOD = 998244353
NP_THRESHOLD = 0   # force numpy path whenever numpy is available


def main():
    data = sys.stdin.buffer.read().split()
    pos = 0
    H = int(data[pos]); pos += 1
    W = int(data[pos]); pos += 1
    HW = H * W
    A_vals = list(map(int, data[pos:pos + HW]))
    pos += HW
    Q = int(data[pos]); pos += 1
    sh = int(data[pos]); pos += 1
    sw = int(data[pos]); pos += 1

    D = H + W
    lo = [0] * (D + 2)
    Nd = [0] * (D + 2)
    for d in range(2, D + 1):
        l = d - W
        if l < 1:
            l = 1
        hi = d - 1
        if hi > H:
            hi = H
        lo[d] = l
        Nd[d] = hi - l + 1

    M = MOD
    mind = H if H < W else W
    use_np = HAVE_NUMPY and mind >= NP_THRESHOLD

    out = []
    ap = out.append

    if use_np:
        A_flat = np.array(A_vals, dtype=np.int64)
        del A_vals
        Ad = [None] * (D + 2)
        Fpad = [None] * (D + 2)
        Gpad = [None] * (D + 2)
        for d in range(2, D + 1):
            l = lo[d]; n = Nd[d]
            hs = np.arange(l, l + n, dtype=np.int64)
            flat = (hs - 1) * W + (d - hs - 1)
            Ad[d] = A_flat[flat]
            Fpad[d] = np.zeros(n + 2, dtype=np.int64)
            Gpad[d] = np.zeros(n + 2, dtype=np.int64)
        del A_flat

        npadd = np.add
        npmul = np.multiply
        npmod = np.mod

        Fpad[2][1] = int(Ad[2][0]) % M
        for d in range(3, D + 1):
            n = Nd[d]
            prev = Fpad[d - 1]
            s = lo[d] - lo[d - 1] - 1
            o = Fpad[d][1:n + 1]
            npadd(prev[s + 1:s + 1 + n], prev[s + 2:s + 2 + n], out=o)
            npmul(o, Ad[d], out=o)
            npmod(o, M, out=o)

        Gpad[D][1] = int(Ad[D][0]) % M
        for d in range(D - 1, 1, -1):
            n = Nd[d]
            nxt = Gpad[d + 1]
            s = lo[d] - lo[d + 1]
            o = Gpad[d][1:n + 1]
            npadd(nxt[s + 1:s + 1 + n], nxt[s + 2:s + 2 + n], out=o)
            npmul(o, Ad[d], out=o)
            npmod(o, M, out=o)

        ans = int(Fpad[D][1])
        h = sh; w = sw; dprev = sh + sw

        for _ in range(Q):
            c = data[pos][0]; pos += 1
            a = int(data[pos]); pos += 1
            if c == 76:        # L
                w -= 1
            elif c == 82:      # R
                w += 1
            elif c == 85:      # U
                h -= 1
            else:              # D
                h += 1
            d = h + w
            if d > dprev:
                n = Nd[d]
                prev = Fpad[d - 1]
                s = lo[d] - lo[d - 1] - 1
                o = Fpad[d][1:n + 1]
                npadd(prev[s + 1:s + 1 + n], prev[s + 2:s + 2 + n], out=o)
                npmul(o, Ad[d], out=o)
                npmod(o, M, out=o)
            else:
                n = Nd[d]
                nxt = Gpad[d + 1]
                s = lo[d] - lo[d + 1]
                o = Gpad[d][1:n + 1]
                npadd(nxt[s + 1:s + 1 + n], nxt[s + 2:s + 2 + n], out=o)
                npmul(o, Ad[d], out=o)
                npmod(o, M, out=o)

            lod = lo[d]
            if h == 1 and w == 1:
                pre = 1
            else:
                l2 = lo[d - 1]
                pre = 0
                if h > 1:
                    pre = int(Fpad[d - 1][(h - 1) - l2 + 1])
                if w > 1:
                    pre += int(Fpad[d - 1][h - l2 + 1])
                pre %= M

            if h == H and w == W:
                suf = 1
            else:
                l2 = lo[d + 1]
                suf = 0
                if h < H:
                    suf = int(Gpad[d + 1][(h + 1) - l2 + 1])
                if w < W:
                    suf += int(Gpad[d + 1][h - l2 + 1])
                suf %= M

            i = h - lod
            old = int(Ad[d][i])
            Ad[d][i] = a
            delta = (a - old) % M * pre % M * suf % M
            ans = (ans + delta) % M
            Fpad[d][i + 1] = a * pre % M
            Gpad[d][i + 1] = a * suf % M
            dprev = d
            ap(ans)

        sys.stdout.write('\n'.join(map(str, out)) + '\n')
        return

    # ---------- pure python fallback ----------
    Adp = [None] * (D + 2)
    for d in range(2, D + 1):
        l = lo[d]; n = Nd[d]
        Adp[d] = [A_vals[(l + i - 1) * W + (d - l - i - 1)] for i in range(n)]
    del A_vals

    Fp = [None] * (D + 2)
    Gp = [None] * (D + 2)
    for d in range(2, D + 1):
        sz = Nd[d] + 2
        Fp[d] = [0] * sz
        Gp[d] = [0] * sz

    Fp[2][1] = Adp[2][0] % M
    for d in range(3, D + 1):
        prev = Fp[d - 1]; cur = Fp[d]; A = Adp[d]
        sp = lo[d] - lo[d - 1]
        for i in range(Nd[d]):
            cur[i + 1] = (prev[sp + i] + prev[sp + i + 1]) * A[i] % M

    Gp[D][1] = Adp[D][0] % M
    for d in range(D - 1, 1, -1):
        nxt = Gp[d + 1]; cur = Gp[d]; A = Adp[d]
        sp = lo[d] - lo[d + 1] + 1
        for i in range(Nd[d]):
            cur[i + 1] = (nxt[sp + i] + nxt[sp + i + 1]) * A[i] % M

    ans = Fp[D][1]
    h = sh; w = sw; dprev = sh + sw
    rng = range

    for _ in range(Q):
        c = data[pos][0]; pos += 1
        a = int(data[pos]); pos += 1
        if c == 76:
            w -= 1
        elif c == 82:
            w += 1
        elif c == 85:
            h -= 1
        else:
            h += 1
        d = h + w
        if d > dprev:
            prev = Fp[d - 1]; cur = Fp[d]; A = Adp[d]
            sp = lo[d] - lo[d - 1]
            for i in rng(Nd[d]):
                cur[i + 1] = (prev[sp + i] + prev[sp + i + 1]) * A[i] % M
        else:
            nxt = Gp[d + 1]; cur = Gp[d]; A = Adp[d]
            sp = lo[d] - lo[d + 1] + 1
            for i in rng(Nd[d]):
                cur[i + 1] = (nxt[sp + i] + nxt[sp + i + 1]) * A[i] % M

        lod = lo[d]
        if h == 1 and w == 1:
            pre = 1
        else:
            l2 = lo[d - 1]
            pre = 0
            if h > 1:
                pre = Fp[d - 1][(h - 1) - l2 + 1]
            if w > 1:
                pre += Fp[d - 1][h - l2 + 1]
            pre %= M

        if h == H and w == W:
            suf = 1
        else:
            l2 = lo[d + 1]
            suf = 0
            if h < H:
                suf = Gp[d + 1][(h + 1) - l2 + 1]
            if w < W:
                suf += Gp[d + 1][h - l2 + 1]
            suf %= M

        i = h - lod
        old = Adp[d][i]
        Adp[d][i] = a
        delta = (a - old) % M * pre % M * suf % M
        ans = (ans + delta) % M
        Fp[d][i + 1] = a * pre % M
        Gp[d][i + 1] = a * suf % M
        dprev = d
        ap(ans)

    sys.stdout.write('\n'.join(map(str, out)) + '\n')


main()