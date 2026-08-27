import sys
import numpy as np


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2 + H]

    size = 1 << W

    vals = np.fromiter((int(s, 2) for s in rows), dtype=np.int64, count=len(rows))
    cnt = np.bincount(vals, minlength=size).astype(np.int64)

    # popcount for all masks
    idx = np.arange(size, dtype=np.int64)
    pc = np.zeros(size, dtype=np.int64)
    for i in range(W):
        pc += (idx >> i) & 1
    g = np.minimum(pc, W - pc).astype(np.int64)

    def wht(a):
        a = a.copy()
        h = 1
        n = a.size
        while h < n:
            b = a.reshape(-1, 2, h)
            x = b[:, 0, :].copy()
            y = b[:, 1, :].copy()
            b[:, 0, :] = x + y
            b[:, 1, :] = x - y
            a = b.reshape(-1)
            h <<= 1
        return a

    F = wht(cnt)
    G = wht(g)
    P = F * G
    f = wht(P)
    # exact division by 2^W
    f = f // size

    print(int(f.min()))


main()