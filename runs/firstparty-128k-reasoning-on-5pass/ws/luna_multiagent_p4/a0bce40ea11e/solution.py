import sys


def matmul(a, b, mod):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        ri = res[i]
        ai = a[i]
        for k, x in enumerate(ai):
            if x:
                bk = b[k]
                for j in range(n):
                    ri[j] += x * bk[j]
        for j in range(n):
            ri[j] %= mod
    return res


def matpow(a, e, mod):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1
    base = a
    while e:
        if e & 1:
            res = matmul(res, base, mod)
        e >>= 1
        if e:
            base = matmul(base, base, mod)
    return res


def solve():
    input = sys.stdin.readline
    n, p = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    if p == 2:
        b = [[1 if a[i][j] == 0 else a[i][j] for j in range(n)]
             for i in range(n)]
        ans = matmul(b, b, 2)
        print("\n".join(" ".join(map(str, row)) for row in ans))
        return

    k = sum(x == 0 for row in a for x in row)
    m = [row[:] for row in a]
    mp = matpow(m, p, p)

    c = [[0] * n for _ in range(n)]

    # Contribution DA + AD, where D marks zero diagonal entries.
    for u in range(n):
        if a[u][u] == 0:
            for v in range(n):
                c[u][v] += a[u][v]
                c[v][u] += a[v][u]

    # For p = 3, a non-loop zero edge can occur twice with its
    # nonzero reverse edge between the two occurrences.
    if p == 3:
        for u in range(n):
            for v in range(n):
                if u != v and a[u][v] == 0 and a[v][u] != 0:
                    c[u][v] += a[v][u]

    sign = 1 if k % 2 == 0 else p - 1
    ans = [[sign * (mp[i][j] + c[i][j]) % p for j in range(n)]
           for i in range(n)]

    print("\n".join(" ".join(map(str, row)) for row in ans))


if __name__ == "__main__":
    solve()