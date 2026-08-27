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


def main():
    data = list(map(int, sys.stdin.buffer.read().split()))
    if not data:
        return

    n, p = data[0], data[1]
    a = []
    pos = 2
    for _ in range(n):
        a.append(data[pos:pos + n])
        pos += n

    # For p = 2, every entry becomes 1, since the only nonzero field element is 1.
    if p == 2:
        x = n & 1
        line = " ".join([str(x)] * n)
        sys.stdout.write("\n".join([line] * n))
        return

    zero_count = 0
    c = [[0] * n for _ in range(n)]
    diag_zero = [False] * n

    for i in range(n):
        for j in range(n):
            if a[i][j] == 0:
                zero_count += 1
                if i == j:
                    diag_zero[i] = True
            else:
                c[i][j] = a[i][j] % p

    ans = mat_pow(c, p, p)

    # For p > 3, the only exceptional surviving walks use a zero diagonal
    # edge p-1 times, with one fixed nonzero edge at the beginning or end.
    # These contribute C*D + D*C, where D marks zero diagonal positions.
    for i in range(n):
        for j in range(n):
            add = 0
            if diag_zero[j]:
                add += c[i][j]
            if diag_zero[i]:
                add += c[i][j]
            ans[i][j] = (ans[i][j] + add) % p

    # For p = 3 only, a non-loop zero edge u->v may occur as
    # (u->v), (v->u), (u->v). Its contribution is C[v][u].
    if p == 3:
        for i in range(n):
            for j in range(n):
                if i != j and a[i][j] == 0:
                    ans[i][j] = (ans[i][j] + c[j][i]) % p

    if zero_count & 1:
        for i in range(n):
            for j in range(n):
                ans[i][j] = (-ans[i][j]) % p

    sys.stdout.write("\n".join(" ".join(map(str, row)) for row in ans))


if __name__ == "__main__":
    main()