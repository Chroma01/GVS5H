import sys


def fwht(a):
    n = len(a)
    if n <= 1:
        return

    # h = 1 stage, unrolled
    for i in range(0, n, 2):
        x = a[i]
        y = a[i + 1]
        a[i] = x + y
        a[i + 1] = x - y

    h = 2
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            j = i
            k = i + h
            end = k
            while j < end:
                x = a[j]
                y = a[k]
                a[j] = x + y
                a[k] = x - y
                j += 1
                k += 1
        h = step


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])

    # With one row, flip exactly the columns containing 1.
    # With one column, flip the column if needed, then flip rows independently.
    if H == 1 or W == 1:
        sys.stdout.write("0")
        return

    N = 1 << W
    freq = [0] * N

    for i in range(2, 2 + H):
        freq[int(data[i], 2)] += 1
    del data

    # Binomial coefficients up to W.
    comb = [[0] * (W + 1) for _ in range(W + 1)]
    for i in range(W + 1):
        comb[i][0] = 1
        comb[i][i] = 1
        for j in range(1, i):
            comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]

    # cost by Hamming weight
    cost_r = [0] * (W + 1)
    for r in range(W + 1):
        v = W - r
        cost_r[r] = r if r < v else v

    # Walsh transform of the radial cost array.
    # ct[t] = sum_d cost[popcount(d)] * (-1)^popcount(d & k),
    # where popcount(k) = t.
    ct = [0] * (W + 1)
    for t in range(W + 1):
        wt = W - t
        total = 0
        comb_t = comb[t]
        comb_wt = comb[wt]

        for r in range(1, W):
            f = cost_r[r]
            if f == 0:
                continue

            jmin = r - wt
            if jmin < 0:
                jmin = 0
            jmax = r if r < t else t

            kraw = 0
            for j in range(jmin, jmax + 1):
                term = comb_t[j] * comb_wt[r - j]
                if j & 1:
                    kraw -= term
                else:
                    kraw += term

            total += f * kraw

        ct[t] = total

    del comb, cost_r

    # Transform row-mask frequencies.
    fwht(freq)

    # Pointwise multiply by the precomputed Walsh transform of the cost array.
    bc = int.bit_count
    ct_local = ct
    a = freq
    for i in range(N):
        a[i] *= ct_local[bc(i)]

    # Inverse transform is the same FWHT, followed by division by N.
    fwht(a)

    ans = min(a) // N
    sys.stdout.write(str(ans))


if __name__ == "__main__":
    main()