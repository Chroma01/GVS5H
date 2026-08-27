import sys


def mat_mul(a, b, mod):
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


def mat_pow(a, e, mod):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        res[i][i] = 1

    while e:
        if e & 1:
            res = mat_mul(res, a, mod)
        a = mat_mul(a, a, mod)
        e >>= 1

    return res


def solve():
    input = sys.stdin.readline
    n, p = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    # For p = 2, every zero is replaced by 1.
    if p == 2:
        b = [[1 if a[i][j] == 0 else a[i][j] for j in range(n)]
             for i in range(n)]
        ans = mat_mul(b, b, p)
        for row in ans:
            print(*row)
        return

    zero = [[False] * n for _ in range(n)]
    c = [[0] * n for _ in range(n)]
    zero_count = 0

    for i in range(n):
        for j in range(n):
            if a[i][j] == 0:
                zero[i][j] = True
                zero_count += 1
            else:
                c[i][j] = a[i][j] % p

    # Walks containing no replaceable entry.
    ans = mat_pow(c, p, p)

    # One zero diagonal edge used p-1 times and one fixed edge.
    for u in range(n):
        if zero[u][u]:
            for i in range(n):
                ans[i][u] += c[i][u]
            for j in range(n):
                ans[u][j] += c[u][j]

    # For p = 3, a non-loop zero edge can occur twice with
    # the reverse fixed edge between its two occurrences.
    if p == 3:
        for u in range(n):
            for v in range(n):
                if u != v and zero[u][v]:
                    ans[u][v] += c[v][u]

    sign = 1 if zero_count % 2 == 0 else p - 1
    for i in range(n):
        for j in range(n):
            ans[i][j] = (ans[i][j] * sign) % p

    for row in ans:
        print(*row)


if __name__ == "__main__":
    solve()