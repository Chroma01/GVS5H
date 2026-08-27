import sys


def matmul(a, b, mod):
    n = len(a)
    res = [[0] * n for _ in range(n)]
    for i in range(n):
        ri = res[i]
        ai = a[i]
        for k in range(n):
            x = ai[k]
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

    while e:
        if e & 1:
            res = matmul(res, a, mod)
        e >>= 1
        if e:
            a = matmul(a, a, mod)
    return res


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, p = data[0], data[1]
    vals = data[2:]
    a = [vals[i * n:(i + 1) * n] for i in range(n)]

    if p == 2:
        # Every entry becomes 1, since the only nonzero element of F_2 is 1.
        value = n & 1
        line = " ".join([str(value)] * n)
        print("\n".join([line] * n))
        return

    zero_count = 0
    c = [[0] * n for _ in range(n)]
    diag_zero = [0] * n

    for i in range(n):
        for j in range(n):
            if a[i][j] == 0:
                zero_count += 1
                if i == j:
                    diag_zero[i] = 1
            else:
                c[i][j] = a[i][j]

    if p == 3:
        c2 = matmul(c, c, p)
        ans = matmul(c2, c, p)

        # C D: a fixed edge entering a zero diagonal loop.
        # D C: a fixed edge leaving a zero diagonal loop.
        for i in range(n):
            if diag_zero[i]:
                for j in range(n):
                    ans[j][i] += c[j][i]
                    ans[i][j] += c[i][j]

        # For a non-loop zero edge i -> j, the only valid placement is
        # (i -> j), (j -> i), (i -> j).
        for i in range(n):
            for j in range(n):
                if i != j and a[i][j] == 0:
                    ans[i][j] += c[j][i]

        for i in range(n):
            for j in range(n):
                ans[i][j] %= p
    else:
        ans = matpow(c, p, p)

        # Add C D + D C.
        for i in range(n):
            if diag_zero[i]:
                for j in range(n):
                    ans[j][i] += c[j][i]
                    ans[i][j] += c[i][j]

        for i in range(n):
            for j in range(n):
                ans[i][j] %= p

    if zero_count & 1:
        for i in range(n):
            for j in range(n):
                ans[i][j] = (-ans[i][j]) % p

    print("\n".join(" ".join(map(str, row)) for row in ans))


if __name__ == "__main__":
    main()