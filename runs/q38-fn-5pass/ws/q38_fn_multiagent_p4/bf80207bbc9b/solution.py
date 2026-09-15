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


def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    N = 1 << W

    freq = [0] * N
    for i in range(2, 2 + H):
        freq[int(data[i], 2)] += 1
    del data

    # Kernel value by Hamming weight: min(k, W-k)
    kernel_by_weight = [0] * (W + 1)
    for k in range(W + 1):
        kernel_by_weight[k] = k if k < W - k else W - k

    # Walsh transform of the kernel, depending only on popcount of the mask.
    # For a mask with popcount t:
    # TF[t] = sum_k kernel_by_weight[k] * [x^k] (1-x)^t (1+x)^(W-t)
    kernel_tf = [0] * (W + 1)
    for t in range(W + 1):
        poly = [1]

        # Multiply by (1 - x)^t
        for _ in range(t):
            new = [0] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c
                new[i + 1] -= c
            poly = new

        # Multiply by (1 + x)^(W-t)
        for _ in range(W - t):
            new = [0] * (len(poly) + 1)
            for i, c in enumerate(poly):
                new[i] += c
                new[i + 1] += c
            poly = new

        val = 0
        for k, c in enumerate(poly):
            val += c * kernel_by_weight[k]
        kernel_tf[t] = val

    # XOR convolution: freq * kernel
    fwht(freq)

    bc = int.bit_count
    freq = [v * kernel_tf[bc(i)] for i, v in enumerate(freq)]

    fwht(freq)

    # Inverse FWHT normalization
    print(min(freq) // N)


if __name__ == "__main__":
    solve()