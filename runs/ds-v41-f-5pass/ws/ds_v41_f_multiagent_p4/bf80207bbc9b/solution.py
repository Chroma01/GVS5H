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


def main():
    data = sys.stdin.buffer.read().split()
    if not data:
        return

    H = int(data[0])
    W = int(data[1])
    n = 1 << W

    freq = [0] * n
    for row in data[2:2 + H]:
        freq[int(row, 2)] += 1

    # g[mask] = min(popcount(mask), W - popcount(mask))
    g = [0] * n
    for i in range(1, n):
        g[i] = g[i >> 1] + (i & 1)
    for i in range(n):
        p = g[i]
        q = W - p
        if q < p:
            g[i] = q

    fwht(freq)
    fwht(g)

    for i in range(n):
        freq[i] *= g[i]

    fwht(freq)

    ans = min(x // n for x in freq)
    print(ans)


if __name__ == "__main__":
    main()