import sys


def compute_Gt(W):
    # g_w = min(w, W-w);  Gt[t] = FWHT(g)[k] for any k with popcount(k)=t
    #           = sum_w g_w * K_w(t)   (Krawtchouk polynomial)
    g = [min(w, W - w) for w in range(W + 1)]
    Gt = [0] * (W + 1)
    for t in range(W + 1):
        val = g[0]                      # K_0 = 1
        if W >= 1:
            d = W - 2 * t
            Kprev = 1                   # K_0
            Kcur = d                    # K_1
            val += g[1] * Kcur
            for w in range(1, W):
                Knxt = (d * Kcur - (W - w + 1) * Kprev) // (w + 1)
                val += g[w + 1] * Knxt
                Kprev, Kcur = Kcur, Knxt
        Gt[t] = val
    return Gt


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    n = 1 << W
    rows = data[2:2 + H]

    Gt = compute_Gt(W)

    try:
        import numpy as np
    except Exception:
        np = None

    if np is not None:
        f = np.zeros(n, dtype=np.int64)
        for r in rows:
            m = 0
            for ch in r:
                m = (m << 1) | (ch & 1)
            f[m] += 1

        h = 1
        while h < n:
            b = f.reshape(-1, h << 1)
            x = b[:, :h].copy()
            y = b[:, h:].copy()
            b[:, :h] = x + y
            b[:, h:] = x - y
            h <<= 1

        idx = np.arange(n, dtype=np.int64)
        pc = np.zeros(n, dtype=np.int64)
        for i in range(W):
            pc += (idx >> i) & 1
        f *= np.array(Gt, dtype=np.int64)[pc]

        h = 1
        while h < n:
            b = f.reshape(-1, h << 1)
            x = b[:, :h].copy()
            y = b[:, h:].copy()
            b[:, :h] = x + y
            b[:, h:] = x - y
            h <<= 1

        ans = int(f.min()) // n
        sys.stdout.write(str(ans) + "\n")
        return

    # ---- pure python fallback ----
    f = [0] * n
    for r in rows:
        m = 0
        for ch in r:
            m = (m << 1) | (ch & 1)
        f[m] += 1

    h = 1
    if n >= 2:
        lo = f[0::2]
        hi = f[1::2]
        f[0::2] = [x + y for x, y in zip(lo, hi)]
        f[1::2] = [x - y for x, y in zip(lo, hi)]
        h = 2
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            j = i + h
            lo = f[i:j]
            hi = f[j:j + h]
            f[i:j] = [x + y for x, y in zip(lo, hi)]
            f[j:j + h] = [x - y for x, y in zip(lo, hi)]
        h = step

    pc = [0] * n
    for k in range(1, n):
        pc[k] = pc[k >> 1] + (k & 1)
    for k in range(n):
        f[k] *= Gt[pc[k]]

    h = 1
    if n >= 2:
        lo = f[0::2]
        hi = f[1::2]
        f[0::2] = [x + y for x, y in zip(lo, hi)]
        f[1::2] = [x - y for x, y in zip(lo, hi)]
        h = 2
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            j = i + h
            lo = f[i:j]
            hi = f[j:j + h]
            f[i:j] = [x + y for x, y in zip(lo, hi)]
            f[j:j + h] = [x - y for x, y in zip(lo, hi)]
        h = step

    sys.stdout.write(str(min(f) // n) + "\n")


main()