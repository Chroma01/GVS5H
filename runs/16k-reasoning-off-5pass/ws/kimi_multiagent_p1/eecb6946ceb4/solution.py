import sys

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    n = int(data[0])
    S = list(map(int, data[1:1 + n]))
    if n < 3:
        print(0)
        return

    import numpy as np

    maxv = max(S)
    size = maxv + 1
    f = np.zeros(size, dtype=np.float64)
    f[np.array(S, dtype=np.int64)] = 1.0

    # Convolution length needed: 2*maxv + 1
    need = 2 * maxv + 1
    L = 1 << (need - 1).bit_length()

    F = np.fft.rfft(f, L)
    g = np.fft.irfft(F * F, L)[:need]
    g = np.rint(g).astype(np.int64)

    idx = 2 * np.array(S, dtype=np.int64)
    total = int(g[idx].sum(dtype=np.int64))
    ans = (total - n) // 2
    print(ans)

solve()