import sys
import numpy as np

def solve():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]

    size = 1 << W
    freq = np.zeros(size, dtype=np.int64)
    for s in rows:
        m = 0
        for ch in s:
            m = (m << 1) | (ch == 49)  # ord('1') == 49
        freq[m] += 1

    # Polynomial Walsh-Hadamard transform.
    # P[m] starts as the constant polynomial freq[m].
    # Butterfly per bit: (a, b) -> (a + y*b, y*a + b).
    # After all W bits, P[c][k] = sum_m freq[m] * [popcount(m XOR c) == k].
    P = np.zeros((size, W + 1), dtype=np.int64)
    P[:, 0] = freq

    for bit in range(W):
        step = 1 << bit
        period = step << 1
        Q = P.reshape(size // period, 2, step, W + 1)
        a = Q[:, 0].copy()
        b = Q[:, 1].copy()
        yb = np.zeros_like(b)
        yb[:, :, 1:] = b[:, :, :-1]   # y * b
        ya = np.zeros_like(a)
        ya[:, :, 1:] = a[:, :, :-1]   # y * a
        Q[:, 0] = a + yb
        Q[:, 1] = ya + b

    # h[c] = sum_k P[c][k] * min(k, W - k); answer = min over c.
    ks = np.arange(W + 1, dtype=np.int64)
    w = np.minimum(ks, W - ks)
    h = P @ w
    print(int(h.min()))

solve()