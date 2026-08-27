import sys


def fwht(a):
    n = len(a)
    h = 1
    while h < n:
        step = h << 1
        if h == 1:
            for j in range(0, n, 2):
                x = a[j]
                y = a[j + 1]
                a[j] = x + y
                a[j + 1] = x - y
        else:
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

    if W == 1:
        print(0)
        return

    n = 1 << (W - 1)
    f = [0] * n
    allones = (1 << W) - 1

    end = 2 + H
    for idx in range(2, end):
        s = data[idx]
        m = int(s, 2)
        if m & 1:
            m ^= allones
        f[m >> 1] += 1
    del data

    g = [0] * n
    for i in range(n):
        bc = i.bit_count()
        g[i] = bc if bc <= W - bc else W - bc

    fwht(f)
    fwht(g)

    for i in range(n):
        f[i] *= g[i]
    del g

    fwht(f)
    print(min(f) // n)


if __name__ == "__main__":
    solve()