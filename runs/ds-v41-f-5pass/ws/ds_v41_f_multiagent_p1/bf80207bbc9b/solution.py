import sys


def fwht_np(a, n):
    h = 1
    while h < n:
        a = a.reshape(-1, 2 * h)
        x = a[:, :h].copy()
        a[:, :h] += a[:, h:]
        a[:, h:] = x - a[:, h:]
        a = a.reshape(-1)
        h <<= 1
    return a


def fwht_py(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h = step


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2 + H]
    n = 1 << W
    masks = [int(s, 2) for s in rows]

    def build_F():
        F = [0] * n
        for m in masks:
            F[m] += 1
        return F

    try:
        import numpy as np

        F = np.zeros(n, dtype=np.int64)
        for m in masks:
            F[m] += 1

        G = np.zeros(n, dtype=np.int64)
        for t in range(n):
            pc = bin(t).count('1')
            G[t] = pc if pc < W - pc else W - pc

        F = fwht_np(F, n)
        G = fwht_np(G, n)
        C = F * G
        C = fwht_np(C, n)
        C //= n
        print(int(C.min()))
    except ImportError:
        F = build_F()
        G = [0] * n
        for t in range(n):
            pc = bin(t).count('1')
            G[t] = pc if pc < W - pc else W - pc
        fwht_py(F)
        fwht_py(G)
        for i in range(n):
            F[i] *= G[i]
        fwht_py(F)
        print(min(v // n for v in F))


main()