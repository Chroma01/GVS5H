import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    size = 1 << W

    # Build frequency table of row masks
    freq = [0] * size
    for r in rows:
        m = 0
        for ch in r:
            m = (m << 1) | (ch - 48)
        freq[m] += 1

    # f[v] = min(popcount(v), W - popcount(v))
    f = [0] * size
    for v in range(1, size):
        pc = bin(v).count('1')
        f[v] = pc if pc <= W - pc else W - pc

    # g(c) = sum_m freq[m] * f(m XOR c)  -- XOR convolution
    try:
        import numpy as np
        a = np.array(freq, dtype=np.int64)
        b = np.array(f, dtype=np.int64)
        n = size
        h = 1
        while h < n:
            a = a.reshape(-1, 2, h)
            x = a[:, 0, :].copy()
            y = a[:, 1, :]
            a[:, 0, :] = x + y
            a[:, 1, :] = x - y
            a = a.reshape(-1)
            b = b.reshape(-1, 2, h)
            x = b[:, 0, :].copy()
            y = b[:, 1, :]
            b[:, 0, :] = x + y
            b[:, 1, :] = x - y
            b = b.reshape(-1)
            h <<= 1
        c = a * b
        h = 1
        while h < n:
            c = c.reshape(-1, 2, h)
            x = c[:, 0, :].copy()
            y = c[:, 1, :]
            c[:, 0, :] = x + y
            c[:, 1, :] = x - y
            c = c.reshape(-1)
            h <<= 1
        c //= n
        ans = int(c.min())
    except ImportError:
        # Fallback: iterate over distinct masks only
        distinct = [(m, cnt) for m, cnt in enumerate(freq) if cnt]
        best = None
        for cmask in range(size):
            total = 0
            for m, cnt in distinct:
                total += f[m ^ cmask] * cnt
            if best is None or total < best:
                best = total
        ans = best

    print(ans)

main()