import sys


def fwht(a):
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


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    N = 1 << W

    freq = [0] * N
    for s in data[2:2 + H]:
        freq[int(s, 2)] += 1

    # Compute the Walsh-Hadamard transform of the radial kernel
    # k[mask] = min(popcount(mask), W - popcount(mask)).
    #
    # If a mask c has weight s, then
    #   FWHT(k)[c] = sum_t cost[t] * K_t(s)
    # where
    #   K_t(s) = sum_j (-1)^j C(s, j) C(W-s, t-j).
    C = [[0] * (W + 1) for _ in range(W + 1)]
    for i in range(W + 1):
        C[i][0] = 1
        C[i][i] = 1
        for j in range(1, i):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    cost = [min(t, W - t) for t in range(W + 1)]
    walsh_kernel = [0] * (W + 1)

    for s in range(W + 1):
        total = 0
        for t in range(W + 1):
            kt = 0
            lo = t - (W - s)
            if lo < 0:
                lo = 0
            hi = t if t < s else s
            for j in range(lo, hi + 1):
                term = C[s][j] * C[W - s][t - j]
                if j & 1:
                    kt -= term
                else:
                    kt += term
            total += cost[t] * kt
        walsh_kernel[s] = total

    # XOR convolution:
    # answer[c] = sum_m freq[m] * k[m xor c]
    fwht(freq)

    bit_count = int.bit_count
    wk = walsh_kernel
    for i in range(N):
        freq[i] *= wk[bit_count(i)]

    fwht(freq)

    # The inverse unnormalized FWHT requires division by N.
    print(min(freq) // N)


if __name__ == "__main__":
    solve()