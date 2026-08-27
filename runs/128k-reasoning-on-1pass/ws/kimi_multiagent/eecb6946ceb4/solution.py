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

    M = max(S)
    need = 2 * M + 1
    size = 1
    while size < need:
        size <<= 1

    try:
        import numpy as np
        a = np.zeros(size, dtype=np.float64)
        a[np.asarray(S, dtype=np.int64)] = 1.0
        f = np.fft.rfft(a)
        q = np.fft.irfft(f * f, size)
        conv = np.rint(q).astype(np.int64)

        ans = 0
        for b in S:
            ans += (int(conv[2 * b]) - 1) // 2
        print(ans)
        return
    except ImportError:
        pass

    # Fallback for environments without numpy. Correct, but only practical
    # for much smaller inputs than the full constraints.
    import math

    a = [0j] * size
    for v in S:
        a[v] = 1.0 + 0j

    def fft(x, invert):
        m = len(x)
        j = 0
        for i in range(1, m):
            bit = m >> 1
            while j & bit:
                j ^= bit
                bit >>= 1
            j |= bit
            if i < j:
                x[i], x[j] = x[j], x[i]

        length = 2
        while length <= m:
            ang = 2.0 * math.pi / length * (-1.0 if invert else 1.0)
            wlen = complex(math.cos(ang), math.sin(ang))
            half = length >> 1
            for i in range(0, m, length):
                w = 1.0 + 0j
                for k in range(i, i + half):
                    u = x[k]
                    v = x[k + half] * w
                    x[k] = u + v
                    x[k + half] = u - v
                    w *= wlen
            length <<= 1

        if invert:
            inv = 1.0 / m
            for i in range(m):
                x[i] *= inv

    fft(a, False)
    for i in range(size):
        a[i] *= a[i]
    fft(a, True)
    conv = [int(round(a[i].real)) for i in range(size)]

    ans = 0
    for b in S:
        ans += (conv[2 * b] - 1) // 2
    print(ans)


solve()