import sys

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        print(0)
        return
    n = int(data[0])
    toks = data[1:1 + n]
    if len(toks) < n:
        n = len(toks)
    if n < 3:
        print(0)
        return

    # Small-input exact path (independent of FFT), also a safety net.
    if n <= 600:
        L = sorted(int(t) for t in toks)
        st = set(L)
        cnt = 0
        m = len(L)
        for i in range(m):
            a = L[i]
            for j in range(i + 1, m):
                c = L[j]
                s = a + c
                if not (s & 1) and (s >> 1) in st:
                    cnt += 1
        print(cnt)
        return

    import numpy as np

    try:
        S = np.array(toks, dtype=np.int64)
        # sanity: make sure conversion produced plausible values
        if S.shape[0] != n:
            raise ValueError
    except Exception:
        S = np.fromiter(map(int, toks), dtype=np.int64, count=n)

    mx = int(S.max())
    need = 2 * mx + 1
    size = 1
    while size < need:
        size <<= 1

    f = np.zeros(size, dtype=np.float64)
    f[S] = 1.0

    F = np.fft.rfft(f)
    del f
    F *= F
    g = np.fft.irfft(F, size)
    del F

    vals = np.rint(g[2 * S]).astype(np.int64)
    del g

    ans = int(((vals - 1) >> 1).sum())
    print(ans)

main()