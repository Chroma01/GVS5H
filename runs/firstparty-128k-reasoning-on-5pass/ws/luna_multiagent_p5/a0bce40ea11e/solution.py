import sys


def mat_mul(a, b, mod):
    n = len(a)
    c = [[0] * n for _ in range(n)]

    for i in range(n):
        ci = c[i]
        ai = a[i]
        for k, x in enumerate(ai):
            if x:
                bk = b[k]
                for j in range(n):
                    ci[j] += x * bk[j]
        for j in range(n):
            ci[j] %= mod

    return c


def mat_pow(a, exponent, mod):
    n = len(a)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1

    while exponent:
        if exponent & 1:
            result = mat_mul(result, a, mod)
        a = mat_mul(a, a, mod)
        exponent >>= 1

    return result


def solve():
    input = sys.stdin.readline
    n, p = map(int, input().split())
    a = [list(map(int, input().split())) for _ in range(n)]

    if p == 2:
        b = [
            [1 if a[i][j] == 0 else a[i][j] for j in range(n)]
            for i in range(n)
        ]
        ans = mat_mul(b, b, p)
    else:
        ans = mat_pow(a, p, p)

        # A zero diagonal edge can be used p-1 times, together with
        # one fixed edge. These contribute D*A + A*D.
        for i in range(n):
            if a[i][i] == 0:
                for j in range(n):
                    ans[i][j] += a[i][j]
                    ans[j][i] += a[j][i]

        # For p = 3, a non-loop zero edge can be used twice, with the
        # reverse fixed edge used once.
        if p == 3:
            for i in range(n):
                for j in range(n):
                    if i != j and a[i][j] == 0:
                        ans[i][j] += a[j][i]

        k = sum(a[i][j] == 0 for i in range(n) for j in range(n))
        factor = 1 if k % 2 == 0 else p - 1

        for i in range(n):
            for j in range(n):
                ans[i][j] = ans[i][j] * factor % p

    sys.stdout.write("\n".join(" ".join(map(str, row)) for row in ans))


if __name__ == "__main__":
    solve()