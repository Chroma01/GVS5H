import sys


def mat_mul(x, y, mod):
    n = len(x)
    z = [[0] * n for _ in range(n)]
    for i in range(n):
        zi = z[i]
        xi = x[i]
        for k, xik in enumerate(xi):
            if xik:
                yk = y[k]
                for j in range(n):
                    zi[j] += xik * yk[j]
        for j in range(n):
            zi[j] %= mod
    return z


def mat_pow(a, e, mod):
    n = len(a)
    r = [[0] * n for _ in range(n)]
    for i in range(n):
        r[i][i] = 1
    while e:
        if e & 1:
            r = mat_mul(r, a, mod)
        e >>= 1
        if e:
            a = mat_mul(a, a, mod)
    return r


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, p = data[0], data[1]
    vals = data[2:]
    a = [vals[i * n:(i + 1) * n] for i in range(n)]

    if p == 2:
        c = [[1 if a[i][j] == 0 else a[i][j] for j in range(n)]
             for i in range(n)]
        ans = mat_mul(c, c, p)
        sys.stdout.write("\n".join(" ".join(map(str, row)) for row in ans))
        return

    zero_count = sum(a[i][j] == 0 for i in range(n) for j in range(n))
    sign = 1 if zero_count % 2 == 0 else p - 1

    ans = mat_pow(a, p, p)

    diagonal_zero = [a[i][i] == 0 for i in range(n)]

    for i in range(n):
        for j in range(n):
            v = ans[i][j]

            if diagonal_zero[i]:
                v += a[i][j]
            if diagonal_zero[j]:
                v += a[i][j]

            if p == 3 and i != j and a[i][j] == 0:
                v += a[j][i]

            ans[i][j] = (sign * v) % p

    sys.stdout.write("\n".join(" ".join(map(str, row)) for row in ans))


if __name__ == "__main__":
    main()