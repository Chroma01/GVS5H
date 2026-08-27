import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    N = int(data[0]); P = int(data[1])
    maxM = N * (N - 1) // 2
    if N == 2:
        sys.stdout.write(str(1 % P) + "\n")
        return
    h = N // 2

    inv = [0] * (N + 2)
    for i in range(1, N + 2):
        inv[i] = pow(i, P - 2, P)

    C = [[0] * (N + 2) for _ in range(N + 2)]
    for i in range(N + 2):
        C[i][0] = 1
        for j in range(1, i + 1):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    # exact integer coefficients of ((1+x)^a - 1)*(1+x)^c , stored as (k, coef) with coef != 0
    mult = {}
    for a in range(1, N + 1):
        for c in range(0, N - a + 1):
            n = a + c
            co = [C[n][k] - (C[c][k] if k <= c else 0) for k in range(n + 1)]
            mult[(a, c)] = [(k, v) for k, v in enumerate(co) if v]

    offs = [max(0, t - h) for t in range(N + 2)]
    rws = [min(t, h) - max(0, t - h) + 1 for t in range(N + 2)]
    plens = [t * (t - 1) // 2 + 1 for t in range(N + 2)]

    a0 = np.zeros((rws[1], plens[1]), dtype=np.int64)
    a0[1 - offs[1], 0] = 1 % P
    lev = {(1, 1, 0): a0}

    for t in range(1, N):
        cur = lev
        # ---- close a layer:  (p,a,c) -> (1-p,c,0)   (only c>=1, no polynomial change)
        for key in list(cur.keys()):
            p, a, c = key
            if c == 0:
                continue
            k2 = (1 - p, c, 0)
            src = cur[key]
            d = cur.get(k2)
            if d is None:
                cur[k2] = src.copy()
            else:
                d += src
                d %= P
        # ---- add one vertex to the current layer
        nxt = {}
        rt, ot, Lt = rws[t], offs[t], plens[t]
        rt1, ot1, Lt1 = rws[t + 1], offs[t + 1], plens[t + 1]
        rem = (N - t) % P
        for (p, a, c), src in cur.items():
            if c + 1 > h:
                continue
            delta = ot + (1 if p == 0 else 0) - ot1
            i0 = -delta
            if i0 < 0:
                i0 = 0
            i1 = rt1 - 1 - delta
            if i1 > rt - 1:
                i1 = rt - 1
            if i1 < i0:
                continue
            mr = src.any(axis=1)
            if not mr.any():
                continue
            lo = int(mr.argmax())
            hi = rt - 1 - int(mr[::-1].argmax())
            if lo > i0:
                i0 = lo
            if hi < i1:
                i1 = hi
            if i1 < i0:
                continue
            block = src[i0:i1 + 1]
            mc = block.any(axis=0)
            if not mc.any():
                continue
            lc = int(mc.argmax())
            hc = Lt - int(mc[::-1].argmax())
            w = hc - lc
            sc = rem * inv[c + 1] % P
            if sc == 0:
                continue
            sub = block[:, lc:hc] * sc % P
            deg = a + c
            tmp = np.zeros((i1 - i0 + 1, w + deg), dtype=np.int64)
            for k, cf in mult[(a, c)]:
                tmp[:, k:k + w] += cf * sub
            tmp %= P
            key2 = (p, a, c + 1)
            d = nxt.get(key2)
            if d is None:
                d = np.zeros((rt1, Lt1), dtype=np.int64)
                nxt[key2] = d
            d[i0 + delta:i1 + delta + 1, lc:lc + w + deg] += tmp
        lev = nxt

    res = np.zeros(maxM + 1, dtype=np.int64)
    orow = h - offs[N]
    for (p, a, c), src in lev.items():
        if c >= 1:
            res += src[orow]
            res %= P
    out = ' '.join(str(int(res[m] % P)) for m in range(N - 1, maxM + 1))
    sys.stdout.write(out + "\n")


main()