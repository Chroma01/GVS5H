import sys


def fwht(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            end = i + h
            for j in range(i, end):
                k = j + h
                x = a[j]
                y = a[k]
                a[j] = x + y
                a[k] = x - y
        h = step


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    N = 1 << W

    f = [0] * N
    for idx in range(2, 2 + H):
        f[int(data[idx], 2)] += 1
    del data

    # Binomial coefficients up to W.
    C = [[0] * (W + 1) for _ in range(W + 1)]
    for n in range(W + 1):
        C[n][0] = 1
        C[n][n] = 1
        for k in range(1, n):
            C[n][k] = C[n - 1][k - 1] + C[n - 1][k]

    # h[d] = min(popcount(d), W - popcount(d)), grouped by weight.
    hw = [0] * (W + 1)
    for w in range(1, W):
        hw[w] = w if w <= W - w else W - w

    # Walsh transform of the radial kernel h, grouped by index weight.
    H_by_weight = [0] * (W + 1)
    for t in range(W + 1):
        total = 0
        C_t = C[t]
        C_out = C[W - t]
        out = W - t
        for w in range(1, W):
            hw_w = hw[w]
            lo = w - out
            if lo < 0:
                lo = 0
            hi = t if t < w else w
            inner = 0
            for j in range(lo, hi + 1):
                term = C_t[j] * C_out[w - j]
                if j & 1:
                    inner -= term
                else:
                    inner += term
            total += hw_w * inner
        H_by_weight[t] = total

    del C, hw

    # XOR convolution f * h via FWHT.
    fwht(f)

    hb = H_by_weight
    bc = int.bit_count
    for i, v in enumerate(f):
        f[i] = v * hb[bc(i)]

    fwht(f)

    print(min(f) // N)


if __name__ == "__main__":
    main()