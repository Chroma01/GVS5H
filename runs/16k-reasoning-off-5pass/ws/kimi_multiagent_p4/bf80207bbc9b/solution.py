import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    N = 1 << W

    # Group identical rows: cnt[p] = number of rows equal to pattern p
    cnt = [0] * N
    for i in range(H):
        cnt[int(data[2 + i], 2)] += 1

    # g[q] = min(popcount(q), W - popcount(q))
    g = [0] * N
    for q in range(1, N):
        pc = g[q >> 1] + (q & 1)  # temporarily store popcount
        g[q] = pc
    for q in range(N):
        p = g[q]
        if W - p < p:
            g[q] = W - p

    # Fused forward FWHT (XOR) of cnt and g
    a = cnt
    b = g
    step = 1
    while step < N:
        jump = step << 1
        for base in range(0, N, jump):
            for off in range(base, base + step):
                u = a[off]; v = a[off + step]
                a[off] = u + v
                a[off + step] = u - v
                x = b[off]; y = b[off + step]
                b[off] = x + y
                b[off + step] = x - y
        step = jump

    # Pointwise product
    for i in range(N):
        a[i] *= b[i]

    # Inverse FWHT (same butterfly; divide by N afterwards)
    step = 1
    while step < N:
        jump = step << 1
        for base in range(0, N, jump):
            for off in range(base, base + step):
                u = a[off]; v = a[off + step]
                a[off] = u + v
                a[off + step] = u - v
        step = jump

    # Convolution values are non-negative integers exactly divisible by N
    ans = min(v // N for v in a)
    print(ans)

main()