import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read()
    arr = np.frombuffer(data, dtype=np.uint8)
    if arr.size == 0:
        return
    isd = arr > 47
    if not isd.any():
        return
    prev = np.empty(isd.size, dtype=bool)
    prev[0] = False
    prev[1:] = isd[:-1]
    starts = np.flatnonzero(isd & ~prev)
    nxt = np.empty(isd.size, dtype=bool)
    nxt[-1] = False
    nxt[:-1] = isd[1:]
    ends = np.flatnonzero(isd & ~nxt)
    lengths = ends - starts + 1
    maxlen = int(lengths.max())
    digits = arr - 48
    vals = np.zeros(starts.size, dtype=np.int64)
    for k in range(maxlen):
        sel = lengths > k
        idx = starts[sel] + k
        vals[sel] = vals[sel] * 10 + digits[idx]
    del arr, isd, prev, nxt, starts, ends, lengths, digits, data

    n = int(vals[0])
    K = int(vals[1])
    A = vals[2:2 + n].astype(np.int32)
    del vals

    M = int(A.max())

    # ---- phase 1: counts of each value ----
    c = np.bincount(A, minlength=M + 1).astype(np.int32)

    # ---- phase 2: cnt[d] = # of elements divisible by d ----
    cnt = np.zeros(M + 1, dtype=np.int32)
    S = M + 1 if M + 1 < 10000 else 10000
    for d in range(1, S):
        cnt[d] = c[d::d].sum()

    tmax = M // S if S <= M else 0
    for t in range(tmax, 0, -1):
        lo = M // (t + 1) + 1
        if lo < S:
            lo = S
        hi = M // t
        if lo > hi:
            continue
        acc = c[lo:hi + 1].copy()
        for k in range(2, t + 1):
            acc += c[k * lo:k * hi + 1:k]
        cnt[lo:hi + 1] = acc
    del c

    # ---- phase 3: f[v] = max good divisor of v ----
    good = cnt >= K
    del cnt
    f = np.ones(M + 1, dtype=np.int32)
    for d in range(2, S):
        if good[d]:
            f[d::d] = d

    for t in range(tmax, 0, -1):
        lo = M // (t + 1) + 1
        if lo < S:
            lo = S
        hi = M // t
        if lo > hi:
            continue
        g = good[lo:hi + 1]
        if not g.any():
            continue
        vv = np.arange(lo, hi + 1, dtype=np.int32)
        for k in range(1, t + 1):
            np.copyto(f[k * lo:k * hi + 1:k], vv, where=g)

    out = f[A]
    sys.stdout.write('\n'.join(map(str, out.tolist())))
    sys.stdout.write('\n')


if __name__ == '__main__':
    main()