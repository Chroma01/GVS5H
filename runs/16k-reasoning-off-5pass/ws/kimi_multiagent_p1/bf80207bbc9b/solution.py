import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    n = 1 << W
    f = [0] * n
    for i in range(H):
        f[int(data[2 + i], 2)] += 1

    # pass 1: g[v] = popcount(v); pass 2: g[v] = min(popcount(v), W - popcount(v))
    g = [0] * n
    for v in range(1, n):
        g[v] = g[v >> 1] + (v & 1)
    for v in range(n):
        p = g[v]
        if W - p < p:
            g[v] = W - p

    # FWHT (XOR convolution): butterfly a,b -> a+b, a-b
    def fwht(a):
        h = 1
        while h < n:
            step = h << 1
            for i in range(0, n, step):
                j = i
                end = i + h
                k = i + h
                while j < end:
                    x = a[j]
                    y = a[k]
                    a[j] = x + y
                    a[k] = x - y
                    j += 1
                    k += 1
            h = step

    fwht(f)
    fwht(g)
    for i in range(n):
        f[i] *= g[i]
    fwht(f)

    print(min(v // n for v in f))

main()