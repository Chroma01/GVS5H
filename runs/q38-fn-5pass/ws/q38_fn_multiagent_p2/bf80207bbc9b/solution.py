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

    # With one column, every cell can be made zero independently.
    if W == 1:
        print(0)
        return

    N = 1 << W
    freq = [0] * N

    for s in data[2:2 + H]:
        freq[int(s, 2)] += 1
    del data

    # popcount for every mask
    pc = [0] * N
    for i in range(1, N):
        pc[i] = pc[i >> 1] + (i & 1)

    # Binomial coefficients up to W
    C = [[0] * (W + 1) for _ in range(W + 1)]
    for i in range(W + 1):
        C[i][0] = 1
        C[i][i] = 1
        for j in range(1, i):
            C[i][j] = C[i - 1][j - 1] + C[i - 1][j]

    # Kernel K[d] = min(popcount(d), W - popcount(d)).
    # Its FWHT depends only on the popcount of the transform mask.
    # Compute that transform analytically to avoid a third FWHT.
    K = [min(i, W - i) for i in range(W + 1)]
    Khat = [0] * (W + 1)

    for t in range(W + 1):
        n_out = W - t
        Ct = C[t]
        Cout = C[n_out]
        total = 0

        for j in range(t + 1):
            inner = 0
            for l in range(n_out + 1):
                inner += Cout[l] * K[j + l]

            if j & 1:
                total -= Ct[j] * inner
            else:
                total += Ct[j] * inner

        Khat[t] = total

    # Forward FWHT of row-mask frequencies.
    fwht(freq)

    # Pointwise multiply by FWHT of the kernel.
    kh = Khat
    for i in range(N):
        freq[i] *= kh[pc[i]]

    # Inverse FWHT: same transform, then divide by N.
    fwht(freq)

    print(min(freq) // N)


if __name__ == "__main__":
    main()