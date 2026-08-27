import sys
input = sys.stdin.readline

def solve():
    H, W = map(int, input().split())
    N = 1 << W
    freq = [0] * N
    for _ in range(H):
        s = input().strip()
        mask = int(s, 2)
        freq[mask] += 1

    # popcount for all 0..N-1
    pc = [0] * N
    for i in range(1, N):
        pc[i] = pc[i >> 1] + (i & 1)
    
    # f[mask] = min(popcount(mask), W - popcount(mask))
    f = [min(pc[mask], W - pc[mask]) for mask in range(N)]
    
    # FWHT for XOR convolution
    # We'll compute conv = freq XOR-convolved with f
    conv = freq[:]
    fwht = conv
    g = f[:]
    size = N
    step = 1
    while step < size:
        for i in range(0, size, step * 2):
            for j in range(step):
                u = fwht[i + j]
                v = fwht[i + j + step]
                fwht[i + j] = u + v
                fwht[i + j + step] = u - v
        step *= 2
    # transform g as well
    step = 1
    while step < size:
        for i in range(0, size, step * 2):
            for j in range(step):
                u = g[i + j]
                v = g[i + j + step]
                g[i + j] = u + v
                g[i + j + step] = u - v
        step *= 2
    
    # pointwise multiply
    for i in range(size):
        conv[i] = fwht[i] * g[i]
    
    # inverse FWHT
    step = 1
    while step < size:
        for i in range(0, size, step * 2):
            for j in range(step):
                u = conv[i + j]
                v = conv[i + j + step]
                conv[i + j] = (u + v) // 2
                conv[i + j + step] = (u - v) // 2
        step *= 2
    
    # conv[c] = sum over rows of f(row XOR c)
    ans = min(conv)
    print(ans)

solve()