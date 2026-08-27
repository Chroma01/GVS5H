import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    size = 1 << W

    freq = [0] * size
    for line in rows:
        mask = 0
        for ch in line:
            mask = (mask << 1) | (ch & 1)  # '0'->0, '1'->1
        freq[mask] += 1

    # h[v] = min(popcount(v), W - popcount(v))
    h = [0] * size
    for v in range(1, size):
        h[v] = h[v >> 1] + (v & 1)
    for v in range(size):
        p = h[v]
        q = W - p
        if q < p:
            h[v] = q

    # XOR convolution via FWHT: conv[c] = sum_p freq[p] * h[p XOR c]
    try:
        import numpy as np
        a = np.array(freq, dtype=np.int64)
        b = np.array(h, dtype=np.int64)
        n = size
        step = 1
        while step < n:
            a = a.reshape(-1, 2, step)
            x = a[:, 0, :].copy()
            y = a[:, 1, :]
            a[:, 0, :] = x + y
            a[:, 1, :] = x - y
            a = a.reshape(-1)
            b = b.reshape(-1, 2, step)
            x = b[:, 0, :].copy()
            y = b[:, 1, :]
            b[:, 0, :] = x + y
            b[:, 1, :] = x - y
            b = b.reshape(-1)
            step <<= 1
        conv = a * b
        # inverse FWHT (same butterfly), then divide by n
        step = 1
        while step < n:
            conv = conv.reshape(-1, 2, step)
            x = conv[:, 0, :].copy()
            y = conv[:, 1, :]
            conv[:, 0, :] = x + y
            conv[:, 1, :] = x - y
            conv = conv.reshape(-1)
            step <<= 1
        conv //= n
        ans = int(conv.min())
    except ImportError:
        a = freq[:]
        b = h[:]
        n = size
        step = 1
        while step < n:
            for i in range(0, n, step << 1):
                for j in range(i, i + step):
                    x = a[j]; y = a[j + step]
                    a[j] = x + y
                    a[j + step] = x - y
                    x = b[j]; y = b[j + step]
                    b[j] = x + y
                    b[j + step] = x - y
            step <<= 1
        conv = [a[i] * b[i] for i in range(n)]
        step = 1
        while step < n:
            for i in range(0, n, step << 1):
                for j in range(i, i + step):
                    x = conv[j]; y = conv[j + step]
                    conv[j] = x + y
                    conv[j + step] = x - y
            step <<= 1
        ans = min(c // n for c in conv)

    print(ans)

main()