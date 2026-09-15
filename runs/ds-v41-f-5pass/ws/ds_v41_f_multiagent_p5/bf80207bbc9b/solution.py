import sys


def fwht(a):
    # In-place (unnormalized) Fast Walsh-Hadamard Transform for XOR.
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        for i in range(0, n, step):
            j = i + h
            lo = a[i:j]
            hi = a[j:j + h]
            a[i:j] = [x + y for x, y in zip(lo, hi)]
            a[j:j + h] = [x - y for x, y in zip(lo, hi)]
        h = step


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    N = 1 << W

    # frequency array over row patterns
    f = [0] * N
    off = 2
    for i in range(H):
        f[int(data[off + i], 2)] += 1

    # popcount precomputation
    pc = [0] * N
    for i in range(1, N):
        pc[i] = pc[i >> 1] + (i & 1)

    # g[d] = min(popcount(d), W - popcount(d))
    g = [pc[x] if 2 * pc[x] <= W else W - pc[x] for x in range(N)]

    # XOR convolution h = f (*) g  ->  h[c] = sum_r f[r] * g[r ^ c]
    fwht(f)
    fwht(g)
    for i in range(N):
        f[i] *= g[i]
    fwht(f)

    ans = min(v // N for v in f)
    sys.stdout.write(str(ans) + "\n")


main()