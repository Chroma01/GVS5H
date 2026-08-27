import sys

def fwht(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        for base in range(0, n, step):
            end = base + h
            for i in range(base, end):
                x = a[i]
                y = a[i + h]
                a[i] = x + y
                a[i + h] = x - y
        h = step

def main():
    input = sys.stdin.buffer.readline
    H, W = map(int, input().split())
    n = 1 << W

    f = [0] * n
    for _ in range(H):
        f[int(input().strip(), 2)] += 1

    g = [0] * n
    for mask in range(n):
        ones = mask.bit_count()
        g[mask] = min(ones, W - ones)

    fwht(f)
    fwht(g)

    for i in range(n):
        f[i] *= g[i]

    fwht(f)

    print(min(x // n for x in f))

if __name__ == "__main__":
    main()