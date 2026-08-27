import sys
import numpy as np


def parse_ints(buf):
    """Parse whitespace-separated integers from a bytes buffer into an int64 array.

    Fast path uses NumPy's bulk bytes->int conversion (works on most versions);
    falls back to a guaranteed-correct fromiter(map(int, ...)) path otherwise.
    """
    tokens = buf.split()
    if not tokens:
        return np.empty(0, dtype=np.int64)
    try:
        arr = np.array(tokens, dtype=np.int64)
        if arr.dtype != np.int64 or arr.size != len(tokens):
            raise ValueError
        return arr
    except Exception:
        return np.fromiter(map(int, tokens), dtype=np.int64, count=len(tokens))


def main():
    data = parse_ints(sys.stdin.buffer.read())
    if data.size == 0:
        return
    pos = 0
    N = int(data[pos]); pos += 1
    A = data[pos:pos + N]; pos += N
    Q = int(data[pos]) if pos < data.size else 0
    pos += 1
    if Q <= 0:
        return
    LR = data[pos:pos + 2 * Q]
    if LR.size < 2 * Q:                      # degenerate / truncated input guard
        Q = LR.size // 2
        if Q == 0:
            return
        LR = LR[:2 * Q]
    L = LR[0::2].copy()
    R = LR[1::2].copy()

    # f[i] = first index j with A[j] >= 2*A[i]  (N if none)
    # since A_i >= 1, 2*A[i] > A[i]  =>  f[i] > i  =>  g[i] >= 1
    f = np.searchsorted(A, 2 * A, side='left')
    idx = np.arange(N, dtype=np.int64)
    g = (f - idx).astype(np.int32)

    # ---- feasibility algebra (0-indexed l = L-1, r = R-1, m = r-l+1) ----
    # K feasible  <=>  2*A[l+t] <= A[r-K+1+t] for all t=0..K-1
    #             <=>  r-K+1+t >= f[l+t]      for all t
    #             <=>  f[l+t] - (l+t) <= (r-l+1) - K = m - K
    #             <=>  max(g[l .. l+K-1]) <= m - K
    # plus K <= m//2.  Monotone in K: the max is nondecreasing in K while m-K
    # decreases, so the predicate is a downward-closed (monotone) condition.
    #
    # Index safety proof (why no clipping is needed):
    #   a = l >= 0 because L >= 1.
    #   length = max(mid, 1), p = 2^floor(log2(length)) <= length, so
    #   b = l + length - p >= l >= 0 and a + p - 1 <= b + p - 1 = l + length - 1.
    #   If mid >= 1 then length = mid <= hi = m//2, hence
    #   l + length - 1 <= l + m - 1 = r <= N-1.
    #   If mid == 0 then length = 1, p = 1, a = b = l <= N-1.
    #   Therefore every sparse-table access is inside [0, N-1].

    # ---- sparse table (2-D, padded tail never queried on valid ranges) ----
    LEV = 1
    while (1 << LEV) <= N:
        LEV += 1
    ST = np.empty((LEV, N), dtype=np.int32)
    ST[0] = g
    for k in range(1, LEV):
        half = 1 << (k - 1)
        prev = ST[k - 1]
        cur = ST[k]
        if N - half > 0:
            np.maximum(prev[:N - half], prev[half:], out=cur[:N - half])
            cur[N - half:] = prev[N - half:]   # padding, never queried
        else:
            cur[:] = prev

    # LOG[i] = floor(log2(i))  for i >= 1
    LOG = np.zeros(N + 2, dtype=np.int64)
    k = 1
    while (1 << k) <= N + 1:
        LOG[(1 << k):] += 1
        k += 1

    l = L - 1
    r = R - 1
    m = r - l + 1
    lo = np.zeros(Q, dtype=np.int64)
    hi = m // 2

    for _ in range(20):
        active = lo < hi
        if not active.any():
            break
        mid = (lo + hi + 1) >> 1
        length = np.maximum(mid, 1)          # avoid length-0 range queries
        kk = LOG[length]
        p = np.left_shift(np.int64(1), kk)
        a = l
        b = l + length - p
        rmax = np.maximum(ST[kk, a], ST[kk, b]).astype(np.int64)
        ok = (mid == 0) | (rmax <= (m - mid))
        adv = active & ok
        lo = np.where(adv, mid, lo)
        hi = np.where(active & ~ok, mid - 1, hi)

    out = '\n'.join(map(str, lo.tolist()))
    sys.stdout.write(out)
    sys.stdout.write('\n')


main()