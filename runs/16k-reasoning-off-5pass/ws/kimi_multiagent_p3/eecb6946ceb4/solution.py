import sys

def solve():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    if n < 3:
        print(0)
        return
    V = max(S)

    try:
        import numpy as np
        size = 1
        while size < 2 * V + 1:
            size <<= 1
        f = np.zeros(size, dtype=np.float64)
        f[np.array(S, dtype=np.int64)] = 1.0
        F = np.fft.rfft(f)
        conv = np.fft.irfft(F * F, size)
        idx = np.array([2 * b for b in S], dtype=np.int64)
        c = np.rint(conv[idx]).astype(np.int64)
        ans = int(((c - 1) // 2).sum())
        print(ans)
    except ImportError:
        # Pure-Python fallback: for each middle B, scan d.
        present = bytearray(V + 1)
        for x in S:
            present[x] = 1
        ans = 0
        for b in S:
            lo = b - 1
            hi = V - b
            lim = lo if lo < hi else hi
            for d in range(1, lim + 1):
                if present[b - d] and present[b + d]:
                    ans += 1
        print(ans)

solve()