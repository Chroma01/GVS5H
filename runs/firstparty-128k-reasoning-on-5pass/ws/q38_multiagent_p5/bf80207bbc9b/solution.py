import sys
from math import comb

def fwht(a, n):
    h = 1
    while h < n:
        h2 = h << 1
        for i in range(0, n, h2):
            for j in range(i, i + h):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h = h2

def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    H = int(data[0])
    W = int(data[1])
    n = 1 << W
    cnt = [0] * n
    for s in data[2:2 + H]:
        cnt[int(s, 2)] += 1

    cost = [min(k, W - k) for k in range(W + 1)]
    G = [0] * (W + 1)
    for t in range(W + 1):
        total = 0
        wt = W - t
        for k, f in enumerate(cost):
            if f:
                s = 0
                lo = max(0, k - wt)
                hi = min(t, k)
                for j in range(lo, hi + 1):
                    term = comb(t, j) * comb(wt, k - j)
                    if j & 1:
                        s -= term
                    else:
                        s += term
                total += f * s
        G[t] = total

    fwht(cnt, n)
    g = G
    for i in range(n):
        cnt[i] *= g[i.bit_count()]
    fwht(cnt, n)
    print(min(cnt) // n)

if __name__ == "__main__":
    main()