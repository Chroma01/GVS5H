import sys


def fwht(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            end = i + h
            for j in range(i, end):
                x = a[j]
                y = a[j + h]
                a[j] = x + y
                a[j + h] = x - y
        h = step


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    n = 1 << W

    freq = [0] * n
    for s in data[2:]:
        freq[int(s, 2)] += 1

    # Pascal table for small W (<= 18).
    comb = [[0] * (W + 1) for _ in range(W + 1)]
    for i in range(W + 1):
        comb[i][0] = 1
        comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]

    # cost[q] = min(popcount(q), W - popcount(q)).
    # Its FWHT depends only on k = popcount(mask).  Compute it analytically
    # to avoid one full FWHT pass.
    cost_hat = [0] * (W + 1)
    for k in range(W + 1):
        ck = comb[k]
        cw = comb[W - k]
        total = 0

        # j = popcount(x).  j = 0 and j = W have cost 0.
        for j in range(1, W):
            gj = j if j < W - j else W - j
            if gj == 0:
                continue

            lo = j - (W - k)
            if lo < 0:
                lo = 0
            hi = k if k < j else j

            kj = 0
            for l in range(lo, hi + 1):
                term = ck[l] * cw[j - l]
                if l & 1:
                    kj -= term
                else:
                    kj += term

            total += gj * kj

        cost_hat[k] = total

    fwht(freq)

    bit_count = int.bit_count
    ch = cost_hat
    for i in range(n):
        freq[i] *= ch[bit_count(i)]

    fwht(freq)

    print(min(freq) // n)


if __name__ == "__main__":
    solve()